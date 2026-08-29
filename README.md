# 🤖 A-SELF-CODE-WRITER-AND-LEARNER-AI-AGENT

> An autonomous Python AI agent that generates code, executes it, detects errors, learns from failures, and retries with improved solutions.

## 📌 Overview

**A-SELF-CODE-WRITER-AND-LEARNER-AI-AGENT**, also presented through the **GALILEAN** Streamlit dashboard, is an AI-powered coding agent built with **Python** and **Streamlit**.

The agent accepts a user-defined programming or data visualization task and performs an autonomous workflow:

**Generate Code → Execute Code → Detect Errors → Reflect → Learn → Retry**

The agent uses the **Google Gemini API** for intelligent code generation and self-reflection. When generated code fails, the agent analyzes the error, extracts a lesson from the failure, stores it in persistent memory, and uses that knowledge during future attempts.

---

# ✨ Features

* 🤖 **AI-Powered Python Code Generation**
* 🧠 **Persistent Agent Memory**
* 🔄 **Automatic Error Detection and Retry**
* 💡 **Self-Reflection and Lesson Learning**
* 📊 **Matplotlib Visualization Support**
* 📈 **Interactive Plotly Visualization Support**
* 🖥️ **Streamlit Web Dashboard**
* 📝 **Real-Time Generated Code Display**
* ⚠️ **Runtime Error Capture**
* 🔢 **Configurable Maximum Retry Attempts**
* 🗑️ **Memory Management and Clear Memory Option**

---

# 🧠 How the AI Agent Works

The system follows a self-learning agent architecture.

```text
              ┌─────────────────────┐
              │    User Task Input  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  Gemini AI Model    │
              │  Generates Python   │
              │       Code          │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Code Execution    │
              │      Sandbox        │
              └──────────┬──────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       ┌──────────────┐      ┌──────────────┐
       │   Success    │      │    Error     │
       └──────┬───────┘      └──────┬───────┘
              │                     │
              ▼                     ▼
       ┌──────────────┐      ┌────────────────┐
       │ Render Output│      │ Self-Reflection│
       │ & Charts     │      └────────┬───────┘
       └──────────────┘               │
                                      ▼
                             ┌────────────────┐
                             │ Store Lesson   │
                             │ in Memory      │
                             └────────┬───────┘
                                      │
                                      ▼
                              Retry Improved
                                   Code
```

---

# 🛠️ Technology Stack

| Technology           | Purpose                           |
| -------------------- | --------------------------------- |
| 🐍 Python            | Core programming language         |
| 🌐 Streamlit         | Interactive web dashboard         |
| 🤖 Google Gemini API | AI code generation and reflection |
| 📊 Matplotlib        | Static data visualization         |
| 📈 Plotly            | Interactive visualizations        |
| 🧠 JSON              | Persistent agent memory storage   |
| ⚙️ OS & SYS          | System and execution handling     |
| 📥 IO                | Output and error capturing        |

---

# 📂 Project Structure

```text
A-SELF-CODE-WRITER-AND-LEARNER-AI-AGENT/
│
├── app.py
│
├── agent_memory.json
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

### File Description

| File                | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `app.py`            | Main Streamlit application                                   |
| `agent_memory.json` | Stores lessons learned from previous errors                  |
| `requirements.txt`  | Required Python dependencies                                 |
| `README.md`         | Project documentation                                        |
| `.gitignore`        | Prevents sensitive and unnecessary files from being uploaded |

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/A-SELF-CODE-WRITER-AND-LEARNER-AI-AGENT.git
```

Navigate to the project directory:

```bash
cd A-SELF-CODE-WRITER-AND-LEARNER-AI-AGENT
```

---

