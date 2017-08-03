import csv

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from mdata import common

Base = declarative_base()


class CompanyInfo(Base):
    """ Model for company_info table."""
    __tablename__ = 'company_info'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(40), nullable=False)
    sector = Column(String(30))
    industry = Column(String(40))
    summary_quote = Column(String(40))

    def _get_data(self):
        symbols = list()
        names = ['symbol', 'name', 'sector', 'industry', 'summary_quote']
        with open(common.COMPANY_LIST_CSV, 'rb') as f:
            reader = csv.DictReader(f, fieldnames=names)
            [symbols.append(row) for row in reader]

        return symbols

    def reset_table(self):
        engine = create_engine('{conn}{db}'.format(db=common.TEST_DATABASE,
                                                   conn=common.DB_CONNECTION))
        if engine.dialect.has_table(engine, self.__tablename__):
            Base.metadata.bind = engine
            company_info = self.__table__
            company_info.drop()

    def create_table(self):
        engine = create_engine('{conn}{db}'.format(db=common.TEST_DATABASE,
                                                   conn=common.DB_CONNECTION))
        Base.metadata.bind = engine
        company_info = self.__table__
        company_info.create()

    def fill_up_table(self):
        engine = create_engine('{conn}{db}'.format(db=common.TEST_DATABASE,
                                                   conn=common.DB_CONNECTION))
        Base.metadata.bind = engine
        dbsession = sessionmaker(bind=engine)
        session = dbsession()
        [session.add(CompanyInfo(**row)) for row in self._get_data()]
        session.commit()


if __name__ == '__main__':
    ob = CompanyInfo()
    # ob.reset_table()
    ob.create_table()
    ob.fill_up_table()




