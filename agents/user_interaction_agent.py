class UserInteractionAgent:
    def __init__(self):
        self.separator = "-" * 40 

    def ask_continue(self, question):
        """Asks the user if they want to continue the process."""
        print(self.separator)
        while True:
            response = input(f"Do you want to continue the process? {question} (yes/no): ").lower()
            if response in ["yes", "y"]:
                return True
            elif response in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def get_user_query(self):
        """Gets any specific query from the user."""
        print(self.separator)
        query = input("Do you have any specific queries or instructions?\n(Press Enter to skip): ")
        return query