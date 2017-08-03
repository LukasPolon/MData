import os

MDATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MAIN_DIRECTORY = os.path.dirname(MDATA_DIR)
TEST_DATABASE = os.path.join(MAIN_DIRECTORY, 'utils', 'test_db.db')
COMPANY_LIST_CSV = os.path.join(MAIN_DIRECTORY, 'utils', 'comp_list.csv')
DB_CONNECTION = 'sqlite:///'

