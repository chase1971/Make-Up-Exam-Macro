#===============================================================================
# CODE SYNOPSIS: html extractor.py
# Generated: 2025-10-25 15:40:01
# INTENT: Provides asynchronous operations for close operations.
#===============================================================================
#
# OVERVIEW:
#   Total Lines: 254
#   Functions: 22
#   Classes: 1
#   Global Variables: 3
#
# Key Dependencies:
#   - asyncio
#   - datetime
#   - json
#   - os
#   - playwright.async_api
#   - threading
#   - tkinter
#
#===============================================================================
# ════════════════════
# BEGIN MACHINE-READABLE DATA (for automated processing)
# ════════════════════
# SYNOPSIS_ANNOTATED: YES
# LAST_ANALYZED: 2025-10-25 15:40:01
# FILE: html extractor.py
# IMPORTS_EXTERNAL: asyncio, datetime, json, os, playwright.async_api, threading, tkinter
# IMPORTS_LOCAL: 
# GLOBALS: FORM_URL, LOGIN_URL, app
# FUNCTIONS: __init__, begin_monitoring_after_ready, cleanup, create_widgets, exit_without_saving, goto_form, inject_into_all_frames, log, monitor_clicks, navigate_to_form, on_close, open_browser, run, run_in_loop, run_loop, save_and_close, setup_click_capture_with_iframe_support, start_async_loop, start_extracting, start_login, update_status, watch_new_frames
# RETURNS: run_in_loop
# THREAD_TARGETS: run_loop
# HOTKEYS: 
# TK_BINDS: 
# COMMAND_BINDS: 
# CLASSES: ClickCaptureGUI
# IO_READS: 
# IO_WRITES: json.dump(...)
# EXCEPTIONS: line 97: ['Exception'], line 190: ['Exception'], line 209: ['Exception'], line 234: ['Exception'], line 148: ['Exception'], line 174: ['all exceptions'], line 160: ['all exceptions']
# CALLGRAPH_ROOTS: __init__,create_widgets,log,update_status,start_async_loop,run_in_loop,start_login,goto_form,start_extracting,begin_monitoring_after_ready,setup_click_capture_with_iframe_support,monitor_clicks,open_browser,navigate_to_form,save_and_close,exit_without_saving,cleanup,run,on_close,run_loop
# STATE_VARS: FORM_URL,LOGIN_URL
# STATE_MACHINES_COUNT: 0
# STATE_TRANSITIONS_COUNT: 0
# INIT_SEQUENCE: 
# INTENT: Provides asynchronous operations for close operations.
# FUNCTION_INTENTS: __init__=Handles the target entities., begin_monitoring_after_ready=Orchestrates multiple operations., cleanup=Handles the target entities., create_widgets=Orchestrates multiple operations., exit_without_saving=Updates internal state., goto_form=Handles form., inject_into_all_frames=Iterates and processes items., log=Updates internal state., monitor_clicks=Iterates and builds collection., navigate_to_form=Orchestrates multiple operations., on_close=Updates internal state., open_browser=Orchestrates multiple operations., run=Handles the target entities., run_in_loop=Returns computed value., run_loop=Updates internal state., save_and_close=Saves data in JSON format., setup_click_capture_with_iframe_support=Iterates and processes items., start_async_loop=Creates and manages background threads., start_extracting=Handles extracting., start_login=Handles login., update_status=Handles status., watch_new_frames=Iterates and processes items.
# END MACHINE-READABLE DATA
# ════════════════════
#===============================================================================
#
# 📝 FUNCTION SIGNATURES:
#
# ClickCaptureGUI.__init__(self) -> None
#
# ClickCaptureGUI.create_widgets(self) -> None
#
# ClickCaptureGUI.exit_without_saving(self) -> None
#
# ClickCaptureGUI.goto_form(self) -> None
#
# ClickCaptureGUI.log(self, msg) -> None
#
# ClickCaptureGUI.on_close(self) -> None
#
# ClickCaptureGUI.run(self) -> None
#
# ClickCaptureGUI.run_in_loop(self, coro) -> None
#
# ClickCaptureGUI.save_and_close(self) -> None
#
# ClickCaptureGUI.start_async_loop(self) -> None
#
# ClickCaptureGUI.start_extracting(self) -> None
#
# ClickCaptureGUI.start_login(self) -> None
#
# ClickCaptureGUI.update_status(self, text, color = 'blue') -> None
#
#===============================================================================
#
# ⚡️ THREADING MODEL (CRITICAL)
#
# Threads Found:
#   - run_loop()
#
#===============================================================================
#
# ⚙️ THREAD INTERACTION MAP:
#
#   run_loop():
#     Reads: None
#     Writes: None
#
#===============================================================================
#
# 🧱 CLASSES FOUND:
#
#   ClickCaptureGUI (line 15):
#     - ClickCaptureGUI.__init__()
#     - ClickCaptureGUI.create_widgets()
#     - ClickCaptureGUI.log()
#     - ClickCaptureGUI.update_status()
#     - ClickCaptureGUI.start_async_loop()
#     - ClickCaptureGUI.run_in_loop()
#     - ClickCaptureGUI.start_login()
#     - ClickCaptureGUI.goto_form()
#     - ClickCaptureGUI.start_extracting()
#     - ClickCaptureGUI.save_and_close()
#     - ClickCaptureGUI.exit_without_saving()
#     - ClickCaptureGUI.run()
#     - ClickCaptureGUI.on_close()
#===============================================================================
#
# CRITICAL GLOBAL VARIABLES:
#
#===============================================================================
#
# 🧠 FUNCTION BEHAVIORAL SUMMARIES:
#
#
#===============================================================================
#
# FUNCTION CALL HIERARCHY (depth-limited):
#
# - __init__()
#
# - create_widgets()
#
# - log()
#
# - update_status()
#
# - start_async_loop()
#
# - run_in_loop()
#
# - start_login()
#
# - goto_form()
#
# - start_extracting()
#
# - begin_monitoring_after_ready()
#
# - setup_click_capture_with_iframe_support()
#
# - monitor_clicks()
#
# - open_browser()
#
# - navigate_to_form()
#
# - save_and_close()
#
# - exit_without_saving()
#
# - cleanup()
#
# - run()
#
# - on_close()
#
# - run_loop()
#
#===============================================================================
#
# 🔄 STATE MACHINES:
#
#   (No state machines detected.)
#
#===============================================================================
#
# 🔌 EXTERNAL I/O SUMMARY:
#
#   Writes: json.dump(...)
#===============================================================================
#
# 📊 DATA FLOW SUMMARY:
#
#   __init__() — calls self.create_widgets, self.start_async_loop, self.window.geometry, self.window.title, tk.Tk; no return value
#   create_widgets() — calls btn_frame.pack, pack, scrolledtext.ScrolledText, self.done_btn.pack, self.exit_btn.pack, self.extract_btn.pack; no return value
#   log() — calls datetime.now, self.log_text.insert, self.log_text.see, strftime; no return value
#   update_status() — calls self.status_label.config; no return value
#   start_async_loop() — calls asyncio.new_event_loop, asyncio.set_event_loop, self.loop.run_forever, self.thread.start, threading.Thread; no return value
#   run_loop() — calls asyncio.new_event_loop, asyncio.set_event_loop, self.loop.run_forever; no return value
#   run_in_loop() — calls asyncio.run_coroutine_threadsafe; returns value
#   start_login() — calls self.login_btn.config, self.open_browser, self.run_in_loop, self.update_status; no return value
#   goto_form() — calls self.form_btn.config, self.navigate_to_form, self.run_in_loop; no return value
#   start_extracting() — calls self.begin_monitoring_after_ready, self.extract_btn.config, self.run_in_loop; no return value
#   begin_monitoring_after_ready() — calls asyncio.create_task, self.done_btn.config, self.log, self.monitor_clicks, self.setup_click_capture_with_iframe_support, self.update_status; no return value
#   setup_click_capture_with_iframe_support() — calls asyncio.create_task, asyncio.sleep, f.evaluate, inject_into_all_frames, self.log, self.page.evaluate; no return value
#   inject_into_all_frames() — calls f.evaluate, self.log; no return value
#   watch_new_frames() — calls asyncio.sleep, f.evaluate, self.log; no return value
#   monitor_clicks() — calls asyncio.sleep, datetime.now, frame.evaluate, isoformat, self.captures.append, self.log; no return value
#   open_browser() — reads LOGIN_URL; calls async_playwright, os.makedirs, print, self.context.new_page, self.form_btn.config, self.log; no return value
#   navigate_to_form() — reads FORM_URL; calls self.extract_btn.config, self.form_btn.config, self.log, self.page.goto, self.page.wait_for_load_state; no return value
#   save_and_close() — calls datetime.now, json.dump, len, open, self.cleanup, self.log; no return value
#   exit_without_saving() — calls self.cleanup, self.run_in_loop, self.window.destroy; no return value
#   cleanup() — calls print, self.context.close, self.playwright.stop; no return value
#   run() — calls self.window.mainloop, self.window.protocol; no return value
#   on_close() — calls self.loop.call_soon_threadsafe, self.window.destroy; no return value
#===============================================================================
#
# 🔧 MODULARIZATION RECOMMENDATIONS:
#
# ⚠️ THREADING: Multiple threads access shared state.
#    1. Keep thread functions with their state variables
#    2. Add proper locking if splitting state
#    3. Ensure thread-safe access to shared resources
#
# ⚠️ GLOBAL STATE: Significant global variables found.
#    1. Create a State class to hold all globals
#    2. Pass state object instead of using globals
#    3. Use getter/setter methods for thread-safe access
#
# When modularizing, consider splitting by:
#   - Separate state management from business logic
#   - Group related functions into modules
#   - Separate UI code from core logic
#===============================================================================
#===============================================================================
# 📞 FUNCTION CALL HIERARCHY:
#   (No intra-module function calls detected.)
#===============================================================================
# 🔄 STATE MACHINE TRANSITIONS:
#   (No *_state transitions detected.)
#===============================================================================
# ⌨️ HOTKEY BINDINGS:
#   (No keyboard hotkeys detected.)
#===============================================================================
#
# 🧩 MODULE INTEGRATION INTENT:
#   Role: Single-file code analyzer that injects a synopsis header
#   Used by: (future) system_synopsis_builder.py for folder-wide Markdown
#   Inputs: Python source file path
#   Outputs: Annotated source file (prepends this synopsis)
#===============================================================================
#
# 📝 INSTRUCTIONS FOR AI:
#   1. Preserve ALL global variable dependencies shown above
#   2. Maintain thread safety for variables accessed by multiple threads
#   3. Do NOT rename variables unless explicitly asked
#   4. Ensure all function dependencies are preserved
#   5. Keep UI-threaded calls (e.g., tk.after) on main thread or marshal via queue
#   6. Ensure hotkeys and binds still invoke the same callbacks
#===============================================================================
# === END SYNOPSIS HEADER ===
# === END SYNOPSIS HEADER ===
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
            shared_browser_data = r"C:\Users\chase\Documents\Shared-Browser-Data"
            os.makedirs(shared_browser_data, exist_ok=True)
            print("✅ Using shared browser data from:", shared_browser_data)
            self.playwright = await async_playwright().start()
            self.context = await self.playwright.chromium.launch_persistent_context(
                shared_browser_data, headless=False,
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
