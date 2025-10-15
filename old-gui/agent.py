import asyncio
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import csv
import difflib
from playwright.async_api import async_playwright
from datetime import datetime
import threading
import os
import screeninfo  # ✅ Added

LOGIN_URL = "https://my.lonestar.edu/psp/ihprd/?cmd=login"
FORM_URL = "https://my.lonestar.edu/psp/ihprd/EMPLOYEE/EMPL/c/LSC_TCR.LSC_TCRFORMS.GBL"
CSV_PATH = r"C:\Users\chase\My Drive\Rosters etc\Email Templates, Assignment Dates\Students.csv"

class Agent:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Exam Form Automation Agent")
        self.window.geometry("700x450")

        self.playwright = None
        self.context = None
        self.page = None
        self.loop = None
        self.thread = None

        self.students = []
        self.term = None
        self.exam = None
        self.exam_file_path = None

        self.create_widgets()
        self.start_async_loop()
        self.load_csv_on_start()

    def create_widgets(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=10)

        self.login_btn = tk.Button(frame, text="Login", command=self.start_login, width=20, height=2)
        self.login_btn.pack(side=tk.LEFT, padx=5)

        self.browse_btn = tk.Button(frame, text="Browse Exam File", command=self.browse_exam, width=20, height=2)
        self.browse_btn.pack(side=tk.LEFT, padx=5)

        self.start_btn = tk.Button(frame, text="Start Automation", command=self.start_form, width=20, height=2, state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        log_label = tk.Label(self.window, text="Log:", font=("Arial", 10, "bold"))
        log_label.pack(anchor=tk.W, padx=10)

        self.log_text = scrolledtext.ScrolledText(self.window, width=85, height=15, font=("Courier", 9))
        self.log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(self.window, text="Ready", fg="blue", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def update_status(self, text, color="blue"):
        self.status_label.config(text=text, fg=color)

    def start_async_loop(self):
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()

    def run_in_loop(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def load_csv_on_start(self):
        self.students = []
        try:
            with open(CSV_PATH, 'r', encoding='utf-8-sig') as file:
                lines = [line.strip() for line in file if line.strip()]

            if len(lines) < 4:
                raise ValueError("CSV missing required rows.")

            header_row = [x.strip() for x in lines[0].split(',')]
            data_row = [x.strip() for x in lines[1].split(',')]

            if 'Term' not in header_row or 'Exam' not in header_row:
                raise ValueError("CSV missing 'Term' or 'Exam' headers on line 1.")

            term_index = header_row.index('Term')
            exam_index = header_row.index('Exam')
            self.term = data_row[term_index]
            self.exam = data_row[exam_index]

            student_headers = [x.strip() for x in lines[2].split(',')]
            csv_data = lines[3:]
            reader = csv.DictReader(csv_data, fieldnames=student_headers)

            for row in reader:
                if not row.get('Class') or not row.get('Name'):
                    continue
                self.students.append(row)

            if self.students and self.term and self.exam:
                self.log(f"✅ Loaded {len(self.students)} student(s) from CSV.")
                self.log(f"📘 Term: {self.term}, Exam: {self.exam}")
                for s in self.students:
                    self.log(f"  Class: {s['Class']}, Name: {s['Name']}, Start: {s['Start Date']}, End: {s['End Date']}, Hours: {s['Hours']}, Minutes: {s['Minutes']}, Specify: {s['Specify']}")
                self.update_status("CSV loaded successfully", "green")
                self.start_btn.config(state=tk.NORMAL)
            else:
                self.log("⚠️ CSV missing term, exam, or student rows.")
                self.update_status("CSV incomplete", "red")
        except Exception as e:
            self.log(f"❌ Error reading CSV: {e}")
            self.update_status("Failed to load CSV", "red")

    def start_login(self):
        self.log("Opening browser for login...")
        self.login_btn.config(state=tk.DISABLED)
        self.run_in_loop(self.open_browser())

    async def open_browser(self):
        try:
            monitors = screeninfo.get_monitors()
            args = ['--disable-blink-features=AutomationControlled']

            # ✅ Automatically handle window position
            if len(monitors) == 1:
                main = monitors[0]
                args += [
                    f'--window-position={main.x + 50},{main.y + 50}',
                    '--window-size=1200,800'
                ]
                self.window.after(0, lambda: self.log("📺 Single monitor detected — opening browser on main display"))
            else:
                # Prefer 2nd monitor if available
                second = monitors[1]
                args += [
                    f'--window-position={second.x + 100},{second.y + 100}',
                    '--window-size=1400,900'
                ]
                self.window.after(0, lambda: self.log("🖥️ Dual monitor setup — opening browser on second display"))

            self.playwright = await async_playwright().start()
            self.context = await self.playwright.chromium.launch_persistent_context(
                "./browser_data", headless=False, args=args
            )
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            await self.page.goto(LOGIN_URL, timeout=10000)
            self.window.after(0, lambda: self.log("Login page loaded - please log in manually"))
            self.window.after(0, lambda: self.update_status("Please log in", "orange"))

        except Exception as e:
            msg = f"Error opening browser: {str(e)}"
            self.window.after(0, lambda: self.log(msg))
            self.window.after(0, lambda: self.update_status(msg, "red"))
            self.window.after(0, lambda: self.login_btn.config(state=tk.NORMAL))

    def browse_exam(self):
        file_path = filedialog.askopenfilename(title="Select Exam File", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if file_path:
            self.exam_file_path = file_path
            self.log(f"📂 Selected exam file: {file_path}")
            self.update_status("Exam file selected", "green")

    def start_form(self):
        if not self.exam_file_path:
            messagebox.showerror("Missing File", "Please select an exam file before starting.")
            return
        if not self.students:
            messagebox.showerror("Missing Data", "No students loaded from CSV.")
            return
        self.log("Starting automation...")
        self.start_btn.config(state=tk.DISABLED)
        self.run_in_loop(self.automate_form())

    async def automate_form(self):
        try:
            await self.page.goto(FORM_URL, wait_until='networkidle', timeout=10000)
            await asyncio.sleep(3)

            class_groups = {}
            for s in self.students:
                class_groups.setdefault(s['Class'], []).append(s)

            for class_code, students in class_groups.items():
                frame = self.page.frame(name="TargetContent")
                if not frame:
                    self.log("ERROR: Could not find TargetContent iframe")
                    return

                await frame.fill("#LSC_TCRFRMA_VW_LSC_TERM", self.term)
                await frame.fill("#LSC_TCRFRMA_VW_LSC_TCTESTNAME", self.exam)

                await frame.click("#PTS_CFG_CL_WRK_PTS_ADD_BTN", timeout=10000)
                await asyncio.sleep(2)

                await frame.fill("#LSC_TCRFORMS_LSC_OFFICELOCATION", "F255")
                await frame.fill("#LSC_TCRFORMS_LSC_BACKPHONE", "281-636-7774")
                await frame.fill("#LSC_TCRFORMS_LSC_CAMPUS", "400")
                await frame.check("input[name='LSC_TCRFORMS_LSC_TCCRSEINFO'][value='C']")
                await frame.check("#LSC_TCR_WEBCAMACK")
                await frame.check("#LSC_TCR_EXAMACK1")
                await frame.fill("#LSC_TCRFORMS_LSC_TCCRSENBR", class_code)

                await frame.click("#LSC_TCRFORMS_LSC_TCRINDSTU", timeout=10000)
                await asyncio.sleep(1)

                for i, student in enumerate(students):
                    magnifier_selector = f"#LSC_TCRFORMSTU_LSC_SEMPLID\\$prompt\\$img\\${i}"
                    try:
                        await frame.wait_for_selector(magnifier_selector, timeout=10000)
                        await frame.click(magnifier_selector, timeout=10000)
                        await self.select_student(student['Name'])
                        self.log(f"🔍 Selected student {student['Name']} in row {i}.")
                    except Exception:
                        self.log(f"⚠️ Could not find magnifier for row {i} ({student['Name']}). Skipping.")

                    if i < len(students) - 1:
                        try:
                            await frame.click("a[id^='LSC_TCRFORMSTU$new']", timeout=10000)
                            await asyncio.sleep(1)
                        except Exception:
                            self.log("⚠️ Could not click '+' to add new row.")

                first_student = students[0]
                await frame.check("#EXAM_TEST")
                await frame.fill("#LSC_TCRFORMS_LSC_STARTDATE", first_student['Start Date'])
                await frame.fill("#LSC_TCRFORMS_LSC_ENDDATE", first_student['End Date'])
                await frame.fill("#LSC_TCRFORMS_LSC_TCLIMITHOUR", first_student['Hours'])
                await frame.fill("#LSC_TCRFORMS_LSC_TCLIMITMINUTE", first_student['Minutes'])
                await frame.check("#LSC_TCTESTPICKUP_E")
                await frame.check("#MAT_SCRATCHPAPER")

                calc_type = "Scientific" if "1314" in class_code else ("Any" if "1324" in class_code else "None")
                await frame.select_option("#LSC_TCRFORMS_LSC_TCCALCULATOR", label=calc_type)

                if first_student['Specify'].strip():
                    await frame.fill("#LSC_TCRFORMS_LSC_TCOTHER1", first_student['Specify'])

                await frame.check("#LSC_TCRFORMCAMP_LSC_TCRSELECTCAMPU\\$11")

                try:
                    await frame.click("#LSC_TCRFIATT_WK_ATTACHADD", timeout=10000)
                    self.log("📎 Clicked Add Attachment button... waiting for modal to appear.")

                    await self.page.wait_for_selector("#pt_modal", timeout=10000)
                    file_inputs = await self.page.query_selector_all("input[type='file']")

                    if not file_inputs:
                        self.log("❌ No file inputs found in modal.")
                    else:
                        for i, fi in enumerate(file_inputs):
                            try:
                                await fi.set_input_files(self.exam_file_path)
                                self.log(f"✅ File attached using input #{i}.")
                                break
                            except Exception as e:
                                self.log(f"⚠️ Could not use input #{i}: {e}")

                    await self.page.click("#Upload", timeout=10000)
                    await asyncio.sleep(3)
                    self.log("✅ File uploaded successfully.")

                except Exception as e:
                    self.log(f"❌ Error during file upload: {e}")

                self.log(f"✅ Completed automation for class {class_code} with {len(students)} student(s).")

            self.update_status("All students processed successfully.", "green")
        except Exception as e:
            msg = f"Error during automation: {str(e)}"
            self.window.after(0, lambda: self.log(msg))
            self.window.after(0, lambda: self.update_status(msg, "red"))

    async def select_student(self, student_name):
        await self.page.wait_for_selector("iframe[name^='ptModFrame_']", timeout=10000)
        lookup_frame = None
        for f in self.page.frames:
            if f.name and f.name.startswith("ptModFrame_"):
                lookup_frame = f
                break
        if not lookup_frame:
            self.window.after(0, lambda: self.log("Could not find student lookup frame."))
            return

        await lookup_frame.wait_for_selector("a.PSSRCHRESULTSODDROW, a.PSSRCHRESULTSEVENROW", timeout=10000)
        links = await lookup_frame.query_selector_all("a.PSSRCHRESULTSODDROW, a.PSSRCHRESULTSEVENROW")

        best_match = None
        best_ratio = 0.0
        best_text = ""
        for link in links:
            text = (await link.inner_text()).strip().lower()
            ratio = difflib.SequenceMatcher(None, text, student_name.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = link
                best_text = text

        if best_match and best_ratio > 0.5:
            await best_match.click()
            self.window.after(0, lambda: self.log(f"Selected best match '{best_text}' for {student_name} (score {best_ratio:.2f})"))
        else:
            self.window.after(0, lambda: self.log(f"No good match found for {student_name}. Best score: {best_ratio:.2f}"))

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def on_close(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.window.destroy()

if __name__ == "__main__":
    app = Agent()
    app.run()
