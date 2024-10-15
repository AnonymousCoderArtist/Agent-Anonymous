import json
import re
class TechLeadAgent:
    def __init__(self):
        self.text_ai = None
        self.ai_prompt = '''
**Project Flow Refinement for Software Development**

**Objective:** Transform a rough project flow into a comprehensive and refined version specifically tailored for software development, ensuring clarity, accuracy, efficiency, and adherence to Agile principles.

**Input:** Provide a detailed and structured rough project flow in Markdown format. Each chapter should be separated by a Markdown heading, and each step should be described using bullet points.

**Format:**

# Chapter 1: Project Initialization

* **Step 1: Set up the Development Environment**
    * **Actionable Description:** Install and configure the necessary software tools (e.g., IDE, version control system, database) on the development machines.
* **Step 2: Create Project Repository**
    * **Actionable Description:** Initialize a Git repository for the project and add a basic README file outlining the project's purpose and structure.

# Chapter 2: Develop User Authentication Feature

* **Step 1: Design User Interface for Login and Registration** 
    * **Actionable Description:** Design the UI for the login and registration forms, including input fields, buttons, and error handling.

* **Step 2:  Implement Backend Logic for User Authentication**
    * **Actionable Description:** Develop the API endpoints for user registration, login, and logout using Node.js and Express. Implement secure password hashing.

**Requirements:**

* **Agile Principles:** Structure the project flow according to Agile principles, including iterative development, sprints, and user stories.
* **Descriptive Steps:** Each step should be descriptive and concise, providing clear instructions for an AI agent to execute.
* **Accuracy:** Ensure that the steps are accurate and reflect best practices in software development project management.
* **Efficiency:** Optimize the flow to minimize redundancy and maximize productivity.
* **Completeness:** Cover all essential phases of a software development project, including planning, development, testing, deployment, and maintenance.

**Note:** The project flow should be provided in Markdown format, with each chapter separated by a Markdown heading and each step described using bullet points. FOLLOW THE EXAMPLE FORMAT STRICTLY. DONT USE ANY GITHUB AND THERE ARE NOT ANY MODULES INSTALLED ALSO THERE IS NO REQUIREMENTS.TXT AND ALSO DONT TRY TO HOST ANYTHING. NO CODEBLOCK AND NO CODE TO BE WRITTEN BY YOU.

**STRICTLY FOLLOW THE ABOVE FORMAT AND NOTHING ELSE.**

ONLY RETURN THE PROJECT FLOW (Make sure its short and concise dont add much steps) AND NOTHING ELSE. HERE IS THE INPUT ROUGH PROJECT FLOW: 
'''

    def refine_project_flow(self, rough_project_flow):
        """Refines the rough project flow using the AI."""
        print("Entering Project flow refinement process...")
        prompt_with_flow = self.ai_prompt + "\n" + rough_project_flow 
        refined_flow_response = self.text_ai.chat(prompt_with_flow)
        if refined_flow_response:
            refined_flow = ''.join(refined_flow_response)
            print(refined_flow)
            return refined_flow
        else:
            print("No result received from the AI. Please check your input and try again.")
            return None

    def structure_and_save_flow(self, refined_flow):
        """Structures the refined project flow and saves it to a JSON file."""
        if not refined_flow:
            print("Refined flow is empty. Cannot proceed with structuring.")
            return

        chapters = self.parse_text_to_json(refined_flow)
        self.save_project_flow(chapters)

    def parse_text_to_json(text):
        """Parses the refined flow from Markdown to a list of dictionaries and handles various heading levels."""
        chapters = []
        current_chapter = None
        current_step = None
        collecting_description = False

        chapter_pattern = re.compile(r'#+\s*Chapter\s*\d+')
        step_pattern = re.compile(r'\d+\.\s*\*\*Step\s*(\d+):\s*(.*)')
        description_pattern = re.compile(r'\s*-\s*(.*)')  # To capture bullet points after steps

        for line in text.splitlines():
            line = line.strip()

            if chapter_pattern.match(line):
                if current_chapter:
                    chapters.append(current_chapter)  # Save the previous chapter
                chapter_title = line.split(":", 1)[-1].strip()  # Extract title after 'Chapter X:'
                current_chapter = {"chapter_title": chapter_title, "steps": []}
                current_step = None  # Reset the current step when a new chapter starts
                collecting_description = False  # Stop collecting descriptions when a new chapter starts
            elif step_pattern.match(line) and current_chapter:
                if current_step:
                    current_chapter["steps"].append(current_step)  # Save the previous step
                match = step_pattern.match(line)
                step_number = match.group(1)
                step_title = match.group(2)
                current_step = {"step_number": step_number, "step_title": step_title, "details": {}}
                collecting_description = False  # Reset collecting descriptions

            elif description_pattern.match(line):
                description = description_pattern.match(line).group(1).strip()
                if current_step:
                    if collecting_description:
                        current_step["details"]["Actionable Description"] += " " + description
                    else:
                        current_step["details"]["Actionable Description"] = description
                        collecting_description = True

        if current_step and current_chapter:
            current_chapter["steps"].append(current_step)
        if current_chapter:
            chapters.append(current_chapter)

        return chapters
    
    def save_project_flow(self, chapters):
        """Saves the structured project flow to a JSON file."""
        with open("project_flow.json", "w") as f:
            json.dump(chapters, f, indent=4)
        print("Project flow saved to project_flow.json")


if __name__ == "__main__":
    # Example usage:
    rough_project_flow = """
    # Project Setup
    * Install dependencies
    * Create project structure
    # Develop Feature X
    * Design UI
    * Implement backend
    * Write tests
    """

    tech_lead = TechLeadAgent()
    refined_flow = tech_lead.refine_project_flow(rough_project_flow)
    if refined_flow:
        tech_lead.structure_and_save_flow(refined_flow)