import json

txt = '''## Project Flow

### Chapter 1: Project Setup

1. **Step 1: Create a virtual environment**
   - Create a new directory for the project and navigate into it.
   - Run `python -m venv venv` to create a new virtual environment named `venv`.
   - Activate the virtual environment using `source venv/bin/activate` on Linux/Mac or `venv\Scripts\activate` on Windows.

2. **Step 2: Install dependencies**
   - Install the required dependencies using pip: `pip install -r requirements.txt`
   - Create a `requirements.txt` file with the following content to specify the target Python version and dependencies:
     ```bash
python==3.8
module1
module2
```

3. **Step 3: Initialize the project structure**
   - Create a new file `main.py` to serve as the entry point of the project.
   - Create a new directory `src` to hold the project's source code.
   - Create a new directory `tests` to hold the project's unit tests.

### Chapter 2: Develop Feature X

1. **Step 1: Design the user interface**
   - Create a new file `ui.py` in the `src` directory to handle user interface logic.
   - Implement the user interface design in `ui.py`.

2. **Step 2: Implement the backend logic**
   - Create a new file `backend.py` in the `src` directory to handle backend logic.
   - Implement the backend logic in `backend.py`.

3. **Step 3: Write unit tests**
   - Create a new file `test_ui.py` in the `tests` directory to hold unit tests for the user interface.
   - Create a new file `test_backend.py` in the `tests` directory to hold unit tests for the backend logic.
   - Implement unit tests for the user interface and backend logic in `test_ui.py` and `test_backend.py` respectively.

## Code to Install Dependencies
```bash
pip install -r requirements.txt
```
No Python code block found in the response.

## Project Flow:

### Chapter 1: Project Setup

1. **Step 1: Create a virtual environment**
   - Create a new directory for the project and navigate into it.
   - Run `python -m venv venv` to create a new virtual environment named `venv`.
   - Activate the virtual environment using `source venv/bin/activate` on Linux/Mac or `venv\Scripts\activate` on Windows.

2. **Step 2: Install dependencies**
   - Install the required dependencies using pip: `pip install -r requirements.txt`
   - Create a `requirements.txt` file with the following content to specify the target Python version and dependencies:
     ```bash
python==3.8
module1
module2
```

3. **Step 3: Initialize the project structure**
   - Create a new file `main.py` to serve as the entry point of the project.
   - Create a new directory `src` to hold the project's source code.
   - Create a new directory `tests` to hold the project's unit tests.

### Chapter 2: Develop Feature X

1. **Step 1: Design the user interface**
   - Create a new file `ui.py` in the `src` directory to handle user interface logic.
   - Implement the user interface design in `ui.py`.

2. **Step 2: Implement the backend logic**
   - Create a new file `backend.py` in the `src` directory to handle backend logic.
   - Implement the backend logic in `backend.py`.

3. **Step 3: Write unit tests**
   - Create a new file `test_ui.py` in the `tests` directory to hold unit tests for the user interface.
   - Create a new file `test_backend.py` in the `tests` directory to hold unit tests for the backend logic.
   - Implement unit tests for the user interface and backend logic in `test_ui.py` and `test_backend.py` respectively.'''

import re
def parse_text_to_json(text):
    """Parses the refined flow from Markdown to a list of dictionaries and handles various heading levels."""
    chapters = []
    current_chapter = None
    current_step = None
    collecting_description = False

    # Regular expression patterns to match headings and steps
    chapter_pattern = re.compile(r'#+\s*Chapter\s*\d+')
    step_pattern = re.compile(r'\d+\.\s*\*\*Step\s*(\d+):\s*(.*)')
    description_pattern = re.compile(r'\s*-\s*(.*)')  # To capture bullet points after steps

    for line in text.splitlines():
        line = line.strip()

        # Match chapter headings starting with any number of '#' (e.g., '# Chapter', '## Chapter')
        if chapter_pattern.match(line):
            if current_chapter:
                chapters.append(current_chapter)  # Save the previous chapter
            # Extract the chapter title (allowing for flexible Markdown syntax)
            chapter_title = line.split(":", 1)[-1].strip()  # Extract title after 'Chapter X:'
            current_chapter = {"chapter_title": chapter_title, "steps": []}
            current_step = None  # Reset the current step when a new chapter starts
            collecting_description = False  # Stop collecting descriptions when a new chapter starts

        # Match steps
        elif step_pattern.match(line) and current_chapter:
            if current_step:
                current_chapter["steps"].append(current_step)  # Save the previous step
            # Extract the step number and initialize a new step
            match = step_pattern.match(line)
            step_number = match.group(1)
            step_title = match.group(2)
            current_step = {"step_number": step_number, "step_title": step_title, "details": {}}
            collecting_description = False  # Reset collecting descriptions

        # Match actionable descriptions or other bullet points under steps
        elif description_pattern.match(line):
            description = description_pattern.match(line).group(1).strip()
            if current_step:
                if collecting_description:
                    # Append to existing description (multi-line support)
                    current_step["details"]["Actionable Description"] += " " + description
                else:
                    current_step["details"]["Actionable Description"] = description
                    collecting_description = True

    # Append the last step and chapter if they exist
    if current_step and current_chapter:
        current_chapter["steps"].append(current_step)
    if current_chapter:
        chapters.append(current_chapter)

    # Return the parsed data as JSON
    return json.dumps(chapters, indent=4)

x = parse_text_to_json(txt)
print(x)
# from agents.tech_lead_agent2 import TechLeadAgent
# from model.sambanova import SambanovaAPI


# rough_project_flow = """
# # Project Setup
# * Install dependencies
# * Create project structure
# # Develop Feature X
# * Design UI
# * Implement backend
# * Write tests
# """

# tech_lead = TechLeadAgent()
# tech_lead.text_ai = SambanovaAPI(r"G:\ALL JARVIS\Anonymous-Agent\model\cookies.json", model="Meta-Llama-3.2-3B-Instruct")
# refined_flow = tech_lead.refine_project_flow(rough_project_flow)
# if refined_flow:
#     tech_lead.structure_and_save_flow(refined_flow)