import sys

import os

import json

import traceback

import io

import difflib

import csv

import asyncio

import threading

import pathlib

import shutil

import tempfile

import subprocess

from datetime import datetime

from playwright.async_api import async_playwright

from docx import Document



# Set UTF-8 encoding for stdout and stderr

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')



class WebAutomationAgent:

    def __init__(self):

        self.playwright = None

        self.context = None

        self.page = None

        self.loop = None

        self.thread = None

        self.students = []

        self.term = None

        self.exam = None

        self.exam_file_path = None

        self.start_async_loop()

        self.load_csv_data()



    def log(self, message):

        print(f"[LOG] {message}", file=sys.stderr)



    def update_status(self, text, color="blue"):

        print(f"[STATUS] {text}", file=sys.stderr)



    def open_email_template(self, class_code, exam_date):

        """Open the appropriate email template and replace the date"""

        try:

            # Determine which email template to use based on class code

            if "1314" in class_code:

                template_path = r"C:\Users\chase\My Drive\Rosters etc\Email Templates, Assignment Dates\M1314 Make up Exam Automation.docx"

            elif "1324" in class_code:

                template_path = r"C:\Users\chase\My Drive\Rosters etc\Email Templates, Assignment Dates\M1324 Make up Exam Automation.docx"

            else:

                self.log("⚠️ Unknown class code, using M1314 template as default")

                template_path = r"C:\Users\chase\My Drive\Rosters etc\Email Templates, Assignment Dates\M1314 Make up Exam Automation.docx"

            

            self.log(f"📧 Opening email template: {os.path.basename(template_path)}")

            self.log(f"📅 Exam date: {exam_date}")

            

            # Load the document and replace the date

            doc = Document(template_path)

            

            # Replace "Insert Date" with the actual exam date

            for paragraph in doc.paragraphs:

                if "Insert Date" in paragraph.text:

                    paragraph.text = paragraph.text.replace("Insert Date", exam_date)

                    self.log(f"✅ Replaced 'Insert Date' with '{exam_date}'")

                

                # Also replace "[Insert Date]" if it exists with brackets

                if "[Insert Date]" in paragraph.text:

                    paragraph.text = paragraph.text.replace("[Insert Date]", exam_date)

                    self.log(f"✅ Replaced '[Insert Date]' with '{exam_date}'")

            

            # Save over the original template (no copy)

            doc.save(template_path)

            self.log(f"✅ Updated template with exam date")

            

            # Open the template

            subprocess.Popen(['start', '', template_path], shell=True)

            self.log("✅ Email template opened")

            

        except Exception as e:

            self.log(f"❌ Error opening email template: {e}")

            # Fallback: open original template

            try:

                subprocess.Popen(['start', '', template_path], shell=True)

                self.log("📝 Opened original template - please manually replace 'Insert Date'")

            except:

                self.log("❌ Failed to open template")



    def start_async_loop(self):

        def run_loop():

            self.loop = asyncio.new_event_loop()

            asyncio.set_event_loop(self.loop)

            self.loop.run_forever()

        self.thread = threading.Thread(target=run_loop, daemon=True)

        self.thread.start()



    def load_csv_data(self):

        try:

            # Use your hardcoded CSV path (as you've specified multiple times)

            csv_path = r"C:\Users\chase\My Drive\Rosters etc\Email Templates, Assignment Dates\Students.csv"

            

            # DEBUG: Show exactly where we're looking

            self.log(f"🔍 I AM LOOKING IN THE FOLDER: {os.path.dirname(csv_path)}")

            self.log(f"🔍 LOOKING FOR FILE: {os.path.basename(csv_path)}")

            self.log(f"🔍 FULL PATH: {csv_path}")

            

            if not os.path.exists(csv_path):

                self.log(f"❌ CSV file not found at: {csv_path}")

                return

            

            self.log(f"✅ CSV file found! Reading contents...")



            with open(csv_path, 'r', encoding='utf-8-sig') as file:

                lines = [line.strip() for line in file if line.strip()]



            if len(lines) < 4:

                self.log("CSV missing required rows")

                return



            header_row = [x.strip() for x in lines[0].split(',')]

            data_row = [x.strip() for x in lines[1].split(',')]



            if 'Term' not in header_row or 'Exam' not in header_row:

                self.log("CSV missing 'Term' or 'Exam' headers")

                return



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



            if self.students and self.term:

                self.log(f"✅ Loaded {len(self.students)} student(s) from CSV")

                self.log(f"📘 Term: {self.term}")

                self.log(f"📋 THE CSV FILE HAS THE FOLLOWING STUDENTS LISTED:")

                for i, s in enumerate(self.students, 1):

                    self.log(f"  {i}. Class: {s['Class']}, Name: {s['Name']}, Start: {s['Start Date']}, End: {s['End Date']}, Hours: {s['Hours']}, Minutes: {s['Minutes']}, Specify: {s['Specify']}")

            else:

                self.log("⚠️ CSV missing term or student rows")

                if not self.students:

                    self.log("❌ NO STUDENTS FOUND IN CSV")

                if not self.term:

                    self.log("❌ NO TERM FOUND IN CSV")



        except Exception as e:

            self.log(f"❌ Error reading CSV: {e}")



    async def select_student(self, student_name):

        await self.page.wait_for_selector("iframe[name^='ptModFrame_']", timeout=10000)

        lookup_frame = None

        for f in self.page.frames:

            if f.name and f.name.startswith("ptModFrame_"):

                lookup_frame = f

                break

        if not lookup_frame:

            self.log("Could not find student lookup frame")

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

            self.log(f"Selected best match '{best_text}' for {student_name} (score {best_ratio:.2f})")

        else:

            self.log(f"No good match found for {student_name}. Best score: {best_ratio:.2f}")



    async def automate_form(self):

        try:

            # Open email template FIRST before starting automation

            if self.students:

                first_student = self.students[0]

                class_code = first_student.get('Class', '')

                exam_date = first_student.get('End Date', '')

                

                self.log("📧 Opening email template FIRST...")

                self.open_email_template(class_code, exam_date)

                self.log("📧 Email template opened - you can edit it while automation runs")

            

            self.log("Starting browser automation...")

            self.playwright = await async_playwright().start()



            try:

                await asyncio.sleep(0.5)

                browser = await self.playwright.chromium.connect_over_cdp("http://localhost:9222")

                self.log("✅ Connected to existing browser session")

                contexts = browser.contexts

                if contexts:

                    self.context = contexts[0]

                    self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

                else:

                    self.context = await browser.new_context()

                    self.page = await self.context.new_page()

            except Exception as e:

                self.log(f"❌ Could not connect to existing browser: {e}")

                # Use the new Playwright API with launch_persistent_context

                self.context = await self.playwright.chromium.launch_persistent_context(

                    user_data_dir="../../Shared-Browser-Data/Make-Up-Exam-Macro-browser_data",

                    headless=False,

                    args=['--remote-debugging-port=9222', '--window-position=-1920,0', '--window-size=1920,1080']

                )

                self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()



            self.log("🌐 Navigating to form page...")

            await self.page.goto("https://my.lonestar.edu/psp/ihprd/EMPLOYEE/EMPL/c/LSC_TCR.LSC_TCRFORMS.GBL", wait_until='networkidle', timeout=15000)

            await self.page.wait_for_load_state('networkidle')

            self.log("✅ Page loaded, waiting for frames...")

            await asyncio.sleep(3)



            class_groups = {}

            for s in self.students:

                class_groups.setdefault(s['Class'], []).append(s)



            for class_code, students in class_groups.items():

                self.log(f"Processing class {class_code} with {len(students)} students")



                if class_code != list(class_groups.keys())[0]:

                    await self.page.reload()

                    await self.page.wait_for_load_state('domcontentloaded')



                self.log("🔍 Looking for TargetContent iframe...")

                frame = self.page.frame(name="TargetContent")

                if not frame:

                    for f in self.page.frames:

                        self.log(f"  - Frame: {f.name or 'unnamed'} (URL: {f.url})")

                    for alt_name in ["TargetContent", "ptModFrame_", "ptFrame_"]:

                        frame = self.page.frame(name=alt_name)

                        if frame:

                            self.log(f"✅ Found alternative frame: {alt_name}")

                            break

                    if not frame:

                        self.log("❌ ERROR: Could not find any suitable iframe")

                        continue



                if self.exam_file_path:

                    self.exam = os.path.splitext(os.path.basename(self.exam_file_path))[0]



                await frame.wait_for_selector("#LSC_TCRFRMA_VW_LSC_TERM")

                await frame.fill("#LSC_TCRFRMA_VW_LSC_TERM", self.term)

                await frame.fill("#LSC_TCRFRMA_VW_LSC_TCTESTNAME", self.exam)

                await frame.click("#PTS_CFG_CL_WRK_PTS_ADD_BTN")



                await frame.wait_for_selector("#LSC_TCRFORMS_LSC_OFFICELOCATION")

                await frame.fill("#LSC_TCRFORMS_LSC_OFFICELOCATION", "F255")

                await frame.fill("#LSC_TCRFORMS_LSC_BACKPHONE", "281-636-7774")

                await frame.fill("#LSC_TCRFORMS_LSC_CAMPUS", "400")

                await frame.check("input[name='LSC_TCRFORMS_LSC_TCCRSEINFO'][value='C']")

                await frame.check("#LSC_TCR_WEBCAMACK")

                await frame.check("#LSC_TCR_EXAMACK1")

                await frame.fill("#LSC_TCRFORMS_LSC_TCCRSENBR", class_code)

                await frame.click("#LSC_TCRFORMS_LSC_TCRINDSTU")



                for i, student in enumerate(students):

                    magnifier_selector = f"#LSC_TCRFORMSTU_LSC_SEMPLID\\$prompt\\$img\\${i}"

                    await frame.wait_for_selector(magnifier_selector)

                    await frame.click(magnifier_selector)

                    await self.select_student(student['Name'])

                    if i < len(students) - 1:

                        # Click the plus button with correct ID format: LSC_TCRFORMSTU$new$i$$0

                        await asyncio.sleep(0.5)

                        plus_button_selector = f"#LSC_TCRFORMSTU\\$new\\${i}\\$\\$0"

                        try:

                            await frame.click(plus_button_selector)

                            self.log(f"✅ Clicked plus button for row {i}")

                        except Exception as e:

                            self.log(f"⚠️ Error clicking plus button: {e}")

                        await asyncio.sleep(0.5)  # Wait for new row to appear



                first_student = students[0]

                await frame.check("#EXAM_TEST")

                

                # Clear and fill date fields with debugging

                self.log(f"📅 Filling Start Date: '{first_student['Start Date']}'")

                await frame.fill("#LSC_TCRFORMS_LSC_STARTDATE", "")

                await asyncio.sleep(0.5)

                # Use JavaScript to set the date value directly (bypasses browser locale issues)

                await frame.evaluate(f"document.querySelector('#LSC_TCRFORMS_LSC_STARTDATE').value = '{first_student['Start Date']}'")

                

                self.log(f"📅 Filling End Date: '{first_student['End Date']}'")

                await frame.fill("#LSC_TCRFORMS_LSC_ENDDATE", "")

                await asyncio.sleep(0.5)

                # Use JavaScript to set the date value directly (bypasses browser locale issues)

                await frame.evaluate(f"document.querySelector('#LSC_TCRFORMS_LSC_ENDDATE').value = '{first_student['End Date']}'")

                

                # Wait a moment for form validation

                await asyncio.sleep(1)

                await frame.fill("#LSC_TCRFORMS_LSC_TCLIMITHOUR", first_student['Hours'])

                await frame.fill("#LSC_TCRFORMS_LSC_TCLIMITMINUTE", first_student['Minutes'])

                await frame.check("#LSC_TCTESTPICKUP_E")

                await frame.check("#MAT_SCRATCHPAPER")



                calc_type = "Scientific" if "1314" in class_code else ("Any" if "1324" in class_code else "None")

                await frame.select_option("#LSC_TCRFORMS_LSC_TCCALCULATOR", label=calc_type)



                if first_student['Specify'].strip():

                    await frame.fill("#LSC_TCRFORMS_LSC_TCOTHER1", first_student['Specify'])



                await frame.check("#LSC_TCRFORMCAMP_LSC_TCRSELECTCAMPU\\$11")



                # File upload fix

                try:

                    self.log("📎 Clicking Add Attachment button...")

                    await frame.click("#LSC_TCRFIATT_WK_ATTACHADD", timeout=10000)

                    self.log("🔍 Add Attachment clicked — waiting for modal iframe...")



                    modal_frame = None

                    for _ in range(20):

                        await asyncio.sleep(0.5)

                        for f in self.page.frames:

                            if f.name and f.name.startswith("ptModFrame_"):

                                modal_frame = f

                                break

                        if modal_frame:

                            break



                    if not modal_frame:

                        raise Exception("❌ Modal attachment frame not found!")



                    self.log(f"✅ Found modal frame: {modal_frame.name}")



                    file_input = await modal_frame.wait_for_selector("input[type='file']", timeout=10000)

                    self.log("✅ File input found — uploading file...")



                    original = pathlib.Path(self.exam_file_path)

                    temp = pathlib.Path(tempfile.gettempdir()) / original.name

                    shutil.copy2(original, temp)



                    await file_input.set_input_files(str(temp))



                    upload_button = await modal_frame.wait_for_selector("#Upload, button:has-text('Upload'), input[id='Upload']", timeout=10000)

                    await upload_button.click()

                    self.log("✅ Upload button clicked — waiting for upload completion...")



                    await asyncio.sleep(2)

                    self.log("✅ File uploaded successfully")



                except Exception as e:

                    self.log(f"❌ File upload error: {e}")



                self.log(f"✅ Completed automation for class {class_code}")



            self.log("All students processed successfully")



        except Exception as e:

            self.log(f"Automation error: {str(e)}")

            raise



    def run_automation(self, exam_file_path):

        try:

            self.exam_file_path = exam_file_path

            self.log("Starting automation...")

            self.update_status("Starting automation...", "blue")

            asyncio.run(self.automate_form())

            self.log("Automation completed successfully")

            self.update_status("Automation completed", "green")

            return True

        except Exception as e:

            self.log(f"Automation error: {str(e)}")

            self.update_status(f"Error: {str(e)}", "red")

            return False

        finally:

            try:

                if hasattr(self, 'context'):

                    asyncio.run(self.context.close())

                    self.log("✅ Browser context closed")

                if hasattr(self, 'playwright'):

                    asyncio.run(self.playwright.stop())

                    self.log("✅ Playwright stopped")

            except Exception as cleanup_error:

                self.log(f"⚠️ Cleanup error: {cleanup_error}")



if __name__ == "__main__":

    try:

        print("🐍 PYTHON SCRIPT STARTED!", file=sys.stderr)

        print(f"🐍 Arguments received: {sys.argv}", file=sys.stderr)

        print(f"🐍 Working directory: {os.getcwd()}", file=sys.stderr)

        

        agent = WebAutomationAgent()

        exam_file_path = sys.argv[2] if len(sys.argv) > 2 else None

        print(f"🐍 Exam file path: {exam_file_path}", file=sys.stderr)

        

        success = agent.run_automation(exam_file_path)

        result = {"success": success, "message": "Automation completed" if success else "Automation failed"}

        print(json.dumps(result))

    except Exception as e:

        print(f"❌ PYTHON SCRIPT ERROR: {e}", file=sys.stderr)

        result = {"success": False, "error": str(e), "traceback": traceback.format_exc()}

        print(json.dumps(result))