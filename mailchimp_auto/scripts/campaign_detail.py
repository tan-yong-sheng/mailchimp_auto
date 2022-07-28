from mailchimp_auto.scripts.gspread_data import getGspreadData
from configparser import RawConfigParser
from mailchimp_auto.scripts.directory import *

config = RawConfigParser()
config.read(template_config)

class Info:    
    def __init__(self, account_choice:str, template_choice: str):
        self.template_choice = template_choice
        self.account_choice = account_choice
        self.gc = getGspreadData(account_choice=self.account_choice, template_choice=self.template_choice)
    
    def getCampaignInfo(self):
        self.worksheet_title_campaign_info = config.get(self.template_choice, "worksheet_title_campaign_info", fallback=None)
        self.campaign_info_cell_ranges = config.get(self.template_choice, "campaign_info", fallback=None)
        
        if len(self.campaign_info_cell_ranges) > 0:    
            char_to_replace = {"\"": "", "\'":"", " ":"", "[":"", "]":""}
            self.campaign_info_cell_ranges = [x for x in self.campaign_info_cell_ranges.translate(str.maketrans(char_to_replace)).split(",")]
               
        Worksheet_selected = self.gc.access_spreadsheet() # template_choice
        self.campaign_info = self.gc.get_campaign_info(worksheet_title=self.worksheet_title_campaign_info, multiple_cell_ranges=self.campaign_info_cell_ranges)
        return self.campaign_info
       
    def gethtmlContent(self):
        # Part 2: get html email content
        # self.campaign_info = self.campaign_detail.get_campaign_info(worksheet_title_campaign_info, multiple_cell_ranges_campaign_info)
        self.worksheet_title_campaign_content = config.get(self.template_choice, "worksheet_title_campaign_content", fallback=None)
        self.campaign_content_cell_ranges = config.get(self.template_choice, "campaign_content", fallback=None)
        
        char_to_replace = {"\"": "", "\'":"", " ":"", "[":"", "]":""}
        self.campaign_content_cell_ranges = [x for x in str(self.campaign_content_cell_ranges).translate(str.maketrans(char_to_replace)).split(",")] \
        
        self.data = self.gc.get_content_info(self.worksheet_title_campaign_content, self.campaign_content_cell_ranges)
        return self.data