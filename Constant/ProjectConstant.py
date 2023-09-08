class project_constant(object):
    DISPLAY_MAX_ROW = 1000
    DISPLAY_MAX_WIDTH = 1000
    DISPLAY_MAX_COLUMN = None
    DEPT = 'FSD'
    HEADER = [2]
    COLUMN_NAME_REPLACE = {'Tên nhân viên': 'name', 'Mã nhân viên': 'emp', 'STT': 'stt', 'Phòng ban': 'dept', 'Ngày': 'date',
                     'Thứ': 'day', 'Giờ vào': 'time_in', 'Giờ ra': 'time_out'}
    COLUMN_NAME_LEVEL1 = ['', 'date_in', 'time_in', 'date_out', 'time_out']
    COLUMN_NAME_LEVEL1_REPLACE = {('in', 'Ngày'): ('in', 'date_in'), ('in', 'Giờ'): ('in', 'time_in'),
                     ('out', 'Ngày'): ('out', 'date_out'), ('out', 'Giờ'): ('out', 'time_out')}
    SCOPE = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

