# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
License: MIT
"""

from app.util.helpers import *

from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase
from playhouse.reflection import generate_models, print_model, print_table_sql
from playhouse.dataset import DataSet
from playhouse.db_url import connect
import pymysql


def test():
    print('working!')


class DbWrapper:
    # private
    _db = None
    _ds = None
    _models = None

    # public data
    driver = None
    db_name = None
    db_user = None
    db_pass = None
    db_host = None
    db_port = None
    file = None

    # reset
    def reset(self):

        self._db = None
        self._ds = None
        self._models = None

        self.driver = None
        self.db_name = None
        self.db_user = None
        self.db_pass = None
        self.db_host = None
        self.db_port = None
        self.file = None

        # helpers

    def close(self):
        self._db.close()

    def connect(self):

        if not self.driver:
            print(' > Error DB driver not set')

        if self.driver == COMMON.DB_SQLITE:
            self._db = SqliteDatabase(self.db_name)
            self._ds = DataSet(self._db)
            return True
        elif self.driver == COMMON.DB_MYSQL:
            self._db = MySQLDatabase(self.db_name, user=self.db_user, password=self.db_pass, host=self.db_host,
                                     port=self.db_port)
            self._ds = DataSet(self._db)
            return True
        elif self.driver == COMMON.DB_PGSQL:
            self._db = PostgresqlDatabase(self.db_name, user=self.db_user, password=self.db_pass, host=self.db_host,
                                          port=self.db_port)
            self._ds = DataSet(self._db)
            return True
        else:
            print(' > Error unsupported driver [' + self.driver + ']')
            return False

    def load_models(self):

        if not self._db:
            print(' > Error: No DB connection')
            return None

        if not self._models:
            self._models = generate_models(self._db)
            return True

    def get_tables_name(self):
        return list(self._models.keys())

    def get_model(self, aModelName):

        if not self._db:
            print(' > Error: No DB connection')
            return None

        if not self._models:
            print(' > Error: No DB models')
            return None

        if not aModelName in self._models:
            print(' > Error Model [' + aModelName + '] not found')
            return None

        return self._models[aModelName]

    def get_model_data(self, aModelName):

        aModel = self.get_model(aModelName)

        if not aModel:
            return None

        return self._ds[aModelName].all()

    def print_all_models(self):

        if not self._db:
            print(' > Error: No DB connection')
            return

        if not self._models:
            print(' > Error: No DB models')
            return

        print(list(self._models.items()))

    def print_db_model(self, aModelName, aSql=False):

        if not self._models:
            print(' > Error: No DB models')
            return

        if not aModelName in self._models:
            print(' > Error Model [' + aModelName + '] not found')
            return

        aModel = self._models[aModelName]

        if aSql:
            print_table_sql(aModel)
        else:
            print_model(aModel)

        return

    def sql_select(self, aModelName):

        if not self._models:
            print(' > Error: No DB models')
            return

        if not aModelName in self._models:
            print(' > Error Model [' + aModelName + '] not found')
            return None

        aModel = self._models[aModelName]

        for item in aModel.select():
            print(item)

    def dump_model_data(self, aModelName, aFileName=None):

        items = self.get_model_data(aModelName)

        # if not items:
        #     return None

        if len(items) == 0:
            print(' > Model [' + aModelName + '] is empty ')
            return None

        header = items[0].keys()

        sqlContent = ''

        for col in header:
            sqlContent += col + ','
        sqlContent = sqlContent[:-1]  # delete the last comma
        sqlContent += '\n'

        for row in items:

            for i in row.values():
                sqlContent += str(i) + ','
            sqlContent = sqlContent[:-1]  # delete the last comma
            sqlContent += '\n'

        if not aFileName:
            aFileName = get_date() + '_' + self.driver + '_' + aModelName

        if not aFileName.endswith('.sql'):
            aFileName += '.sql'

        return sqlContent

    def dump_tables(self, aFileName=None):

        sqlContent = ''

        if not self._models:
            print(' > Error: No DB models')
            return False

        if not aFileName:
            aFileName = get_date() + '_' + self.driver

        if not aFileName.endswith('.sql'):
            aFileName += '.sql'

        for table_name in self._models.keys():

            # SQLite Engine Metadata
            if 'sqlite_sequence' == table_name:
                continue

            # Unused
            aModel = self._models[table_name]

            # Hack the print
            with Capturing() as output:

                self.print_db_model(table_name, True)

            sqlContent += '\n'
            sqlContent += '-- Table: ' + table_name + '\n'
            sqlContent += h_list_to_s(output, '\n')
            sqlContent += ';\n'

        return sqlContent

    def dump_models(self, aFileName=None):

        sqlContent = ''

        if not self._models:
            print(' > Error: No DB models')
            return False

        if not aFileName:
            aFileName = get_date() + '_' + self.driver + '_models'

        if not aFileName.endswith('.sql'):
            aFileName += '.sql'

        for table_name in self._models.keys():

            # SQLite Engine Metadata
            if 'sqlite_sequence' == table_name:
                continue

            # Unused
            aModel = self._models[table_name]

            # Hack the print
            with Capturing() as output:

                self.print_db_model(table_name)

            sqlContent += '\n'
            sqlContent += '-- Table: ' + table_name + '\n'
            sqlContent += h_list_to_s(output, '\n')
            sqlContent += ';\n'

        return sqlContent

    def dump_tables_data(self, aFileName=None):

        sqlContent = ''

        if not self._models:
            print(' > Error: No DB models')
            return False

        if not aFileName:
            aFileName = get_date() + '_' + self.driver

        if not aFileName.endswith('.sql'):
            aFileName += '.sql'

        for table_name in self._models.keys():

            # SQLite Engine Metadata
            if 'sqlite_sequence' == table_name:
                continue

            # print(' > Dump data for [' + table_name + ']')
            print(self.dump_model_data(table_name))

        return True
