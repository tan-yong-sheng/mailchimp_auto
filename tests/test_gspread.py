from mailchimp_auto.scripts.gspread_data import *

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1h31GQRfBqUpMmPCXI013J1-Y-kinfgifN6Pa3dx3hB0/edit?usp=sharing"

def test_get_campaign_info():
    #test = getGspreadData()
    #test.access_spreadsheet(spreadsheet_url)
    #print(test.get_campaign_info("Campaign Info", ["A1:B6", "A8:B9", "A11:B11"]))
    pass

def test_get_content_info():
    test = getGspreadData(account_choice="TYONGSHENG", template_choice="my_weekly_newsletter")
    test.access_spreadsheet()
    print(test.get_content_info("Weekly Newsletter", ["A3:B5", "A7:H20"]))
