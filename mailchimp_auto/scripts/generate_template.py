from jinja2 import Environment, FileSystemLoader
from mailchimp_auto.scripts import directory
from mailchimp_auto.scripts.campaign_detail import Info
from configparser import RawConfigParser
import os
import logging

config = RawConfigParser()
config.read(directory.template_config)


def generate_html_template(account_choice:str, template_name: str, 
                           input_fileName: str="master.htm",
                           preview: bool = False) -> None:
    """_summary_

    :param account_choice: _description_
    :type account_choice: str
    :param template_name: _description_
    :type template_name: str
    :param input_fileName: _description_, defaults to "master.htm"
    :type input_fileName: str, optional
    :param preview: _description_, defaults to False
    :type preview: bool, optional
    :return: _description_
    :rtype: _type_
    """
     
    #print(f"123 generate_html_content account_choice: {account_choice}")
    fileLoader = FileSystemLoader(searchpath=directory.template_folder)
    env = Environment(loader=fileLoader)
    
    # use json/csv and for loop to render
    template_loc = f"{template_name}/{input_fileName}"
    data=Info(account_choice=account_choice,template_choice=template_name).gethtmlContent()
    #print(data)
    #print(f"test template_loc1: {template_loc}")
    rendered = env.get_template(template_loc).render(**data)
    
    if preview:
        output_file = os.path.join(directory.output_folder, "index.htm")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Please check your generated template output at {output_file}")
        
    # ?? need to add this one? : Send data to mc:edit => https://stackoverflow.com/questions/29366766/mailchimp-api-not-replacing-mcedit-content-sections-using-ruby-library
    return rendered
