from kivy.uix.textinput import TextInput
from mdata.drivers.databases.operations import Operations


class CompanyListTextinput(TextInput):
    def __init__(self, **kwargs):
        self.db_oper = Operations()
        self.validate = True
        self.allow_copy = True
        self.multiline = True
        self.readonly = True
        self.size_hint = (0.4, 0.8)
        self._data_chunks = None
        self.chunk_limit = 100
        self.current_chunk = 0
        super(CompanyListTextinput, self).__init__(**kwargs)

    def __call__(self):
        self.set_text()
        return self

    @property
    def data_chunks(self):
        if self._data_chunks is None:
            chunks = list()
            counter = 0
            rows = list()
            for company in self._get_names():
                if counter > self.chunk_limit:
                    chunks.append(rows)
                    counter = 0
                    rows = list()
                row = '{name}, {symbol}'.format(name=company[0],
                                                symbol=company[1])
                rows.append(row)
                counter += 1
            self._data_chunks = chunks
        return self._data_chunks

    def _get_names(self):
        comp_data = self.db_oper.get_columns(table='company_info',
                                             columns=['name', 'symbol'])
        return comp_data

    def set_text(self):
        self.text = ''
        self.text = '\n'.join(self.data_chunks[self.current_chunk])

    def next_chunk(self):
        if self.current_chunk >= len(self.data_chunks) - 1:
            self.current_chunk = 0
        else:
            self.current_chunk += 1