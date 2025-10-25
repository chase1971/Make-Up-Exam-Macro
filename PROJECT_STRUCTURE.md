# 🧩 PROJECT STRUCTURE SUMMARY
**Generated:** 2025-10-25 15:30:12

## 🚀 APPLICATION OVERVIEW

### Purpose
This application is designed to: Provides asynchronous operations. Updates various components.

**Key Capabilities:**
- Provides asynchronous operations for close operations.

### Key Components

### Architecture Summary
- **Total Modules**: 3
- **Total Functions**: 32
- **Total Classes**: 2

### Key Features
- Assignment Date Automation
- D2L Course Management
- Data Extraction

### 📄 Project Structure & Examples
**Example Module: `example.py`**
*Purpose: Provides asynchronous operations. Updates various components.*

**Key Functions:**
- `__init__`
- `automate_form`
- `load_csv_data`

**Function Signatures:**
```python
WebAutomationAgent.__init__(self) -> None
WebAutomationAgent.load_csv_data(self) -> None
WebAutomationAgent.log(self, message) -> None
WebAutomationAgent.open_email_template(self, class_code, exam_date) -> None
WebAutomationAgent.run_automation(self, exam_file_path) -> None
```

**Project Statistics:**
- **Total Modules**: 3
- **Total Functions**: 32
- **Total Classes**: 2

---

## 🚪 ENTRY POINTS

### Utility Scripts
- **`automation_agent.py`**: Provides asynchronous operations. Updates various components.
- **`html extractor.py`**: Provides asynchronous operations for close operations.

### Execution Flow
1. **Start**: Run the main application
2. **Initialization**: Load configuration and dependencies
3. **Processing**: Execute core functionality
4. **Output**: Generate results or complete tasks

### Command Line Usage
```bash
# Run the application
python <main_script.py>
```

---

## 🔄 SHARED STATE TABLE

| File | Variable | Modified By | Read By |
|------|----------|-------------|---------|

---

This document provides a full architectural map of the project.

## 🧱 Module Dependency Graph

```mermaid
graph TD
```

## 🔄 Cross-Module Data Flow Map

| Source Module | Target or Description |
|----------------|----------------------|
| automation_agent.py | Functions: __init__, automate_form, load_csv_data, log, open_email_template, run_automation, run_loop, select_student, start_async_loop, update_status |
| html extractor.py | Functions: __init__, begin_monitoring_after_ready, cleanup, create_widgets, exit_without_saving, goto_form, inject_into_all_frames, log, monitor_clicks, navigate_to_form, on_close, open_browser, run, run_in_loop... |

## 📦 Module Summaries

### `automation_agent.py`

**Intent:** Provides asynchronous operations. Updates various components.

**Classes:** WebAutomationAgent

**Functions:** __init__, automate_form, load_csv_data, log, open_email_template, run_automation, run_loop, select_student, start_async_loop, update_status

**Globals:** agent, exam_file_path, result, success


**Local Imports:** _None_

**External Imports:** asyncio, csv, datetime, difflib, docx, io, json, os, pathlib, playwright.async_api, shutil, subprocess, sys, tempfile, threading, traceback


#### 📝 Function Signatures

- `WebAutomationAgent.__init__(self) -> None`

- `WebAutomationAgent.load_csv_data(self) -> None`

- `WebAutomationAgent.log(self, message) -> None`

- `WebAutomationAgent.open_email_template(self, class_code, exam_date) -> None`

- `WebAutomationAgent.run_automation(self, exam_file_path) -> None`

- `WebAutomationAgent.start_async_loop(self) -> None`

- `WebAutomationAgent.update_status(self, text, color = 'blue') -> None`


#### 🎯 Function Intents

- **__init__()**: Handles the target entities.

- **automate_form()**: Performs mathematical calculations.

- **load_csv_data()**: Checks file or directory existence.

- **log()**: Handles the target entities.

- **open_email_template()**: Open the appropriate email template and replace the date.

- **run_automation()**: Orchestrates multiple operations.

- **run_loop()**: Updates internal state.

- **select_student()**: Iterates and processes items.

- **start_async_loop()**: Creates and manages background threads.

- **update_status()**: Handles status.


#### File I/O Summary

- Reads: unknown

- Writes: _None_


#### Threading & UI Bindings

- Threads: run_loop

- UI Binds: _None_


#### Exception Paths

