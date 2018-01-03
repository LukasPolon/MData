from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label


class InfoScreenLayout(AnchorLayout):
    def __init__(self, **kwargs):
        self.anchor_x = 'center'
        self.anchor_y = 'top'
        super(InfoScreenLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        self.add_widget(Label(text=self.get_text_info(), markup=True))
        return self

    def get_text_info(self):
        info = '''[size=25][b]The analysis of stock market data with tools avaliable in scikit-learn module[/b][/size]
        
        
        
        [size=18]Application usage:
        
        1. Go to Options Screen and set desired options:[/size][size=14]
                1.1 Directory for plots and results
                1.2 Company name, which data will be downloaded
                1.3 Date range (data amount)
                1.4 Regression method (Linear, KRR, SVR, Gaussian)
                1.5 Data set, which will be used for regression (Open, Close, High, Low)
                1.6 Training / test data split rate (% of training data)[/size][size=18]
    
        2. Go to Regression Screen and load the data
    
        3. Check data plots (Open/Close, High/Low, Volume price diagrams)
    
        4. Perform the regression analysis
    
        5. Check the results and regression plots
    
        6. Save the output[/size]'''
        return info