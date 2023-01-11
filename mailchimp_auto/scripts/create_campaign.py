import mailchimp_marketing
import logging
from typing import Dict
from mailchimp_auto.scripts.campaign_detail import Info
from typing import Union, Optional

def campaign_creation_function(account_choice:str, template_choice: str,                              
                               client: type[mailchimp_marketing.Client], recipients_segment: Optional[Union[str,int]]=None, template_id: int=0
                               ) -> Dict:
    """_summary_

    :param account_choice: _description_
    :type account_choice: str
    :param template_choice: _description_
    :type template_choice: str
    :param recipients_segment: _description_
    :type recipients_segment: Union[str,int]
    :param client: _description_
    :type client: type[mailchimp_marketing.Client]
    :param template_id: _description_, defaults to 0
    :type template_id: int, optional
    :return: _description_
    :rtype: Dict
    """
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
        "tracking":
            {"opens": True,
             "html_clicks":True,
             "text_clicks":True,
             }
    }
    
    if recipients_segment:
        if isinstance(recipients_segment, str):
            data["settings"].update({"recipients":{"segment_opts": {"match": recipients_segment}}})
        if isinstance(recipients_segment, int):
            data["settings"].update({"recipients":{"segment_opts": {"saved_segment_id": recipients_segment}}})    
    if template_id:
        data["settings"].update({"template_id": template_id})
    
    new_campaign = client.campaigns.create(data)
    logging.debug("type of New campaign: " + str(type(new_campaign)))
    logging.debug(new_campaign)
    
    return new_campaign