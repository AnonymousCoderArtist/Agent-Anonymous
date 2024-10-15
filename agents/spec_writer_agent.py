from model.sambanova import SambanovaAPI
class SpecWriterAgent:
    def __init__(self):
        self.text_ai = None
        self.ai_prompt = '''**Project Complexity and Description Framework:**
Act as an expert Project Analyst who can assess project complexity and generate comprehensive project descriptions.
## Project Complexity and Description Analysis:


**Output:**
Generate a structured analysis of the project containing the following:

* **Project Complexity Assessment:** Classify the project's complexity as **Low**, **Medium**, **High**, or **Very High**, supported by a clear justification outlining the factors contributing to the assigned level. Consider the following factors:
	+ **Scope and Size:** Specify the number of features, deliverables, and stakeholders involved in the project.
	+ **Technical Difficulty:** Describe the technologies used, integration complexity, and novelty of the solution.
	+ **Dependencies:** Identify internal and external dependencies and potential bottlenecks.
	+ **Risk and Uncertainty:** Outline potential challenges, unknown factors, and the likelihood of changes.
* **Comprehensive Project Description:** Provide a concise and well-structured description of the project, suitable for handover to an architect agent. The description should:
	+ Summarize the project's goals and scope.
	+ Outline key features and technical requirements.
	+ Be clear, concise, and easily understandable by someone unfamiliar with the project.

Example: If the project is "Develop a mobile application for online food ordering," the project complexity assessment would consider factors like the app's features (user registration, menu browsing, order placement, payment integration, delivery tracking, etc.), the chosen tech stack (native or hybrid development), integration with third-party services (payment gateways, map APIs), and potential challenges (scalability, security).

**Note:** Provide a well-organized and easy-to-understand output using bullet points, tables, or other appropriate formatting. PROVIDE ONLY THE COMPREHENSIVE PROJECT DESCRIPTION AND NOTHING ELSE.

**Input:** {project_description}
'''

    def generate_spec(self, project_description):
        prompt_with_description = self.ai_prompt.format(project_description=project_description)
        response = self.text_ai.chat(prompt_with_description)
        
        if response is not None:
            result = ''.join(response)
            print(result)
            return(result)
        else:
            print("No result received.")
            return("No result received.")
            

if __name__ == "__main__":
    spec_writer = SpecWriterAgent()
    spec_writer.text_ai = SambanovaAPI(r"G:\ALL JARVIS\Anonymous-Agent\model\cookies.json", model="Meta-Llama-3.2-1B-Instruct")
    project_description = """
I want to create a simple calculator app in python with a tkinter GUI.
"""
    spec_writer.generate_spec(project_description)