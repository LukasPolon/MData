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
            tables = {'company_info': CompanyInfo}
        return tables

    def get_columns(self, table=None, columns=None):
        try:
            selected_table = self.tables[table]
        except KeyError:
            raise KeyError('Wrong table name.')

        mytable = selected_table.__table__
        columns_attr = list()
        if columns:
            columns_attr = [getattr(selected_table, col_name)
                            for col_name in columns]

        db_driver = DbDriver()
        engine = db_driver.register_engine()
        session = db_driver.create_db_session(engine)
        if columns:
            result = session.query(*columns_attr)
        else:
            result = session.query(mytable)

        table_data = [row for row in result]
        return table_data






if __name__ == '__main__':
    ob = Operations()
    ob.get_columns(table='company_info', columns=['id', 'name'])



