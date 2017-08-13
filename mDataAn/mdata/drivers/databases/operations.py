from sqlalchemy import literal
from mdata.drivers.databases.mDataAnDB.company_info import CompanyInfo
from mdata.drivers.databases.db_driver import DbDriver
from mdata.drivers.databases.db_driver import database_session


from sqlalchemy.sql.expression import select


class Operations(object):
    def __init__(self):
        self._tables = None

    @property
    def tables(self):
        if self._tables is None:
            self._tables = {'company_info': CompanyInfo}
        return self._tables

    @database_session
    def get_columns(self, session=None, table=None, columns=None):
        try:
            selected_table = self.tables[table]
        except KeyError:
            raise KeyError('Wrong table name.')

        mytable = selected_table.__table__
        if columns:
            columns_attr = [getattr(selected_table, col_name)
                            for col_name in columns]
            result = session.query(*columns_attr)
        else:
            result = session.query(mytable)

        table_data = [row for row in result]

        return table_data

    @database_session
    def get_one_record(self, session=None, table=None, name=None):
        try:
            selected_table = self.tables[table]
        except KeyError:
            raise KeyError('Wrong table name.')
        mytable = selected_table.__table__
        col = getattr(selected_table, 'name')

        result = session.query(mytable).filter(col == name)
        data = {key: value for (key, value)
                in zip(mytable.columns.keys(), [el for el in result][0])}
        return data

    @database_session
    def exists_query(self, session=None, table=None, column=None, value=None):
        try:
            selected_table = self.tables[table]
        except KeyError:
            raise KeyError('Wrong table name.')
        mytable = selected_table.__table__
        col = getattr(selected_table, column)

        exists_query = session.query(mytable).filter(col == value)
        result = session.query(literal(True)).filter(
                                                exists_query.exists()).scalar()
        return result


if __name__ == '__main__':
    ob = Operations()
    r = ob.get_one_record(table='company_info', name='Ericsson')
    print(r)





