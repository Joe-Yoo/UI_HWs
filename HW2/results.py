from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from user_data import user_data
from utils import CAUSES

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )

        table = GridLayout(
            cols=4,
            rows=7,
            spacing=dp(2)
        )
        
        cell_contents = {
            1: ("Results", sp(24), True),
            2: ("Rating", sp(14), False),
            3: ("Tally", sp(14), False),
            4: ("Weight", sp(14), False),
            5: ("Mental Demand", sp(14), False),
            9: ("Physical Demand", sp(14), False),
            13: ("Temporal Demand", sp(14), False),
            17: ("Performance", sp(14), False),
            21: ("Effort", sp(14), False),
            25: ("Frustration", sp(14), False)
        }
        
        self.data_cells = {}
        
        for i in range(1, 29):
            if i in cell_contents:
                text, font_size, bold = cell_contents[i]
                if bold:
                    cell = Label(
                        text=f"[b]{text}[/b]",
                        font_size=font_size,
                        markup=True,
                        halign='center',
                        valign='middle'
                    )
                else:
                    cell = Label(
                        text=text,
                        font_size=font_size,
                        halign='center',
                        valign='middle'
                    )
            else:
                cell = Label(
                    text=str(i),
                    font_size=sp(16),
                    halign='center',
                    valign='middle'
                )
                if i in [6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27, 28]:
                    self.data_cells[i] = cell
            table.add_widget(cell)
        
        main_layout.add_widget(table)
        
        # Bottom row
        self.bottom_row = Label(
            text='Overall: 0.00',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(self.bottom_row)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.calculate_results()
    
    def calculate_results(self, instance=None):
        percents = user_data.get_percentages()
        tallies = user_data.get_tally()

        data = []
        total_sum = 0
        
        cell_positions = {
            "Mental Demand": [6, 7, 8],
            "Physical Demand": [10, 11, 12], 
            "Temporal Demand": [14, 15, 16],
            "Performance": [18, 19, 20],
            "Effort": [22, 23, 24],
            "Frustration": [26, 27, 28]
        }
        
        for c in CAUSES:
            rating = percents.get(c, 0)
            tally = tallies.get(c, 0)
            weight = tally / 15
            
            product = rating * tally
            total_sum += product
            
            data.append((c, rating, tally, weight))
            
            if c in cell_positions:
                rating_cell, tally_cell, weight_cell = cell_positions[c]
                self.data_cells[rating_cell].text = str(rating)
                self.data_cells[tally_cell].text = str(tally) 
                self.data_cells[weight_cell].text = f"{weight:.3f}"

        overall = total_sum / 15
        self.bottom_row.text = f'Overall: {overall:2f}'
        