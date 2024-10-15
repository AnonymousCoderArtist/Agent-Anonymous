import subprocess
import re
import sys
import click
import platform
import os
import datetime
def run_system_command(
    command: str,
    exit_on_error: bool = True,
    stdout_error: bool = True,
    help: str = None,
):
    """Run commands against system
    Args:
        command (str): shell command
        exit_on_error (bool, optional): Exit on error. Defaults to True.
        stdout_error (bool, optional): Print out the error. Defaults to True
        help (str, optional): Help info incase of exception. Defaults to None.
    Returns:
        tuple: (is_successful, object[Exception|Subprocess.run])
    """
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return (True, result)
    except subprocess.CalledProcessError as e:
        # Handle error if the command returns a non-zero exit code
        if stdout_error:
            click.secho(f"Error Occurred: while running '{command}'", fg="yellow")
            click.secho(e.stderr, fg="red")
            if help is not None:
                click.secho(help, fg="cyan")
        sys.exit(e.returncode) if exit_on_error else None
        return (False, e)

class ArchitectAgent:
    def __init__(self, project_description):
        self.text_ai = None
        self.interpreter: str = "python",
        self.internal_exec: bool = True,
        self.python_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            if self.internal_exec
            else run_system_command(
                f"{self.interpreter} --version",
                exit_on_error=True,
                stdout_error=True,
            )[1].stdout.split(" ")[1]
        )
        self.ai_prompt = f'''Act as a software project manager who is an expert in Python. I am starting a new project with the following complexity and description:
{project_description}

Based on this information, I need you to:

1. **Outline the project flow:** Provide a detailed outline of the project flow, outlining the major steps and dependencies involved in developing the project.
2. **Generate the necessary Python code:** Provide the Python code to install the required dependencies for this project using a suitable package manager (e.g., pip). Please ensure the code is compatible with Python 3.8. Please include the target Python version in the code.
3. **Structure the flow of the project:** The flow of the project should be well-structured, commented, and easy to understand. Consider using a virtual environment for dependency management.

## Code to Install Dependencies
```Python
pip install (module)
```
## Project Flow

# Project Setup
* Install dependencies
* Create project structure
# Develop Feature X
* Design UI
* Implement backend
* Write tests


Current system : {platform.system()}
Python version : {self.python_version}
Current directory : {os.getcwd()}
Current Datetime : {datetime.datetime.now()}

Note: The actual code and project flow will depend on the specific project description and requirements. This promptified prompt includes the necessary details and specifications for a well-structured project flow. ONLY RETURN THE PROJECT FLOW AND CODE TO INSTALL DEPENDENCIES KEEP IN MIND THAT THERE ARE NO REQUIREMENTS.TXT OR ANYTHING AND NOTHING ELSE.
'''

    def generate_flow_code(self):
        prompt_with_description = self.ai_prompt
        response = self.text_ai.chat(prompt_with_description)
        if response is not None:
            result = ''.join(response)
            print(result)
            return(result)
        else:
            print("No result received.")
            return("No result received.")

    def extract_and_run_code(self, response):
        code_block = re.search(r"```python(.*?)```", response, re.DOTALL)
        if code_block:
            code = code_block.group(1).strip()
            print("Installing dependencies...")
            commands = code.split('\n')
            for command in commands:
                subprocess.run(command, shell=True, check=True)
        else:
            print("No Python code block found in the response.")

    def extract_flow(self, response):
        flow_section = None
        if "## Project Flow" in response:
            flow_section = response.split("## Project Flow")[1].strip()
        elif "**Project Flow" in response:
            flow_section = response.split("**Project Flow")[1].strip()
        elif "##Project Flow" in response:
            flow_section = response.split("##Project Flow")[1].strip()
        
        if flow_section:
            print("\n## Project Flow:\n")
            print(flow_section)
            return flow_section
        else:
            print("No project flow section found in the response.")
            return None