## 2️⃣ Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit matplotlib plotly google-genai
```

---

# 🔑 Gemini API Configuration

This project requires a **Google Gemini API Key**.

You can provide your API key in two ways.

## Option 1: Environment Variable

### macOS / Linux

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

---

## Option 2: Streamlit Dashboard

Enter your Gemini API key directly in the sidebar under:

```text
🔑 Credentials
```

> ⚠️ **Security Warning:** Never upload your API key to GitHub.

---

# ▶️ Run the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

# 🖥️ Dashboard Features

The GALILEAN dashboard provides an easy-to-use interface for interacting with the AI agent.

## 🔑 Credentials Panel

The sidebar allows users to enter their Gemini API key securely.

The application checks:

```text
1. GEMINI_API_KEY Environment Variable
                ↓
2. Streamlit Sidebar Input
```

---

## 🧠 Agent Memory

The AI agent stores lessons learned from previous execution failures.

Example:

```text
Lesson Learned:
Always import required libraries before using their functions.
```

These lessons are stored in:

```text
agent_memory.json
```

During future code generation attempts, the agent receives previous lessons as context.

---

## 📝 Task Input

Users can enter Python programming or visualization tasks.

Example:

```text
Generate sample sales data for four quarters across three regions.
Create an interactive Plotly grouped bar chart and calculate
the total overall sales.
```

---

## 🔄 Retry Configuration

The user can select the maximum number of attempts.

```text
Minimum: 1
Maximum: 5
Default: 3
```

If the code fails, the agent:

1. Detects the runtime error.
2. Sends the error and failed code to Gemini.
3. Generates a concise lesson.
4. Saves the lesson in memory.
5. Retries the task using the learned information.

---

# 🧩 Core Components

## 🧠 Memory Management

The project includes helper functions for persistent learning.

### Load Memory

```python
load_memory()
```

Loads previously stored lessons from:

```text
agent_memory.json
```

---

### Save Memory

```python
save_memory(reflections)
```

Stores newly generated lessons in JSON format.

---

### Clear Memory

```python
clear_memory()
```

Deletes all previously stored lessons.

---

# ⚡ Code Execution Engine

The function:

```python
execute_python_code()
```

executes AI-generated Python code and captures:

* Standard output
* Standard errors
* Runtime exceptions
* Matplotlib figures
* Plotly figures

The execution function returns:

```python
(
    success_status,
    text_output,
    captured_figures
)
```

---

# 📊 Visualization Support

## Matplotlib

The agent can generate static charts using:

```python
import matplotlib.pyplot as plt
```

Example supported charts:

* Line Charts
* Bar Charts
* Scatter Plots
* Histograms
* Pie Charts

---

## Plotly

The agent can also generate interactive charts.

Example:

```python
import plotly.graph_objects as go
```

Supported visualizations include:

* Interactive Bar Charts
* Scatter Charts
* Line Charts
* Pie Charts
* Dashboard Visualizations

For Plotly generation, the AI agent is instructed to store the chart in:

```python
fig
```

Example:

```python
fig = go.Figure()
```

The application automatically detects and renders the figure.

---

# 🤖 Self-Learning Mechanism

The most important feature of this project is the **reflection-based learning system**.

When generated code fails:

```text
Generated Code
      ↓
Code Execution
      ↓
Error Detected
      ↓
Gemini Analyzes Failure
      ↓
Lesson Generated
      ↓
Lesson Saved to Memory
      ↓
Agent Retries
```

Example failure:

```text
NameError: name 'pd' is not defined
```

Possible learned lesson:

```text
Always import pandas as pd before using pandas functions.
```

This lesson is stored and supplied to the AI during future attempts.

---

# 📋 Example Workflow

### User Task

```text
Create a bar chart showing monthly sales data.
```

### Attempt 1

The AI generates Python code.

```text
Execution Started
```

### Runtime Failure

```text
NameError: name 'plt' is not defined
```

### Self-Reflection

The AI analyzes the error and generates:

```text
Lesson Learned:
Always import matplotlib.pyplot as plt before using plotting functions.
```

### Attempt 2

The lesson is included in the next prompt.

The AI generates improved code.

```text
Execution Successful!
```

### Result

The dashboard displays:

* Generated Python Code
* Terminal Output
* Matplotlib Chart or Plotly Visualization
* Learned Memory

---

# 🧠 Agent Prompt Strategy

The AI is instructed to:

1. Generate valid Python code.
2. Follow the user's requested task.
3. Use Matplotlib or Plotly for visualization tasks.
4. Avoid calling `plt.show()`.
5. Store Plotly figures in a variable named `fig`.
6. Return clean Python code.
7. Consider lessons learned from previous failures.

This makes the agent capable of improving its execution strategy over multiple attempts.

---

# 📦 requirements.txt

Create a `requirements.txt` file with:

```txt
streamlit
matplotlib
plotly
google-genai
```

Install using:

```bash
pip install -r requirements.txt
```

---

# 🔒 Recommended .gitignore

Use the following `.gitignore`:

```gitignore
# API Keys
.env
secrets.toml

