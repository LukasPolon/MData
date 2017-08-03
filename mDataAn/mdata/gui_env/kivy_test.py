import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class CalcGridLayout(GridLayout):


    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "ERROR!"


class CalculatorApp(App):

    def build(self):
        return CalcGridLayout()

calc_app = CalculatorApp()
calc_app.run()
