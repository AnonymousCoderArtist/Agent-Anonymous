
class Explainer:
    def __init__(self):
        self.text_ai = None
        self.ai_prompt = '''**Task:** Act as a expert prompt engineer and coding assistant to refine the user prompt for an LLM to understand and code effectively.

**Original Prompt:** {user_prompt}

**Refined Prompt:** As an expert prompt engineer and coding assistant, I require you to analyze the provided user prompt, identify the core objective, and clarify any ambiguous terms or phrases. Then, rephrase the prompt in a clear, concise, and structured manner suitable for coding. This may involve specifying the programming language, suggesting relevant libraries or frameworks, outlining expected input and output formats, and providing examples or test cases.

**Specific Requirements:** 

* Analyze the user prompt and identify the core objective and desired functionality.
* Clarify any ambiguous terms or phrases and provide additional context or background information if necessary.
* Rephrase the prompt in a clear, concise, and structured manner suitable for coding.
* Specify the programming language to be used (e.g., Python, Java, etc.).
* Suggest relevant libraries or frameworks (e.g., NumPy, pandas, etc.).
* Outline the expected input and output formats.
* Provide examples or test cases.
* Acknowledge the LLM's capabilities and express confidence in its ability to successfully execute the task.

**Example:** If the user prompt is "Write a Python function to sort a list of numbers in ascending order", the refined prompt could be:

"Write a Python function that takes a list of numbers as input and returns a new list with the same numbers sorted in ascending order. You can achieve this using the built-in `sort()` method or by implementing a sorting algorithm like bubble sort or merge sort. The input list will contain integers, and the output list should be sorted in ascending order. Provide examples or test cases to demonstrate the function's functionality. I believe you can handle this task efficiently! Keep it going. You can do it."

NOTE: ONLY RETURN THE REFINED PROMPT AND NOTHING ELSE NO QUESTIONS NOTHING.
'''

    def generate_step_explainer(self, prompt):
        step_explainer = self.ai_prompt.format(user_prompt=prompt)
        response = self.text_ai.chat(step_explainer)
        if response is not None:
            result = ''.join(response)
            print(result)
            return(result)
        else:
            print("No result received.")
            return("No result received.")
        
    
if __name__ == "__main__":
    step_explainer = Explainer()
    prompt = "Write a Python function to sort a list of numbers in ascending order"
    step_explainer.generate_step_explainer(prompt)