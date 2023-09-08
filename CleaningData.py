from CrawlData.CrawlData import data_collector
import pandas as pd
from GoogleSheet.GoogleSheetService import google_sheet
from Constant.ProjectConstant import project_constant as pjc

class cleaning_data(object):
    def __init__(self, json, link_file, ma_nv):
        self.gg_sheet = google_sheet(json)
        self.sheet = None
        self.data = data_collector(link_file)
        self.data.set_panda_options()
        self.data.getData(header=pjc.HEADER)
        self.df = self.data.clean_data(ma_nv)

    def get_sheet_google(self, name_work_book, name_of_sheet):
        self.sheet = self.gg_sheet.get_sheet(name_work_book=name_work_book, name_of_sheet=name_of_sheet)
        return self.sheet

    def processing_dataframe(self):
        self.df['time_late_in'] = self.df['time_in']
        self.df['time_late_out'] = self.df['time_out']
        self.df.loc[ (self.df['time_late_in'] > '08:00:00') & (self.df['time_in'] != '00:00:00'), ['time_late_in']] = \
            self.df.loc[self.df['time_late_in'] > '08:00:00', ['time_late_in']] - pd.to_timedelta('08:00:00'.strip())
        self.df.loc[(self.df['time_late_out'] < '17:00:00') & (self.df['time_out'] != '00:00:00'), ['time_late_out']] = \
            pd.to_timedelta('17:00:00'.strip()) - self.df.loc[self.df['time_late_out'] < '17:00:00', ['time_late_out']]

        self.df['date_to'] = self.df['date']
        self.df['name_temp'] = ''
        df_late_in = self.df.loc[
            (self.df['time_in'] > '08:00:00') & (self.df['time_in'] < '17:00:00') , ['time_in', 'date', 'time_late_in', 'code', 'day', 'name_temp', 'date_to']]
       
        df_late_out = self.df.loc[
            (self.df['time_out'] < '17:00:00' ) & (self.df['day'] != 'Thứ 7') , ['time_out', 'date', 'time_late_out', 'code', 'day', 'name_temp', 'date_to']]
  
        return df_late_in, df_late_out

    def late_two_hour(self):
        df_late_in, df_late_out = self.processing_dataframe()
        leave_two_hour_in = df_late_in.loc[
            (df_late_in['time_late_in'] > '01:30:00') & (df_late_in['time_late_in'] < '02:30:00'),
            ['code', 'date', 'day', 'name_temp', 'date_to']]

        leave_two_hour_out = df_late_out.loc[
            (df_late_out['time_late_out'] > '01:30:00') & (df_late_out['time_late_out'] < '02:30:00'),
            ['code', 'date', 'day', 'name_temp', 'date_to']]
        leave_two_hour = pd.concat([leave_two_hour_in, leave_two_hour_out], ignore_index = True)
        leave_two_hour.reset_index()     
        leave_two_hour['note'], leave_two_hour['num_hours'], leave_two_hour['loai_nghi'], leave_two_hour['ca'], leave_two_hour['cong'] = ['Nghỉ phép 2h', '2', 'NP', 'VP', 'P']

        return leave_two_hour

    def late_four_hour(self):
        df_late_in, df_late_out = self.processing_dataframe()
        leave_four_hour_in = df_late_in.loc[
            df_late_in['time_late_in'] > '03:00:00' , ['code', 'date', 'day', 'name_temp', 'date_to']]
        leave_four_hour_out = df_late_out.loc[
            df_late_out['time_late_out'] > '03:00:00', ['code', 'date', 'day', 'name_temp', 'date_to']]    
        leave_four_hour = pd.concat([leave_four_hour_in, leave_four_hour_out], ignore_index = True)  
        leave_four_hour.reset_index()        
        leave_four_hour['note'], leave_four_hour['num_hours'], leave_four_hour['loai_nghi'], leave_four_hour['ca'], \
        leave_four_hour['cong'] = ['Nghỉ phép 4h', '4', 'NP', 'VP', 'P']

        return leave_four_hour

    def late_entire_day(self):
        leave_entire_day = self.df.loc[
            (self.df['time_in'] == '00:00:00') & (self.df['time_out'] == '00:00:00'), ['code', 'date', 'day',
                                                                                       'name_temp', 'date_to']]
        leave_entire_day['note'], leave_entire_day['num_hours'], leave_entire_day['loai_nghi'], leave_entire_day['ca'], \
        leave_entire_day['cong'] = ['Nghỉ phép cả ngày', '8', 'NP', leave_entire_day['day'].apply(lambda x: 'T7' if x == 'Thứ 7' else 'VP'), 'P']
        leave_entire_day['num_hours'] = leave_entire_day['day'].apply(lambda x: '4' if x == 'Thứ 7' else '8')
        leave_entire_day['note'] = leave_entire_day['day'].apply(lambda x: 'Nghỉ phép thứ 7' if x == 'Thứ 7' else 'Nghỉ cả ngày')
        return leave_entire_day

    def miss_check_start_day(self):
        df_miss_check_start_day = self.df.loc[
            ((self.df['time_in'] == '00:00:00') & (self.df['time_out'] != '00:00:00')) | ((self.df['time_in'] >= '17:00:00') & (self.df['time_out'] == '00:00:00') ), ['code', 'date', 'day',
                                                                                       'name_temp', 'time_out', 'time_in',
                                                                                       'date_to']]
        df_miss_check_start_day['time_out'] = df_miss_check_start_day['time_in'].astype(str).map(
            lambda x: x[7:].replace(':00', ''))

        df_miss_check_start_day['note'], df_miss_check_start_day['time_in'], df_miss_check_start_day['ct_ca'], \
        df_miss_check_start_day['cong'] = ['Quên chấm công vào', '08:00', 'CH', 'QC']
        df_miss_check_start_day['ca'] = df_miss_check_start_day['day'].apply(lambda x: 'T7' if x == 'Thứ 7' else 'VP')
        return df_miss_check_start_day

    def miss_check_end_day(self):
        df_miss_check_end_day = self.df.loc[
            ((self.df['time_in'] != '00:00:00') & (self.df['time_in'] < '17:00:00'))  & (self.df['time_out'] == '00:00:00') , ['code', 'date', 'day',
                                                                                       'name_temp', 'time_in',
                                                                                       'date_to']]
        df_miss_check_end_day['time_in'] = df_miss_check_end_day['time_in'].astype(str).map(
            lambda x: x[7:].replace(':00', ''))
        df_miss_check_end_day['ca'] = df_miss_check_end_day['day'].apply(lambda x: 'T7' if x == 'Thứ 7' else 'VP')
        df_miss_check_end_day['note'], df_miss_check_end_day['time_out'], df_miss_check_end_day['ct_ca'], \
        df_miss_check_end_day['cong'] = ['Quên chấm công ra', '17:00', 'CH', 'QC']
        return df_miss_check_end_day

    def execute_google_sheet(self, dataframe, mode):
        self.gg_sheet.export_to_sheet(sheet=self.sheet, mode=mode, data_frame=dataframe)

    def execute_google_sheet_mutil(self, sheet, dataframe, mode, list_name_df, list_col):
        max_rows = len(sheet.get_all_values(major_dimension='rows'))
        for i in range(0, len(list_name_df)):
            self.gg_sheet.export_to_sheet_handle(sheet=sheet, mode=mode, data_frame=dataframe[[list_name_df[i]]],
                                                 max_rows=max_rows, col=list_col[i])
