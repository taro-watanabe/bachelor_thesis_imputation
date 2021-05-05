import numpy as np
import pandas as pd
import sqlalchemy as sq



## --------configure_URI_info_here:-------------
## I use a postgres based engine but theoretically any conventional dialect based off of SQl should in fact work.
## Construction of URI is optional; if you would like to work directly from the csv format -> out into csv format,
## simply put the "no_db" option to True in the main.

config = {
        'engine': 'postgresql+psycopg2',
        'USER': 'postgres',
        'PSW': 'Pass2020!',
        'DB_URL': '127.0.0.1:5432',
        'DB': 'postgres'
}

URI = config['engine'] + '://' + config['USER'] + ':' + config['PSW'] \
              + '@' + config['DB_URL'] + ':5432/' + config['DB']


class Bocconi:

    def __init__(self, table_name, imputation_method, sample_size, ml_algo, ml_param, no_db):
        self.impute_method = imputation_method
        self.sample = sample_size
        self.table = table_name
        self.algo = ml_algo
        self.algo_param = ml_param
        self.no_db_bool = no_db


    def load_datasets(self):

        if self.no_db_bool == True:
            df = pd.read_csv(str(self.table))

        elif self.no_db_bool == False:
            df = pd.read_sql_table(str(self.table), sq.create_engine(URI))

        else:
            raise Exception("The no_db boolean seems to be a non boolean.")

        return df

    def show_information_df(self, df):

        print(df.columns)
        print(df.index)
        print(df.shape)
        print(df)



