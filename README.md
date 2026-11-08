# Exora Desktop Agent

> An autonomous desktop-automation agent built on **Google ADK**. Give it a task in plain English; it plans, operates your browser, files, and spreadsheets, recovers from errors, and **verifies the result before claiming success**.

[![CI](https://github.com/<your-username>/exora-desktop-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/exora-desktop-agent/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture and Flow](#architecture-and-flow)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Run with Docker](#run-with-docker)
- [Safety Model](#safety-model)
- [Testing](#testing)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Exora** takes instructions such as *"Find report_draft.txt in Downloads, rename it and move it to Documents/Archive"* and completes them autonomously using tools for the browser (Playwright), file system, `.xlsx` spreadsheets, and optionally, mouse/keyboard control (PyAutoGUI). It works with any LLM supported by [LiteLLM](https://docs.litellm.ai/) (Groq, OpenAI, Anthropic, Ollama, etc.) or Gemini natively.

---

## Features

- **Plan → Act → Observe → Verify → Decide Loop:** Operates with a live, visible execution plan.
- **Strict Verification:** Enforced in code—the agent cannot finish with `success=true` unless a verification step runs after its last action.
- **Human Approval Gate:** Form submissions and high-impact actions are blocked until manually approved in the UI.
- **Error Recovery:** Handles retries, click fallbacks, popups, dialogs, slow-page tolerance, loop detection, and automatic re-planning.
- **Sandboxed File Access:** Restricts file access strictly to user-allowed directories, with no file deletion tools available.
- **Streamlit UI & CLI:** Includes interactive controls (Start/Stop, live logs, plan viewer, status, counters) alongside a command-line interface.
- **Provider-Safe Messages:** Built-in sanitizer strips non-standard or provider-rejected fields (such as `reasoning_content`) before sending requests.

---

## Architecture and Flow

```mermaid
flowchart TD
    U[User task in Streamlit UI / CLI] --> R[AgentTaskController]
    R --> A[Google ADK LlmAgent]
    A -->|plan| P[set_plan]
    A -->|act| T{Tools}
    T --> B[Browser: Playwright]
    T --> F[Files: search, rename, move]
    T --> S[Spreadsheets: openpyxl]
    T --> D[Desktop: PyAutoGUI]
    T --> O[Observe / verify tools]
    O --> V{Verified?}
    V -- no --> A
    V -- yes --> C[declare_task_complete]
    B -. submit click .-> G[Approval gate]
    G -->|user approves| B
    C --> UI[Status + evidence in UI]# exora-desktop-agent
