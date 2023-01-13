import gspread
from typing import Dict, Union
import pandas as pd
import numpy as np
import os
from configparser import RawConfigParser
from mailchimp_auto.scripts.directory import *
import logging
import re
from mailchimp_auto.scripts.image_processor import upload_image

config = RawConfigParser()
config.read(template_config)

class getGspreadData: 
    def __init__(self, account_choice:str="", template_choice:str =""):
        """_summary_

        Args:
            credentials (dict, optional): Google Oauth2.0 JSON credentials in python dict instead of original json format. Defaults to credentials.
            user_authorized (dict, optional): authorized user's client id, client secret, etc in python dict format. Defaults to user_authorized.
        """
        self.account_choice = account_choice
        self.template_choice = template_choice
        self.spreadsheet_url = config.get(self.template_choice, "spreadsheet_url", fallback=None)
        self.sheet = self.access_spreadsheet()
    
    def access_spreadsheet(self):
        tpl_config = RawConfigParser()
        tpl_config.read(account_config)
        service_account_file_path = tpl_config.get(self.account_choice, "service_account_file_path", fallback=None)

        try:
            self.gc = gspread.service_account(filename=service_account_file_path) #oauth_from_dict(self.credentials, self.user_authorized)
            sheet = self.gc.open_by_url(self.spreadsheet_url)
        except gspread.exceptions.APIError as error:
            print(f"{error}")
            print("Please choose the Google account that has permission to open the spreadsheet!")
        logging.debug(f"The type of sheet object: {type(sheet)}")
        return sheet

    def get_campaign_info(self, worksheet_title:str, multiple_cell_ranges: Union[str, list]) -> Dict[str, str]: 
        """_summary_

        Args:
            worksheet_title (str): Google spreadsheet worksheet title
            multiple_cell_ranges (List[str]): Input Google spreadsheet's multiple cell ranges of 2 
                                            columns (dimension: i x 2) in list, e.g., ["A1:B6", "A8:B9", 
                                            "A11:B11"]
                                            
        Returns:
            Dict[str, str]: returns the dict key value pair whereby the key is the first column of 
            args: multiple_cell_ranges and the value is its second column. 
        """
        
        char_to_replace = {"\"": "", "\'":"", " ":"", "[":"", "]":""}
        multiple_cell_ranges = [x for x in str(multiple_cell_ranges).translate(str.maketrans(char_to_replace)).split(",")]
        
        worksheet_campaign = self.sheet.worksheet(worksheet_title)
        campaign_info_list = []
        campaign_info_dict = {}
        
        for cell_range in multiple_cell_ranges:
           campaign_info_list.extend(worksheet_campaign.get(cell_range))
        for index in campaign_info_list:
            try:
                campaign_info_dict.update({index[0]:index[1]})
            except IndexError:
                pass
        return campaign_info_dict
    
    def get_content_info(self, worksheet_title:str, multiple_cell_ranges: Union[str, list]):
        if type(multiple_cell_ranges) == "str":
            char_to_replace = {"\"": "", "\'":"", " ":"", "[":"", "]":""}
            multiple_cell_ranges = [x for x in multiple_cell_ranges.translate(str.maketrans(char_to_replace)).split(",")]
        
        worksheet_content_info = self.sheet.worksheet(worksheet_title)
        content_info_dict = dict()
        content_info_list = worksheet_content_info.batch_get(multiple_cell_ranges)

        for index in range(0, len(content_info_list), 1):
            section_name = content_info_list[index].pop(0)
            content_info_dict.update({section_name[0]: {}})  
            df = pd.DataFrame.from_records(content_info_list[index])
            header_row = df.iloc[0]
            df_with_header = pd.DataFrame(df.values[1:], columns=header_row)
            df_with_header.replace("", np.nan, inplace=True)
            df_with_header.dropna(axis=0, how="any", inplace=True)
            content_info_dict[section_name[0]].update(df_with_header.to_dict())
        
    
        #print(content_info_dict)
        #print("--------content info dict above------------")
                
        return content_info_dict