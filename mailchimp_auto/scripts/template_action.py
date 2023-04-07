from jinja2 import Environment, FileSystemLoader
from mailchimp_auto.scripts import directory
from mailchimp_auto.scripts.campaign_detail import Info
from configparser import RawConfigParser
import os
import logging
import mailchimp_marketing
from string import Template
from mailchimp_marketing.api_client import ApiClientError
import datetime
from mailchimp_auto.scripts.image_processor import update_image_link

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
    #updated_data = update_image_link(data, client)
    #print(data)
    #print(f"test template_loc1: {template_loc}")
    rendered = env.get_template(template_loc).render(**data)
    
    if preview:
        output_file: str = os.path.join(directory.output_folder, "index.htm")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Please check your generated template output at {output_file}")
        
    # ?? need to add this one? : Send data to mc:edit => https://stackoverflow.com/questions/29366766/mailchimp-api-not-replacing-mcedit-content-sections-using-ruby-library
    return rendered


def upload_template(template_name: str, html_code:str, client: type[mailchimp_marketing.Client]) -> int:
    """_summary_

    Args:
        html_code (_str_): _description_
        campaign_id (_str_): _description_
        client (_type_): _description_
    """
    string_template = Template(html_code).safe_substitute()
    
    try:
        response: dict = client.templates.create({"name": f"{template_name}_{datetime.datetime.now().strftime('%YY_%m_%d')}", "html": string_template})
        template_id: int = response["id"]
        logging.info(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    return template_id

# Get the sections that you can edit in a template, including each section's default content.
# https://mailchimp.com/developer/marketing/api/template-default-content/view-default-content/
def get_editable_content(template_id: int, client: type[mailchimp_marketing.Client]):
    try:
        response = client.templates.get_default_content_for_template(template_id)
        print(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))