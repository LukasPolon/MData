import csv

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


from mdata.drivers.databases.db_driver import DbDriver
from mdata.drivers.databases.db_driver import database_session
from mdata.drivers.databases.db_driver import BASE

from mdata import common

DB_DRIVER = DbDriver()


class CompanyInfo(BASE):
    """ Model for company_info table.

        Attributes:
            id (int): primary key, auto-increment
            symbol (str): data set symbol, e.g. AAPL
            name (str): company name, e.g. Apple Inc.
            sector (str): industrial sector, e.g. Technology
            industry (str): industry branch, e.g. Computer Manufacturing
            summary_quote (str): direct link to the Nasdaq Composite site
    """
    __tablename__ = 'company_info'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(40), nullable=False)
    sector = Column(String(30))
    industry = Column(String(40))
    summary_quote = Column(String(40))

    def _get_data(self):
        """ Get stock data from csv file.

            Returns:
                symbols (list): list of dictionaries, which
                contains stock data
        """
        names = ['symbol', 'name', 'sector', 'industry', 'summary_quote']
        with open(common.COMPANY_LIST_CSV, 'rb') as f:
            symbols = [row for row in csv.DictReader(f, fieldnames=names)]

        return symbols

    def reset_table(self):
        """ Remove company_info table from database, if exists."""
        engine = DB_DRIVER.register_engine()
        if engine.dialect.has_table(engine, self.__tablename__):
            # BASE.metadata.bind = engine
            company_info = self.__table__
            company_info.drop()

    def create_table(self):
        """ Create company_info table if not exists."""
        engine = DB_DRIVER.register_engine()
        if not engine.dialect.has_table(engine, self.__tablename__):
            # Base.metadata.bind = engine
            company_info = self.__table__
            company_info.create()

    @database_session
    def fill_up_table(self, session):
        """ Fill up company_info table with data from csv file."""
        [session.add(CompanyInfo(**row)) for row in self._get_data()]
        session.commit()


if __name__ == '__main__':
    ob = CompanyInfo()
    # ob.reset_table()
    ob.create_table()
    ob.fill_up_table()




