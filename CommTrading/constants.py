import os

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_DIRECTORY = os.path.join(APP_DIRECTORY, 'comm_trading_demo.csv')
LOGO_DIRECTORY = os.path.join(APP_DIRECTORY, 'logo.png')

TRADING_FLOW_COLORS = {'Export': '#1500FF', 'Re-Export': '#3B98F5', 'Import': '#FF8C00', 'Re-Import': '#F5D700'}
DASHBOARD_MAIN_COLOR1 = '#0096eb'
MAIN_HEADER_BG = '#01012c'
APP_BG = '#EBECF0'