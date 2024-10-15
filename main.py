from agents.project_creator import ProjectCreator
from agents.spec_writer_agent import SpecWriterAgent
from agents.architect_agent import ArchitectAgent
from agents.tech_lead_agent import TechLeadAgent
from agents.user_interaction_agent import UserInteractionAgent
from agents.code_executor import CodeExecutor
from agents.step_explainer import Explainer
from model.sambanova import SambanovaAPI
import json

def handle_modifications(artifact, refine_function, user_interaction):
    """Handles user modifications for a given artifact (specification or flow)."""
    while True:
        if not user_interaction.ask_continue(question=f"Satisfied with the {artifact}?"):
            raise SystemExit("Exiting process...")

        user_query = user_interaction.get_user_query()
        if user_query:
            if "change" in user_query.lower() or "modify" in user_query.lower():
                print(f"Please provide the updated {artifact}:")
                updated_content = input()
                artifact = f"{artifact}\n\n**User Modifications:**\n{updated_content}"
                artifact = refine_function(artifact)
                print(f"Updated {artifact}:\n{artifact}")
            else:
                print(f"Processing user query: {user_query}")
        else:
            break

    return artifact

def main():
    """Main function to orchestrate the project creation process."""
    tech_lead = TechLeadAgent()
    user_interaction = UserInteractionAgent()

    try:
        model = SambanovaAPI(r"G:\ALL JARVIS\Anonymous-Agent\model\cookies.json", model="Meta-Llama-3.1-8B-Instruct")

        project_name = input("Enter project name: ")

        creator = ProjectCreator(project_name)
        spec_writer = SpecWriterAgent()
        spec_writer.text_ai = model
        project_folder_path, project_description = creator.create_project()

        # Create the CodeExecutor with the project directory
        code_executor = CodeExecutor(code_dir=project_folder_path)  

        architect = ArchitectAgent(project_description)
        architect.text_ai = model

        print(project_description)
        specification = spec_writer.generate_spec(project_description)

        specification = handle_modifications("specification", spec_writer.generate_spec, user_interaction)

        # Create the ArchitectAgent, passing the specification
        architect = ArchitectAgent(specification)
        architect.text_ai = model

        # Use the ArchitectAgent
        response = architect.generate_flow_code()
        architect.extract_and_run_code(response)
        project_flow = architect.extract_flow(response)

        # Handle project flow modifications
        tech_lead.text_ai = model
        project_flow = handle_modifications("project flow", tech_lead.refine_project_flow, user_interaction)

        print(project_flow)
        tech_lead.structure_and_save_flow(project_flow)

        with open("project_flow.json", "r") as f:
            structured_flow = json.load(f)

        context = ""
        for chapter in structured_flow:
            print(f"[bold blue]## {chapter['chapter_title']}[/]")
            for step in chapter['titles']:
                print(f"[bold green]**Step {step['step_number']}**: {step['step_description']}[/]")

                explainer = Explainer()
                explainer.text_ai = model
                explained_step = explainer.generate_step_explainer(step['step_description'])

                result = code_executor.execute_execute_python_code({"user_request": explained_step})
                print(result)

                context += f"\nStep {step['step_number']} Output:\n{result}"

    except SystemExit as e:
        print(e)
    finally:
        print("Project creation completed.")

if __name__ == "__main__":
    main()