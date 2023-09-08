import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
from Constant.ProjectConstant import project_constant

class google_sheet(object):
    def __init__(self, json):
        self.screds = ServiceAccountCredentials.from_json_keyfile_name(json, project_constant.SCOPE)
        self.client = gs.authorize(self.screds)
        self.sheet = None

    def get_sheet(self, name_work_book, name_of_sheet):
        self.sheet = self.client.open(name_work_book).worksheet(name_of_sheet)
        return self.sheet

    def export_to_sheet(self, sheet, data_frame, mode='r'):
        if mode == 'a':
            max_rows = len(sheet.get_all_values(major_dimension='rows'))
            gd.set_with_dataframe(worksheet=sheet, dataframe=data_frame, include_index=False, row=max_rows + 1,
                                  include_column_header=False, resize=False)
        if mode == 'w':
            sheet.clear()
            gd.set_with_dataframe(worksheet=sheet, dataframe=data_frame, include_index=False,
                                  include_column_header=True,
                                  resize=True)
        else:
            return gd.get_as_dataframe(worksheet=sheet)

    def export_to_sheet_handle(self, sheet, data_frame, mode='r', col=1, max_rows=0):
        if mode == 'a':
            gd.set_with_dataframe(worksheet=sheet, dataframe=data_frame, include_index=False, row=max_rows + 1, col=col,
                                  include_column_header=False, resize=False)
        if mode == 'w':
            sheet.clear()
            gd.set_with_dataframe(worksheet=sheet, dataframe=data_frame, include_index=False,
                                  include_column_header=True, col=col,
                                  resize=True)
        else:
            return gd.get_as_dataframe(worksheet=sheet)
