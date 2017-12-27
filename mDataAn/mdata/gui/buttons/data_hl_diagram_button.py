from kivy.uix.button import Button
from kivy.uix.popup import Popup
from mdata.gui.layouts.data_diagram_popup_layout import DataDiagramPopupLayout


class DataHLDiagramButton(Button):
    def __init__(self, **kwargs):
        self.size_hint = (0.15, 0.1)
        self.text = 'High/Low price\n' \
                    ' data diagram'
        self.plots = kwargs['plots']
        super(DataHLDiagramButton, self).__init__(**kwargs)

    def on_press(self):
        self.generate_popup()

    def generate_popup(self):
        data_popup = DataDiagramPopupLayout(plots=self.plots,
                                            select_plot='price_hl')
        popup = Popup(title='DataDiagram',
                      content=data_popup,
                      size=(550, 550),
                      size_hint=(None, None))
        data_popup.kwargs = {'base': popup}
        data_popup()
        popup.open()

    def _verify_plot_generate(self):
        check = True
        if self.plots.data is None:
            check = False

        return check