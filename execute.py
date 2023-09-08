
import CleaningData as cl
import pandas as pd
from threading import Thread, Lock
import os
link = ''

while True:
    link = input("Nhập tên tệp tin (xlsx): ")
    if link.endswith(".xlsx") and os.path.isfile(link):
        break
    else:
        print("Tệp tin phải là là .xls")

name_emp = input('Mã nhân viên: ')

obj = cl.cleaning_data(json='Dattestsheet.json', ma_nv=name_emp, link_file=link)
# obj = cl.cleaning_data(json='Dattestsheet.json', ma_nv='DATNH', link_file=r'C:\Users\Admin\Desktop\T9 01 30.xls')

obj.processing_dataframe()
late_four_hour = obj.late_four_hour()
late_two_hour = obj.late_two_hour()

late_entire_day = obj.late_entire_day()
miss_check_start_day = obj.miss_check_start_day()
miss_check_end_day = obj.miss_check_end_day()
miss_check = pd.concat([miss_check_start_day, miss_check_end_day]).sort_values(by='date')
late = pd.concat([late_two_hour, late_four_hour, late_entire_day]).sort_values(by='date')
# Sheet

# sheet = obj.get_sheet_google(name_work_book='Dattest', name_of_sheet='Sheet2')
late['date'] = pd.to_datetime(late['date']).dt.strftime('%d/%m/%Y')
late['date_to'] = pd.to_datetime(late['date_to']).dt.strftime('%d/%m/%Y')
miss_check['date'] = pd.to_datetime(miss_check['date']).dt.strftime('%d/%m/%Y')
miss_check['date_to'] = pd.to_datetime(miss_check['date_to']).dt.strftime('%d/%m/%Y')
print(late)
print(miss_check)


def write_to_sheet_check():
    sheet = obj.get_sheet_google(name_work_book='FSD Group info', name_of_sheet='Chấm công')
    obj.execute_google_sheet_mutil(sheet = sheet, dataframe=miss_check, mode='a',
                                   list_name_df=['code', 'date', 'ca', 'ct_ca', 'cong', 'time_in', 'time_out', 'note'],
                                   list_col=[2, 5, 6, 7, 8, 9, 11, 17])


def write_to_sheet_late():
    sheet = obj.get_sheet_google(name_work_book='FSD Group info', name_of_sheet='Nghỉ phép')
    obj.execute_google_sheet_mutil(sheet = sheet, dataframe=late, mode='a',
                                   list_name_df=['code', 'date', 'date', 'loai_nghi', 'ca', 'cong', 'num_hours',
                                                 'note'],
                                   list_col=[2, 4, 5, 6, 7, 8, 9, 11])
Thread(target=write_to_sheet_check).start()
Thread(target=write_to_sheet_late).start()