line 784: ['Exception'], line 88: ['Exception'], line 194: ['Exception'], line 376: ['Exception'], line 736: ['Exception'], line 404: ['Exception'], line 762: ['Exception'], line 164: ['all exceptions'], line 640: ['Exception'], line 562: ['Exception']


---

### `html extractor.py`

**Intent:** Provides asynchronous operations for close operations.

**Classes:** ClickCaptureGUI

**Functions:** __init__, begin_monitoring_after_ready, cleanup, create_widgets, exit_without_saving, goto_form, inject_into_all_frames, log, monitor_clicks, navigate_to_form, on_close, open_browser, run, run_in_loop, run_loop, save_and_close, setup_click_capture_with_iframe_support, start_async_loop, start_extracting, start_login, update_status, watch_new_frames

**Globals:** FORM_URL, LOGIN_URL, app


**Local Imports:** _None_

**External Imports:** asyncio, datetime, json, os, playwright.async_api, threading, tkinter


#### 📝 Function Signatures

- `ClickCaptureGUI.__init__(self) -> None`

- `ClickCaptureGUI.create_widgets(self) -> None`

- `ClickCaptureGUI.exit_without_saving(self) -> None`

- `ClickCaptureGUI.goto_form(self) -> None`

- `ClickCaptureGUI.log(self, msg) -> None`

- `ClickCaptureGUI.on_close(self) -> None`

- `ClickCaptureGUI.run(self) -> None`

- `ClickCaptureGUI.run_in_loop(self, coro) -> None`

- `ClickCaptureGUI.save_and_close(self) -> None`

- `ClickCaptureGUI.start_async_loop(self) -> None`

- `ClickCaptureGUI.start_extracting(self) -> None`

- `ClickCaptureGUI.start_login(self) -> None`

- `ClickCaptureGUI.update_status(self, text, color = 'blue') -> None`


#### 🎯 Function Intents

- **__init__()**: Handles the target entities.

- **begin_monitoring_after_ready()**: Orchestrates multiple operations.

- **cleanup()**: Handles the target entities.

- **create_widgets()**: Orchestrates multiple operations.

- **exit_without_saving()**: Updates internal state.

- **goto_form()**: Handles form.

- **inject_into_all_frames()**: Iterates and processes items.

- **log()**: Updates internal state.

- **monitor_clicks()**: Iterates and builds collection.

- **navigate_to_form()**: Orchestrates multiple operations.

- **on_close()**: Updates internal state.

- **open_browser()**: Orchestrates multiple operations.

- **run()**: Handles the target entities.

- **run_in_loop()**: Returns computed value.

- **run_loop()**: Updates internal state.

- **save_and_close()**: Saves data in JSON format.

- **setup_click_capture_with_iframe_support()**: Iterates and processes items.

- **start_async_loop()**: Creates and manages background threads.

- **start_extracting()**: Handles extracting.

- **start_login()**: Handles login.

- **update_status()**: Handles status.

- **watch_new_frames()**: Iterates and processes items.


#### File I/O Summary

- Reads: _None_

- Writes: json.dump(...)


#### Threading & UI Bindings

- Threads: run_loop

- UI Binds: _None_


#### Exception Paths

line 96: ['Exception'], line 189: ['Exception'], line 208: ['Exception'], line 233: ['Exception'], line 147: ['Exception'], line 173: ['all exceptions'], line 159: ['all exceptions']


---

### `agent.py`

**Classes:** _None_

**Functions:** _None_

**Globals:** _None_


**Local Imports:** _None_

**External Imports:** _None_


#### 📝 Function Signatures

_No function signatures available._


#### 🎯 Function Intents

_No function intents available._


#### File I/O Summary

- Reads: _None_

- Writes: _None_


#### Threading & UI Bindings

- Threads: _None_

- UI Binds: _None_


#### Exception Paths

_No exception handlers detected._


---

## 🧠 DATA SCHEMA SUMMARY

```json
{
  "ModuleSummary": {
    "file": "str",
    "classes": ["list[str]"],
    "functions": ["list[str]"],
    "globals": ["list[str]"],
    "imports_local": ["list[str]"],
    "imports_external": ["list[str]"],
    "io_reads": ["list[str]"],
    "io_writes": ["list[str]"],
    "threads": ["list[str]"],
    "ui_binds": ["list[str]"],
    "exceptions": ["list[str]"],
    "intent": "str",
    "function_signatures": ["list[str]"],
    "function_intents": "str"
  }
}
```
