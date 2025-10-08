import asyncio
import tkinter as tk
from tkinter import scrolledtext
from playwright.async_api import async_playwright
from datetime import datetime
import json
import threading
import os

LOGIN_URL = "https://my.lonestar.edu/psp/ihprd/?cmd=login"
FORM_URL = "https://my.lonestar.edu/psp/ihprd/EMPLOYEE/EMPL/c/LSC_TCR.LSC_TCRFORMS.GBL"

class ClickCaptureGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Form Click Capture Tool – iframe-aware")
        self.window.geometry("620x520")

        self.playwright = None
        self.context = None
        self.page = None
        self.captures = []
        self.monitoring = False
        self.loop = None
        self.thread = None
        self.monitor_task = None

        self.create_widgets()
        self.start_async_loop()

    def create_widgets(self):
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        self.login_btn = tk.Button(btn_frame, text="1. Open Browser & Login",
                                   command=self.start_login, width=20, height=2)
        self.login_btn.pack(side=tk.LEFT, padx=5)

        self.form_btn = tk.Button(btn_frame, text="2. Go to Form Page",
                                  command=self.goto_form, width=20, height=2, state=tk.DISABLED)
        self.form_btn.pack(side=tk.LEFT, padx=5)

        self.extract_btn = tk.Button(btn_frame, text="3. Start Extracting",
                                     command=self.start_extracting, width=20, height=2,
                                     state=tk.DISABLED, bg="#4CAF50", fg="white")
        self.extract_btn.pack(side=tk.LEFT, padx=5)

        self.done_btn = tk.Button(btn_frame, text="Done – Save Captures",
                                  command=self.save_and_close, width=20, height=2, state=tk.DISABLED)
        self.done_btn.pack(side=tk.LEFT, padx=5)

        self.exit_btn = tk.Button(btn_frame, text="Exit Without Saving",
                                  command=self.exit_without_saving, width=20, height=2, bg="#ff6b6b", fg="white")
        self.exit_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(self.window, text="Log:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)
        self.log_text = scrolledtext.ScrolledText(self.window, width=72, height=22, font=("Courier", 9))
        self.log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.status_label = tk.Label(self.window, text="Ready to start", fg="blue", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}] {msg}\n")
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

    def start_login(self):
        self.login_btn.config(state=tk.DISABLED)
        self.run_in_loop(self.open_browser())
        self.update_status("Launching browser...", "orange")

    def goto_form(self):
        self.form_btn.config(state=tk.DISABLED)
        self.run_in_loop(self.navigate_to_form())

    def start_extracting(self):
        self.extract_btn.config(state=tk.DISABLED)
        self.run_in_loop(self.begin_monitoring_after_ready())

    async def begin_monitoring_after_ready(self):
        try:
            await self.setup_click_capture_with_iframe_support()
            self.monitoring = True
            self.monitor_task = asyncio.create_task(self.monitor_clicks())
            self.window.after(0, lambda: self.log("✅ Click capture ready (iframe-aware)."))
            self.window.after(0, lambda: self.update_status("Listening for clicks (all frames)...", "green"))
            self.window.after(0, lambda: self.done_btn.config(state=tk.NORMAL))
        except Exception as e:
            self.log(f"Setup error: {e}")
            self.update_status("Error setting up click capture", "red")

    async def setup_click_capture_with_iframe_support(self):
        js_listener = """
            () => {
                function markClickable(el) {
                    if (el.__clickInstalled) return;
                    el.__clickInstalled = true;
                    el.addEventListener('click', e => {
                        const t = e.target;
                        window.lastClickedElement = {
                            tag: t.tagName,
                            id: t.id || '',
                            name: t.name || '',
                            class: t.className || '',
                            type: t.type || '',
                            text: t.textContent?.trim().substring(0,150) || '',
                            value: t.value || '',
                            outer: t.outerHTML?.substring(0,400) || ''
                        };
                        t.style.outline = '3px solid lime';
                        setTimeout(() => t.style.outline = '', 700);
                    }, true);
                }
                document.querySelectorAll('*').forEach(markClickable);
                const obs = new MutationObserver(m => {
                    for (const rec of m)
                        for (const n of rec.addedNodes)
                            if (n.nodeType === 1) {
                                markClickable(n);
                                n.querySelectorAll('*').forEach(markClickable);
                            }
                });
                obs.observe(document.body, { childList: true, subtree: true });
            }
        """
        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.evaluate(js_listener)

        # Inject into all frames (including modal ones)
        async def inject_into_all_frames():
            for f in self.page.frames:
                try:
                    await f.evaluate(js_listener)
                    self.log(f"Injected listener into frame: {f.name or f.url[:60]}")
                except Exception as e:
                    self.log(f"Injection failed in frame {f.name or f.url[:60]}: {e}")
        await inject_into_all_frames()

        # Watch for new iframes dynamically
        async def watch_new_frames():
            while True:
                await asyncio.sleep(1)
                for f in self.page.frames:
                    try:
                        has_listener = await f.evaluate("() => !!window.lastClickedElement || true")
                        if has_listener is None:
                            await f.evaluate(js_listener)
                            self.log(f"Reinjected listener into new frame {f.name or f.url[:60]}")
                    except:
                        pass
        asyncio.create_task(watch_new_frames())

    async def monitor_clicks(self):
        self.log("🔍 Monitoring clicks (including iframes)...")
        while self.monitoring:
            await asyncio.sleep(0.3)
            for frame in [self.page] + self.page.frames:
                try:
                    click_data = await frame.evaluate("() => window.lastClickedElement || null")
                    if click_data:
                        click_data['frameName'] = frame.name or ''
                        click_data['frameUrl'] = frame.url
                        self.captures.append({
                            "timestamp": datetime.now().isoformat(),
                            "element": click_data,
                            "page_url": self.page.url
                        })
                        self.log(f"CLICK → {click_data['tag']} id='{click_data['id']}' text='{click_data['text'][:50]}' in frame '{click_data['frameName']}'")
                        await frame.evaluate("() => window.lastClickedElement = null")
                except:
                    continue

    async def open_browser(self):
        try:
            os.makedirs("browser_data", exist_ok=True)
            self.playwright = await async_playwright().start()
            self.context = await self.playwright.chromium.launch_persistent_context(
                "browser_data", headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            await self.page.goto(LOGIN_URL)
            self.log("Browser opened – please log in.")
            self.update_status("Login to your account", "orange")
            self.form_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"Browser error: {e}")
            self.login_btn.config(state=tk.NORMAL)

    async def navigate_to_form(self):
        try:
            await self.page.goto(FORM_URL)
            await self.page.wait_for_load_state('domcontentloaded')
            self.log("Form page loaded.")
            self.extract_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.log(f"Form navigation error: {e}")
            self.form_btn.config(state=tk.NORMAL)

    def save_and_close(self):
        self.monitoring = False
        file = f"click_captures_iframe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.captures, f, indent=2, ensure_ascii=False)
        self.log(f"Saved {len(self.captures)} clicks → {file}")
        self.update_status("Saved successfully.", "green")
        self.run_in_loop(self.cleanup())
        self.window.destroy()

    def exit_without_saving(self):
        self.monitoring = False
        self.run_in_loop(self.cleanup())
        self.window.destroy()

    async def cleanup(self):
        try:
            if self.context:
                await self.context.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Cleanup error: {e}")

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def on_close(self):
        self.monitoring = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.window.destroy()

if __name__ == "__main__":
    app = ClickCaptureGUI()
    app.run()
