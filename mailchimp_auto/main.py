import typer
from mailchimp_auto.scripts import directory, engine
import logging
from mailchimp_auto.scripts import Config
from mailchimp_auto.scripts.template_Config import Configuration
from mailchimp_marketing.api_client import ApiClientError
import os

logging.basicConfig(level=logging.CRITICAL, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(level=logging.CRITICAL)

app = typer.Typer()

@app.command(short_help="Upload html email template to mailchimp server and create a campaign.")
def create(user: str = typer.Option(..., help="Input your Mailchimp Username here!"), 
           template: str = typer.Option(..., help="Input your template choice here!")):
    try:    
        engine.connect(account_username = user)
        engine.create_new_campaign(account_username = user,template_name=template)
        logging.info("The task has been completed!")
    except ApiClientError as error:
        typer.echo("Error: {}".format(error.text))
        typer.echo("Please run `python -m auto_mailchimp config` to check your mailchimp API, server prefix!")        
    
@app.command(short_help="Setup Mailchimp API, Mailchimp server prefix, Google Service account's json file, MUST SETUP this first before running this program")
def config():
    Config.config_page()
        
@app.command(short_help="To check your account config file, either account config file or template config file.")
def config_file(config_file_type:str=typer.Argument(..., help="Choose either `account` or `template` to see its config file location.")):
    account_config_path = Config.config_file_path()
    template_config_path = directory.template_config
    if config_file_type =="account" and os.path.isfile(account_config_path):        
        print(account_config_path)
    elif config_file_type =="template" and os.path.isfile(template_config_path):
        print(template_config_path)
    else:
        print(f"The {config_file_type} config file is not created yet.")

@app.command(short_help="Setup Google spreadsheet, campaign info and its email content.")
def config_template():
    template_setting = Configuration("template")
    template_setting.config_page()
    
if __name__ == "__main__": 
    app()