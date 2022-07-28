# from mailchimp3 import MailChimp
import mailchimp_marketing
from mailchimp_auto.scripts.create_campaign import campaign_creation_function
from mailchimp_auto.scripts.load_newsletter_template import customized_template # html_code is a variable
from mailchimp_auto.scripts.template import generate_html_template
from mailchimp_auto.scripts.Config import *
from typing import Tuple
from mailchimp_auto.scripts.campaign_detail import *

# setup mailchimp account
def connect(account_username: str) -> Tuple[str, str]:
    config = read_config("account.conf")
    api_key = config.get(account_username, "api_key")
    server_prefix = config.get(account_username, "server_prefix")
    return api_key, server_prefix
    
# create new campaign
def create_new_campaign(account_username:str, template_name:str):
    """_summary_
    #How to start this program
    `python mailchimpcamp.py` or `python mailchimpcamp.py run`
    
    #Processes being run:
    1. connect to your mailchimp account using API key.
    2. create a campaign under your certain audience list.
    3. generate a html template based on your google spreadsheet input.
    4. upload that html template to the mailchimp server as the campaign content.
    """
    api_key, server_prefix = connect(account_username)
    # authenticate using mailchimp api and username
    client = mailchimp_marketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": server_prefix,
        })

    # create campaign
    campaign = campaign_creation_function(account_choice=account_username, 
                                          template_choice=template_name,
                                        client=client)

    # generate html template
    rendered_html = generate_html_template(account_choice=account_username, template_name = template_name)  # need to input template path

    # upload the html template to the campaign
    customized_template(html_code=rendered_html, campaign_id=campaign["id"], client=client)