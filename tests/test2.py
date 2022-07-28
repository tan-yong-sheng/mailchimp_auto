from mailchimp_auto.scripts.campaign_detail import Info
from mailchimp_auto.scripts.gspread_data import getGspreadData

from configparser import RawConfigParser
from mailchimp_auto.scripts.directory import *

#a= Info(account_choice="TYONGSHENG", template_choice="my_weekly_newsletter")
# print(a.getCampaignInfo())
#print(a.gethtmlContent())
# print(type(a.gethtmlContent()))

tpl_config = RawConfigParser()
tpl_config.read(account_config)

service_account_file_path = tpl_config.get("TYONGSHENG", "service_account_file_path", fallback=None)

b = getGspreadData(account_choice = "TYONGSHENG", template_choice = "my_weekly_newsletter")  
Campaign = b.access_spreadsheet()
print(b.get_campaign_info(worksheet_title="Campaign Info", multiple_cell_ranges=["A1:B6", "A8:B9", "A11:B11"]))



