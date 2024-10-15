import re
import sys
from typing import Dict, Any
from webscout import PhindSearch as a
from agents.senior_coder import SeniorCoder
import os
import uuid


class CodeExecutor:
    def __init__(self, code_dir):
        self.autocoder = SeniorCoder()
        self.autocoder.internal_exec = True
        self.autocoder.confirm_script = False
        self.autocoder.prettify = False
        self.autocoder.quiet = True
        self.code_dir = code_dir
        if not os.path.exists(self.code_dir):
            os.makedirs(self.code_dir)

    def execute_execute_python_code(self, arguments: Dict[str, Any]) -> str:
        """
        Executes Python code using the AutoCoder based on the user's request.
        Handles missing packages, code errors, and saves code to a file.
        """
        user_request = arguments.get("user_request")

        intro_prompt = self.autocoder.intro_prompt

        ai = a(
            is_conversation=True,
            max_tokens=800,
            timeout=30,
            intro=intro_prompt,
            proxies={},
            history_offset=10250,
            act=None,
        )

        if user_request:
            response = ai.chat(user_request)
            autocoder_feedback = self.autocoder.main(response)  # Get output from SeniorCoder

            # Save the code to a file
            code_blocks = re.findall(r"```python.*?```", response, re.DOTALL)
            if code_blocks:
                raw_code = code_blocks[0]
                raw_code_plus = re.sub(r"(```)(python)?", "", raw_code)
                file_name = f"{uuid.uuid4().hex}.py"  # Generate unique file name
                file_path = os.path.join(self.code_dir, file_name)
                with open(file_path, "w") as f:
                    f.write(raw_code_plus)

            if "PREVIOUS SCRIPT EXCEPTION" in autocoder_feedback:
                pass 
            else:
                return autocoder_feedback  # Return the output of the code 
        else:
            return "Please provide a user request to generate and execute Python code."