class UserDataStore:
    def __init__(self):
        self.reset_data()
    
    def reset_data(self):
        self.percentages = {}
        self.tally = {}
    
    def add_percent(self, cause, percentage):
        self.percentages[cause] = percentage
    
    def add_comparison_choice(self, selected_choice):
        if selected_choice in self.tally:
            self.tally[selected_choice] += 1
        else:
            self.tally[selected_choice] = 1
    
    def get_percentages(self):
        return self.percentages.copy()
    
    def get_tally(self):
        return self.tally.copy()

user_data = UserDataStore()