# Python
__pycache__/
*.py[cod]
venv/
env/

# Agent Memory
agent_memory.json

# Streamlit
.streamlit/secrets.toml

# macOS
.DS_Store
```

> It is recommended to avoid uploading `agent_memory.json` if it may contain sensitive prompts or generated information.

---

# 🚀 Future Improvements

Possible future enhancements include:

* 🔐 Secure execution sandbox using Docker
* 🐳 Containerized code execution
* 📚 Vector database-based long-term memory
* 🧠 Semantic lesson retrieval
* 🔍 Automatic code quality analysis
* 🛡️ Security filtering for generated code
* 🧪 Automated test generation
* 📊 More visualization libraries
* 💾 Database-backed memory
* 🔄 Multi-agent collaboration
* 🖥️ Enhanced execution logs
* 📈 Agent performance analytics
* 🌐 Deployment on Streamlit Cloud

---

# ⚠️ Security Notice

This project uses Python's:

```python
exec()
```

to execute AI-generated code.

**Running arbitrary AI-generated code can be dangerous.**

The current execution mechanism should be considered suitable for:

* Educational purposes
* Local experimentation
* Controlled development environments

It is **not recommended** to expose unrestricted code execution publicly.

For production use, consider implementing:

* Docker containers
* Resource limits
* Restricted file system access
* Network isolation
* Process isolation
* Execution timeouts
* Allowlisted Python modules

---

# 🎯 Use Cases

This project can be used for:

* 🤖 Autonomous AI Coding Agents
* 📊 AI Data Visualization
* 🧠 Self-Improving AI Systems
* 🎓 AI and Python Learning
* 🧪 Automated Code Experimentation
* 🔄 Error Correction Research
* 💻 Streamlit AI Applications

---

# 🏗️ Architecture

```text
                 ┌───────────────────┐
                 │   Streamlit UI    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │    User Prompt    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   Gemini API      │
                 │ Code Generation   │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Python Execution  │
                 │      Engine       │
                 └─────────┬─────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                  Success        Error
                    │             │
                    ▼             ▼
              ┌──────────┐  ┌──────────────┐
              │ Visualize│  │ Self-Reflect │
              └──────────┘  └──────┬───────┘
                                   │
                                   ▼
                            ┌──────────────┐
                            │ JSON Memory  │
                            └──────┬───────┘
                                   │
                                   ▼
                              Retry Agent
```

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

```bash
# Fork the repository

# Create a new branch
git checkout -b feature/new-feature

# Make your changes

# Commit changes
git commit -m "Add new feature"

# Push changes
git push origin feature/new-feature
```

Then create a Pull Request.

---

# 📄 License

This project is intended for educational and research purposes.

You can add an MIT License to make the project open source.

---

# 👨‍💻 Author

**Sankalp Shukla**

B.Tech Computer Science & Engineering
AI/ML Enthusiast | Python Developer | AI Projects

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps support the development of more AI and automation projects.

---

## 🔥 Project Motto

> **"Write. Execute. Fail. Learn. Improve. Repeat."**

---

### Made with ❤️ using Python, Streamlit, Matplotlib, Plotly, and Generative AI.
