import os

class ProjectCreator:
    def __init__(self, project_name):
        self.project_name = project_name.replace(" ", "_")
        self.description = ""

    def create_project(self):
        os.makedirs(self.project_name, exist_ok=True)
        self.description = self.get_description()
        print(f"Project '{self.project_name}' created successfully!")
        return os.path.join(os.getcwd(), self.project_name), self.description

    def get_description(self):
        print("Please describe the project as much as possible if the description is over then press shift+enter: ")
        description = ""
        while True:
            line = input()
            if not line:
                break
            description += line + "\n"
        return description
