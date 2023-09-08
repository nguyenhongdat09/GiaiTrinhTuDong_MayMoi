import pandas as pd
import numpy as np
from pandas.core.indexing import _IndexSlice
import unidecode
from Constant.ProjectConstant import project_constant
from unidecode import unidecode
from datetime import datetime
import timedelta


class data_collector(object):
    def __init__(self, directory_file):
        self.directory_file = directory_file
        self.data_excel = None
        self.df = None
        self.pd = pd

    def set_panda_options(self):
        self.pd.set_option('display.max_rows', project_constant.DISPLAY_MAX_ROW, 'display.max_columns',
                           project_constant.DISPLAY_MAX_COLUMN)
        self.pd.set_option('display.width', project_constant.DISPLAY_MAX_WIDTH)
        # self.pd.options.mode.chained_assignment = None

    def groupColumn(self, df):
        df_colum_1 = [[x[0] if x[1] == '' else x[1], ''] for x in df.columns.tolist()]
        # pd.MultiIndex.from_tuples(df_colum_1)
        df.columns = pd.MultiIndex.from_tuples(df_colum_1)
        df.columns = df.columns.droplevel(1)
        self.df = df
        return self.df

    def getData(self, header):
        df = pd.read_excel(self.directory_file, header=header)
        df.rename(columns=lambda x: x if "Unnamed" not in str(x) else '', inplace=True)
        df.rename(columns=project_constant.COLUMN_NAME_REPLACE, level=0, inplace=True)
        # Chuyển Column Multi level thanh tuples // df.columns.values la  mang col dang tuple de thay doi name roi conver lai thanh multiple index
        df.columns = df.columns.values
        # df.columns = pd.MultiIndex.from_tuples(df.rename(columns=project_constant.COLUMN_NAME_LEVEL1_REPLACE))
        # df.columns.set_levels(project_constant.COLUMN_NAME_LEVEL1, level=1)
        # df = df.loc[df['dept'] == project_constant.DEPT, :]
        self.df = df[['name', 'date', 'day', 'time_in', 'time_out']]
        # self.df = self.groupColumn(self.df)
    def get_code_emp(self, val):
        arr = val.split()
        name = arr[len(arr) - 1]
        for i in range(0, len(arr) - 1):
            name += arr[i][0]
        return name.upper()

    def clean_data(self, name_select):
        df = self.df
        # Value not string
        # coln_not_str = pd.to_numeric(df['name'], errors='coerce').isna()
        # df = df.loc[coln_not_str, :]
        df['name'] = df['name'].apply(lambda x: unidecode(x))
        df['code'] = df['name'].apply(lambda x: self.get_code_emp(x))
        df = df.loc[(df['code'] == name_select) & (df['day'] != 'Chủ nhật'), :].copy()
        df.fillna('-', inplace=True)
        df['time_in'] = df['time_in'].apply(lambda x: x.replace('-', '00:00'))
        df['time_out'] = df['time_out'].apply(lambda x: x.replace('-', '00:00'))
        df['time_in'] = df['time_in'] + ':00'
        df['time_out'] = df['time_out'] + ':00'
        df['time_in'] = (pd.to_timedelta(df['time_in'].str.strip()))
        df['time_out'] = (pd.to_timedelta(df['time_out'].str.strip()))
        self.df = df
        return self.df
# data = data_collector(r'C:\Users\Windows 10\Desktop\Moi.xlsx')
# data.getData(header=[2])
# print(data.clean_data('MYTTD'))