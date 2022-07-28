from tempfile import template
from mailchimp_auto.scripts.gspread_data import *


# spreadsheet_url = "https://docs.google.com/spreadsheets/d/1h31GQRfBqUpMmPCXI013J1-Y-kinfgifN6Pa3dx3hB0/edit?usp=sharing"

def test_get_content_info():
    test = getGspreadData()
    test.access_spreadsheet(template_choice="MY_weekly_newsletter")
    print(test.get_content_info("Weekly Newsletter", ["A3:B5", "A7:H20"]))
    
test_get_content_info()