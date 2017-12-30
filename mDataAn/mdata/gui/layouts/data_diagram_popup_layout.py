from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from mdata.drivers.config.config_management import ConfigManagement


class DataDiagramPopupLayout(GridLayout):
    def __init__(self, **kwargs):
        self.name = 'Data diagram popup layout'
        self.rows = 2
        self.plots = kwargs['plots']
        self.select_plot = kwargs['select_plot']
        super(DataDiagramPopupLayout, self).__init__(**kwargs)

    def __call__(self):
        return self.generate()

    def generate(self):
        if self.plots.last_company and not self._compare_company_vars():
            self.add_widget(self._diagram_not_found_label())

        elif self.plots.unp_plot_fig or self.plots.volume_plot_fig:
            if self.select_plot == 'price_oc':
                self.add_widget(FigureCanvasKivyAgg(self.plots.unp_plot_fig))
            elif self.select_plot == 'price_hl':
                self.add_widget(FigureCanvasKivyAgg(self.plots.high_low_fig))
            elif self.select_plot == 'volume':
                self.add_widget(FigureCanvasKivyAgg(self.plots.volume_plot_fig))
            elif self.select_plot == 'reg':
                try:
                    self.add_widget(FigureCanvasKivyAgg(self.plots.regression_fig))
                except:
                    self.add_widget(self._diagram_not_found_label())
            elif self.select_plot == 'reg_train':
                try:
                    self.add_widget(FigureCanvasKivyAgg(self.plots.regression_train_fig))
                except:
                    self.add_widget(self._diagram_not_found_label())
        else:
            self.add_widget(self._diagram_not_found_label())

        return self

    def _diagram_not_found_label(self):
        nf_label = Label(text='You have to load data to generate diagram!')
        return nf_label

    def _compare_company_vars(self):
        config_mng = ConfigManagement()
        config_data = config_mng.get_data()
        company = config_data['company']

        are_identical = True
        if company != self.plots.last_company:
            are_identical = False
        return are_identical
