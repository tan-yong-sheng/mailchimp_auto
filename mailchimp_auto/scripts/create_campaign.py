import mailchimp_marketing
import logging
from typing import Dict
from mailchimp_auto.scripts.campaign_detail import Info


def campaign_creation_function(account_choice:str, template_choice: str,                                
                               client: type[mailchimp_marketing.Client]) -> Dict:
    
    tpl = Info(account_choice = account_choice, template_choice=template_choice)
    
    data = {
        "type": "regular",
        "recipients" :
        {
            "list_id": tpl.getCampaignInfo()["list_id"],
        },
        "settings":
        {
            "subject_line": tpl.getCampaignInfo()["subject_line"],
            "preview_text": tpl.getCampaignInfo()["preview_text"],
            "title":tpl.getCampaignInfo()["campaign_title"],
            "from_name": tpl.getCampaignInfo()["from_name"],
            "to_name": tpl.getCampaignInfo()["to_name"], 
            "reply_to": tpl.getCampaignInfo()["reply_to"],
        },
    }
    
    new_campaign = client.campaigns.create(data)
    logging.debug("type of New campaign: " + str(type(new_campaign)))
    logging.debug(new_campaign)
    
    return new_campaign