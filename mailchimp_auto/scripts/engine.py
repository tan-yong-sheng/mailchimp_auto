# from mailchimp3 import MailChimp
import mailchimp_marketing
from mailchimp_auto.scripts.create_campaign import campaign_creation_function
from mailchimp_auto.scripts.template_action import generate_html_template, upload_template, get_editable_content
from mailchimp_auto.scripts.Config import *
from typing import Tuple
from mailchimp_auto.scripts.campaign_detail import *
import logging

# setup mailchimp account
def connect(account_username: str) -> Tuple[str, str]:
    config = read_config("account.conf")
    api_key = config.get(account_username, "api_key")
    server_prefix = config.get(account_username, "server_prefix")
    return api_key, server_prefix
    
# create new campaign
def create_new_campaign(account_username:str, template_name:str, preview:bool):
    """_summary_

    :param account_username: _description_
    :type account_username: str
    :param template_name: _description_
    :type template_name: str
    :param preview: _description_
    :type preview: bool

    Explanation: 
    # How to start this program
    `python mailchimpcamp.py` or `python mailchimpcamp.py run`
    
    # Processes being run:
    1. connect to your mailchimp account using API key.
    2. create a campaign under your certain audience list.
    3. generate a html template based on your google spreadsheet input.
    4. upload that html template to the mailchimp server as the campaign content.
    """
    
    if not preview:
        api_key, server_prefix = connect(account_username)
        # authenticate using mailchimp api and username
        client = mailchimp_marketing.Client()
        client.set_config({
            "api_key": api_key,
            "server": server_prefix,
            })

        # generate html template
        rendered_html = generate_html_template(account_choice=account_username, template_name = template_name)  # need to input template path
        
        
        # upload html template to mailchimp server
        template_id = upload_template(template_name = template_name, html_code=rendered_html, client=client)

        # create campaign
        campaign = campaign_creation_function(account_choice=account_username, 
                                            template_choice=template_name,
                                            client=client, template_id=template_id)
        
        logging.info(campaign["id"])
        
        get_editable_content(template_id=template_id, client=client)
    
    elif preview:
        rendered_html = generate_html_template(account_choice=account_username, template_name = template_name, preview=preview)