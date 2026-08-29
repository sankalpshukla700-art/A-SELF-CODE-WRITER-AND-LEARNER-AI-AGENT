import json
import os
import sys
import io
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from google import genai

# Page Configuration
st.set_page_config(
    page_title="GALILEAN ",
    page_icon="📈",
    layout="wide"
)

MEMORY_FILE = "agent_memory.json"


# --- Memory Helper Functions ---
def load_memory() -> list:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_memory(reflections: list):
    with open(MEMORY_FILE, "w") as f:
        json.dump(reflections, f, indent=2)


def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)


# --- Enhanced Execution Sandbox with Plot Interception ---
def execute_python_code(code: str) -> tuple[bool, str, list]:
    """
    Executes Python code safely, capturing stdout/stderr and intercepting
    Matplotlib figures and Plotly chart objects.
    Returns: (success_status, text_output, list_of_figures)
    """
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = buffer_out = io.StringIO()
    sys.stderr = buffer_err = io.StringIO()

    # Close previous matplotlib figures to prevent overlap
    plt.close('all')

    success = True
    output = ""
    captured_figures = []

    try:
        exec_globals = {
            'plt': plt,
            'go': go
        }
        exec(code, exec_globals)
        output = buffer_out.getvalue()

        # 1. Capture any active Matplotlib figures
        if plt.get_fignums():
            for fig_num in plt.get_fignums():
                captured_figures.append(("matplotlib", plt.figure(fig_num)))

        # 2. Capture explicit Plotly figures saved in variables
        for val in exec_globals.values():
            if isinstance(val, (go.Figure,)):
                captured_figures.append(("plotly", val))

    except Exception as e:
        success = False
        output = f"{type(e).__name__}: {str(e)}\n{buffer_err.getvalue()}"
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

    return success, output.strip(), captured_figures


# --- LLM Functions ---
def generate_code_attempt(client, task: str, memory: list, retry_context: str = "") -> str:
    memory_str = "\n".join([f"- {m}" for m in memory]) if memory else "None yet."

    prompt = f"""You are a Python data visualization and coding agent.
Task: {task}

=== PAST LESSONS LEARNED (from previous mistakes) ===
{memory_str}

=== CURRENT RETRY CONTEXT ===
{retry_context if retry_context else "First attempt."}

Instructions:
1. Write valid Python code to complete the task.
2. If the task calls for a chart/plot, use Matplotlib (`import matplotlib.pyplot as plt`) or Plotly (`import plotly.graph_objects as go` / `import plotly.express as px`).
3. For Matplotlib, build the plot using `plt.figure()` or `plt.plot()`. Do NOT call `plt.show()`.
4. For Plotly, assign the figure to a variable named `fig` (e.g. `fig = px.scatter(...)`).
5. Output ONLY raw Python code inside a ```python ``` block.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    text = response.text.strip()
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text


def reflect_on_error(client, task: str, failed_code: str, error_message: str) -> str:
    prompt = f"""Analyze why the following Python plot/code generation failed for task: "{task}"

Failed Code:
{failed_code}

Error Stack Trace:
{error_message}

Instruction: Write a concise, one-sentence "Lesson Learned" rule to prevent this mistake in the future.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text.strip()


# --- Streamlit GUI Dashboard ---
st.title("📊GALILEAN* ")
st.markdown(
    "This agent writes code, captures errors, self-corrects, and renders **Matplotlib** & **Plotly** visualizations dynamically.")

# Sidebar - API Key Input & Memory Viewer
with st.sidebar:
    st.header("🔑 Credentials")
    api_key_input = st.text_input(
        "Enter Gemini API Key:",
        value="ENTER OR PASTE KEY HERE",  # <--- Pasted here as default value
        type="password",
        help="Paste your AI Studio key here if not set in environment."
    )

    st.header("🧠 Agent Memory (Lessons)")
    current_memory = load_memory()
    st.metric(label="Stored Lessons", value=len(current_memory))

    if current_memory:
        for idx, lesson in enumerate(reversed(current_memory), start=1):
            st.info(f"**Lesson {len(current_memory) - idx + 1}:** {lesson}")
    else:
        st.write("No memories stored yet.")

    if st.button("🗑️ Clear Agent Memory", type="secondary"):
        clear_memory()
        st.rerun()

# Main Interface
sample_plotting_prompt = (
    "Generate sample sales data for 4 quarters across 3 regions (North, South, East). "
    "Create an interactive Plotly grouped bar chart showing sales by region per quarter, "
    "and calculate total overall sales in terminal output."
)

task_input = st.text_area(
    "Enter a Python Task (Data Viz / Plotting supported):",
    height=100,
    value=sample_plotting_prompt
)

max_attempts = st.slider("Max Retries per Run", min_value=1, max_value=5, value=3)

if st.button("🚀 Run Agent", type="primary"):
    # Priority: 1. Environment Variable, 2. Sidebar Text Input Box
    api_key = os.environ.get("GEMINI_API_KEY") or api_key_input

    if not api_key:
        st.error("Missing API Key! Please enter your Gemini API Key in the left sidebar.")
        st.stop()

    # Initialize Google GenAI client with explicit API Key
    client = genai.Client(api_key=api_key)

    memory = load_memory()
    retry_context = ""

    status_box = st.status("Agent Execution Started...", expanded=True)

    for attempt in range(1, max_attempts + 1):
        status_box.update(label=f"Attempt {attempt}/{max_attempts} in progress...", state="running")
        st.subheader(f"🔄 Attempt {attempt}")

        # 1. Code Generation
        with st.spinner("Generating code & plot..."):
            code = generate_code_attempt(client, task_input, memory, retry_context)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Generated Code:**")
            st.code(code, language="python")

        # 2. Execution & Chart Capture
        success, output, figures = execute_python_code(code)

        with col2:
            st.markdown("**Execution Output:**")
            if success:
                st.success("Execution Successful!")
                if output:
                    st.code(output, language="text")

                # Render Captured Plots
                if figures:
                    st.markdown("**Rendered Visualizations:**")
                    for fig_type, fig_obj in figures:
                        if fig_type == "matplotlib":
                            st.pyplot(fig_obj)
                        elif fig_type == "plotly":
                            st.plotly_chart(fig_obj, use_container_width=True)
                elif not output:
                    st.info("[Code executed with no stdout output or figures]")

                status_box.update(label=f"Task Completed Successfully on Attempt {attempt}!", state="complete")
                break
            else:
                st.error("Runtime Failure!")
                st.code(output, language="text")

        # 3. Reflection & Memory Update
        if not success:
            with st.spinner("Reflecting on plotting error..."):
                lesson = reflect_on_error(client, task_input, code, output)
                memory.append(lesson)
                save_memory(memory)
                retry_context = f"Attempt {attempt} failed with error:\n{output}\nLesson extracted: {lesson}"

            st.warning(f"**Self-Reflection Lesson:** {lesson}")
            st.divider()

    else:
        status_box.update(label="Agent failed to resolve task within maximum attempts.", state="error")
