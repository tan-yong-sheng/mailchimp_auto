from string import Template
import os
import sys
import mailchimp_marketing
from mailchimp_auto.scripts.directory import *

#print(html_file)

#try:
#    html_code = open(html_file,"r", encoding="utf-8").read()
# except FileNotFoundError:
#    os.makedirs(os.path.dirname(html_file), exist_ok=True)
#    with open(html_file, "w"):
#        pass      
#    html_code = open(html_file,"r", encoding="utf-8").read()

def customized_template(html_code:str, campaign_id:str, client: mailchimp_marketing.Client) -> None:
    """_summary_

    Args:
        html_code (_str_): _description_
        campaign_id (_str_): _description_
        client (_type_): _description_
    """
    string_template = Template(html_code).safe_substitute()
    
    client.campaigns.set_content( campaign_id, {  
                                "html": string_template,
                                })
            