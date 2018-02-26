import pandas as pd
from enum import Enum
import os
os.environ["NLS_LANG"] = "Russian.AL32UTF8"
import cx_Oracle


class DataBases(Enum):
    Oracle = "Oracle DB"
    MSSQL = "MS SQL Server"
    MSAccess = "MS Access"


# TODO: допилить класс и интегрировать в work_server.py
class DBOperations(object):
    def __init__(self, connection_str, db_type=DataBases.Oracle, user=None, password=None):
        self.connection_str = connection_str
        self.user = user
        self.password = password
        self.db_type = db_type

    def connect(self):
        if self.db_type == DataBases.Oracle:
            self.connection = cx_Oracle.connect(user=self.user,
                                                password=self.password,
                                                dsn=self.connection_str)
        elif self.db_type == DataBases.MSSQL:
            pass
        elif self.db_type == DataBases.MSAccess:
            pass
        pass

    def disconnect(self):
        if self.db_type == DataBases.Oracle:
            self.connection.close()

    def download(self, query, path):
        df = pd.read_sql(query, self.connection)
        df.to_excel(path, index=False)

    def upload(self, query, data):
        pass
