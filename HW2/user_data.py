class UserDataStore:
    def __init__(self):
        self.reset_data()
    
    def reset_data(self):
        self.percentages = {}
        self.comparisons = []
    
    def add_percent(self, cause, percentage):
        self.percentages[cause] = percentage
    
    def add_comparison_choice(self, option1, option2, selected):
        for i, (opt1, opt2, _) in enumerate(self.comparisons):
            if (opt1 == option1 and opt2 == option2) or (opt1 == option2 and opt2 == option1):
                self.comparisons[i] = (option1, option2, selected)
                return
        
        self.comparisons.append((option1, option2, selected))
    
    def get_percentages(self):
        return self.percentages.copy()
    
    def get_tally(self):
        tally = {}
        for _, _, selected in self.comparisons:
            if selected in tally:
                tally[selected] += 1
            else:
                tally[selected] = 1
        return tally
    
    def get_comparisons(self):
        return self.comparisons.copy()

user_data = UserDataStore()