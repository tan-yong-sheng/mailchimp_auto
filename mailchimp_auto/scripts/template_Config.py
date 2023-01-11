from configparser import RawConfigParser
from genericpath import exists
import os
import shutil
from mailchimp_auto.scripts import directory
from gspread.utils import extract_id_from_url
import logging

conf = RawConfigParser()

class Configuration:
    def __init__(self, subject:str):
        self.subject = subject
        
    def select_action(self): # select_tempate in template_Config.py or select_action
        # Step 0: print out something
        print("Current template(s):")
        print("Template\t\t\tSpreadsheet Id")
        print("========\t\t\t===============")
        
        if len(self.read_config().sections()) > 0:
            for template_folder_name in self.read_config().sections():
                print(str(template_folder_name), "\t\t", extract_id_from_url(str(self.read_config().get(template_folder_name, "spreadsheet_url", fallback=None))))
           
        print("\n")
        print(f"e) Edit existing {self.subject}")
        print(f"n) New {self.subject}")
        print(f"d) Delete {self.subject}")
        print("q) quit")
        
        acceptable_choices = ["e","n","d", "q"]
        action_choice = input("e/n/d/q > ")
        while action_choice not in acceptable_choices:
            print("This value must be a single character, one of the following: e, n, d, q")
            action_choice = input("e/n/d/q > ")
        return action_choice

    def select_template(self, act_choice: str) -> str:  
        tpl_choice = None #to avoid outbound error
        
        if act_choice == "q":
            pass
        
        elif act_choice in ["e","d"] and len(self.read_config().sections()) > 0:
            print(f"\nSelect {self.subject}.")
            print("Choose a number from below, or type in an existing value.")
            
            for index, conf_variable in enumerate(self.read_config().sections()):
                print(index+1, "> ", conf_variable)
            
            acceptable_choices = [conf_variable for conf_variable in self.read_config().sections()]
            acceptable_choices.extend([str(index) for index in range(1, len(self.read_config().sections())+1, 1)])    
            tpl_choice = input(f"{self.subject.title()} > ")
            
            while tpl_choice not in acceptable_choices:
                print("No choices with your input.")
                tpl_choice = input(f"{self.subject.title()} > ")
            try: 
                tpl_choice = self.read_config().sections()[int(tpl_choice)-1] # try else
            except ValueError:
                pass
            
        elif act_choice == "n":
            tpl_choice = input(f"\nEnter name of new {self.subject}.\nname: ")
            
        return tpl_choice
            
    def read_config(self, config_file: str = "template.conf") -> type[RawConfigParser]: #ok
        config_file = os.path.join(directory.config_folder, config_file)
        self.path = self.config_file_path(config_file)
        conf.read(self.path)
        return conf
    
    def write_config(self, config_file: str = "template.conf", action_choice: str = "", template_choice: str = ""):
        config_file = os.path.join(directory.config_folder, config_file)
        path = self.config_file_path(config_file)
        conf.read(path)
        
        if action_choice == "d" and len(self.read_config().sections()) > 0: # delete the entry
            conf.remove_section(template_choice)
            with open(path, 'w') as configfile:
                conf.write(configfile)
                
            # remove template folder
            shutil.rmtree(os.path.join(directory.template_folder, template_choice))
                
        elif action_choice in ["e", "n"]: # edit(e) or create (n) the config file            
            if action_choice == "n": # create new section (n)
                conf.add_section(template_choice)
                self.main_config(template_choice = template_choice, action_choice = action_choice)            
            elif action_choice == "e" and len(self.read_config().sections()) > 0:
                self.main_config(template_choice = template_choice, action_choice = action_choice)
            else:
                print(f"No {self.subject} to edit!")
        
        elif action_choice == "q":
            pass
        
        else: 
            print(f"No {self.subject} to delete!")


    def config_file_path(self, config_file: str = "template.conf") -> type[RawConfigParser]:
        config_file = os.path.join(directory.config_folder, config_file)
        return config_file
    
    def copy_template_folder(self, action_choice: str, template_folder_name:str): # specific to template_Config.py        
        if action_choice == "n" or action_choice == "e":
            template_folder_dir = conf.get(template_folder_name, "template_folder_dir", fallback=None)
            new_template_folder_dir = input(f"\nTemplate folder.\nThe file path of the HTML email template folder.\nEnter a string value. Press Enter for the default ({template_folder_dir}): ")
            print(os.path.isdir(new_template_folder_dir.replace("\"", "")))
                
            while not os.path.isdir(new_template_folder_dir.replace("\"", "")) and len(new_template_folder_dir) > 0: # got problem
                print("Please enter a valid template folder path: ")
                new_template_folder_dir = input(f"\nTemplate folder.\nThe file path of the HTML email template.\nEnter a string value. Press Enter for the default ({template_folder_dir}): ")
            new_template_folder_dir = new_template_folder_dir.replace("\"", "")
            new_template_folder_dir = template_folder_dir if len(new_template_folder_dir) == 0 else new_template_folder_dir
            #print(new_template_folder_dir)
            
            #print(f"name2: {template_folder_name}")
            template_loc = os.path.join(directory.template_folder, template_folder_name)
            #print(template_loc)
            
            try:
                shutil.copytree(new_template_folder_dir, template_loc)
                print(f"\nYour file is copied and uploaded to {template_loc}.")
            except shutil.SameFileError:
                pass
            except FileExistsError:
                pass
            
            # Step 4: Write the changes into template.conf file      
            conf.set(template_folder_name, "template_folder_dir", template_loc)
            self.path = self.config_file_path("template.conf")
            with open(self.path, 'w') as configfile:
                conf.write(configfile)
    
    def setup_Spreadsheet(self, template_selected: str):
        self.spreadsheet_url = conf.get(template_selected, "spreadsheet_url", fallback=None)
        new_spreadsheet_url = input(f"\nSpreadsheet url.\nThe Google spreadsheet url that you want to parse it to the Jinja2 HTML email template: .\nEnter a string value. Press Enter for the default ({self.spreadsheet_url}): ")
        new_spreadsheet_url = self.spreadsheet_url if len(new_spreadsheet_url) == 0 else new_spreadsheet_url
        conf.set(template_selected, "spreadsheet_url", new_spreadsheet_url)
        with open(self.path, 'w') as configfile:
            conf.write(configfile)
    
    def setup_campaign(self, template_selected:str):
        worksheet_title_campaign_info = conf.get(template_selected, "worksheet_title_campaign_info", fallback="Campaign Info")
        new_worksheet_title_campaign_info = input(f"\nWorksheet Title of Campaign Info.\nThe worksheet title of campaign info: .\nEnter a series of cell ranges, separated by symbol (,). Press Enter for the default ({worksheet_title_campaign_info}): ")
        new_worksheet_title_campaign_info = worksheet_title_campaign_info if len(new_worksheet_title_campaign_info) == 0 else new_worksheet_title_campaign_info
        
        campaign_info = conf.get(template_selected, "campaign_info", fallback=None)
        new_campaign_info = input(f"\nCampaign Info.\nThe Campaign info that you want to parse it to the Jinja2 HTML email template: .\nEnter a series of cell ranges, separated by symbol (,). Press Enter for the default ({campaign_info}): ")
        new_campaign_info = campaign_info if len(new_campaign_info) == 0 else new_campaign_info
            
        worksheet_title_campaign_content = conf.get(template_selected, "worksheet_title_campaign_content", fallback="Campaign Content")
        new_worksheet_title_campaign_content = input(f"\nWorksheet Title of Campaign Content.\nThe worksheet title of campaign content: .\nEnter a series of cell ranges, separated by symbol (,). Press Enter for the default ({worksheet_title_campaign_content}): ")
        new_worksheet_title_campaign_content = worksheet_title_campaign_content if len(new_worksheet_title_campaign_content) == 0 else new_worksheet_title_campaign_content
       
        campaign_content = conf.get(template_selected, "campaign_content", fallback=None)
        new_campaign_content = input(f"\nCampaign Content.\nThe Campaign Content that you want to pass it to the Jinja2 HTML email template: .\nEnter a series of cell ranges, separated by symbol (,). Press Enter for the default ({campaign_content}): ")
        new_campaign_content = campaign_content if len(new_campaign_content) == 0 else new_campaign_content
        
        conf.set(template_selected, "worksheet_title_campaign_info", new_worksheet_title_campaign_info)
        conf.set(template_selected, "worksheet_title_campaign_content", new_worksheet_title_campaign_content)
        conf.set(template_selected, "campaign_info", new_campaign_info)
        conf.set(template_selected, "campaign_content", new_campaign_content)
        with open(self.path, 'w') as configfile:
            conf.write(configfile)
            
    def config_page(self): 
        directory.create_dir()
        action_selected = self.select_action()
        #print(f"action_selected1: {action_selected}")
        template_selected = self.select_template(act_choice=action_selected)
        #print(f"template_selected: {template_selected}")
        self.write_config(action_choice=action_selected, template_choice=template_selected)
       
    def main_config(self, template_choice:str, action_choice:str):
        # Step 1: Upload template
        self.copy_template_folder(template_folder_name = template_choice, action_choice = action_choice)
        
        # Step 2: Setup spreadsheet url
        self.setup_Spreadsheet(template_selected = template_choice)
        
        # Step 3: setup campaign info & campaign content
        self.setup_campaign(template_selected= template_choice)
        
        