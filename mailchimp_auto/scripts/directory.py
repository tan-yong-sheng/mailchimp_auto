import os
import pathlib

home_path = pathlib.Path.home()
mailchimp_auto_folder = os.path.join(home_path, "Documents", "mailchimp-auto")
template_folder = os.path.join(mailchimp_auto_folder, "template")
config_folder = os.path.join(mailchimp_auto_folder, ".config")
service_account_folder = os.path.join(config_folder, "service_account_file")
output_folder = os.path.join(mailchimp_auto_folder, "output")

authorized_user_file = os.path.join(config_folder, "authorized_user.json")
template_config = os.path.join(config_folder, "template.conf")
account_config = os.path.join(config_folder, "account.conf")


def create_dir():
    os.makedirs(mailchimp_auto_folder, exist_ok=True) # create app path to store html email template and json credentials
    os.makedirs(template_folder, exist_ok=True)
    os.makedirs(service_account_folder, exist_ok =True)
    os.makedirs(service_account_folder, exist_ok=True)
    os.makedirs(output_folder)

def create_file(file:str):
    if not os.path.isfile(file):
        with open(file, "w"):
            pass 
        
def create_files(*files):
    for file in files:
        create_file(file)
        
