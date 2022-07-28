from configparser import RawConfigParser
import os
import shutil
from mailchimp_auto.scripts.directory import *
from mailchimp_auto.scripts.directory import create_dir


conf = RawConfigParser()

def config_page():
    create_dir()
    action_selected = select_action() #choose which action to do (e.g., new, edit, delete)
    account_selected = select_account(action_selected) # choose which account you want to deal with
    write_config(action_choice=action_selected, account_choice=account_selected)
    
def select_action():
    # run config page
    print("\nCurrent Mailchimp remote:")
    print("Account Username\tServer Prefix")
    print("=================\t=============")
    
    # read_config("account.conf").sections() != ["settings"] and 
    if len(read_config("account.conf""account.cof").sections()) > 0:
        for account in read_config("account.conf""account.conf").sections():
            print(str(account), "\t\t", str(read_config("account.conf").get(account, "server_prefix", fallback=None)))
    print("\n")
    print("e) Edit existing account")
    print("n) New account")
    print("d) Delete account")
    print("q) quit")
    
    acceptable_choices = ["e","n","d", "q"]
    action_choice = input("e/n/d/q > ")
    while action_choice not in acceptable_choices:
        print("This value must be a single character, one of the following: e, n, d, q")
        action_choice = input("e/n/d/q > ")
    return action_choice

def select_account(act_choice: str) -> str:
    if act_choice == "q":
        pass
    
    elif act_choice != "n" and  len(read_config("account.conf").sections()):
        print("\nSelect account.")
        print("Choose a number from below, or type in an existing value.")
        
        for index, account in enumerate(read_config("account.conf").sections()):
            print(index+1, "> ", account)
        
        acceptable_choices = [account for account in read_config("account.conf").sections()]
        acceptable_choices.extend([str(index) for index in range(1, len(read_config("account.conf").sections())+1, 1)])    
        act_choice = input("Account > ")
        
        while act_choice not in acceptable_choices:
            print("No choices with your input.")
            act_choice = input("Account > ")
        try: 
            act_choice = read_config("account.conf").sections()[int(act_choice)-1] # try else
        except ValueError:
            pass
    return act_choice
    
def write_config(config_file: str = "account.conf", action_choice: str = "", account_choice: str = ""):
    config_file = os.path.join(config_folder, config_file)
    path = config_file_path(config_file)
    conf.read(path)
    
    if action_choice == "d" and len(read_config("account.conf").sections()) > 0: # delete the entry
        conf.remove_section(account_choice)
        with open(path, 'w') as configfile:
            conf.write(configfile)
            
        sa_file_name = str(account_choice) + ".json" 
        sa_full_file_name = os.path.join(service_account_folder, sa_file_name)
        os.unlink(sa_full_file_name)
            
    elif action_choice in ["e", "n"]: # edit(e) or create (n) the config file
        api_key = conf.get(account_choice, "api_key", fallback=None)
        server_prefix = conf.get(account_choice, "server_prefix", fallback=None)
        #print(f"api_key1: {api_key}")
        #print(f"server prefix1: {server_prefix}")        
        
        if action_choice == "n": # create new section (n)
            account_choice = input("\nEnter username of Mailchimp Account.\nname: ")
            conf.add_section(account_choice)
            #print(f"api_key2: {api_key}") 
            main_config(api_key=api_key, server_prefix = server_prefix, account_choice = account_choice)            
        elif action_choice == "e" and len(read_config("account.conf").sections()) > 0:
            main_config(api_key=api_key, server_prefix = server_prefix, account_choice = account_choice)
        else:
            print("No account to edit!")
    
    elif action_choice == "q":
        pass
    
    else: 
        print("No account to delete!")
        
def read_config(config_file: str = "account.conf") -> type[RawConfigParser]:
    config_file = os.path.join(config_folder, config_file)
    path = config_file_path(config_file)
    conf.read(path)
    return conf

def config_file_path(config_file: str = "account.conf") -> type[RawConfigParser]:
    config_file = os.path.join(config_folder, config_file)
    return config_file

def main_config(api_key, server_prefix, account_choice):
    sa_file_name = str(account_choice) + ".json" 
    dirname=os.path.dirname
    sa_full_file_name = os.path.join(service_account_folder, sa_file_name)

    # Step 1: Setup Mailchimp API
    path = config_file_path()
    
    new_api_key = input(f"\nMailchimp API\nEnter a string value. Press Enter for the default ({api_key}): ")
    new_api_key = api_key if len(new_api_key) == 0 else new_api_key
        
    # Step 2: Setup Mailchimp Server Prefix
    new_server_prefix = new_api_key.rsplit("-")[1]
    # new_server_prefix = input(f"\nServer Prefix (e.g. us1, us9)\nEnter a string value. Press Enter for the default ({server_prefix}): ")
    new_server_prefix = server_prefix if len(new_server_prefix) == 0 else new_server_prefix
        
    # Step 3: Setup Google Service Account
    gs_account_json = conf.get(account_choice, "service_account_file_path", fallback=None)     
    new_gs_account_json = input(f"\nService_account_file.\nGoogle Service Account Credentials JSON file path.\nEnter a string value. Press Enter for the default ({gs_account_json}): ")
    
    while len(new_gs_account_json) != 0 and new_gs_account_json.replace("\"", "").rsplit(".", 1)[1] != "json":
        print("The file format should end with .json format!")
        new_gs_account_json = input("Please re-insert again Google Service Account Credentials JSON file path: ")

    new_gs_account_json = gs_account_json if len(new_gs_account_json) == 0 else new_gs_account_json
    
    try:
        shutil.copy(new_gs_account_json.replace("\"", ""), sa_full_file_name)
        print(f"\nGoogle service account file (in json format) is copied to {sa_full_file_name}.")
    except shutil.SameFileError:
        pass      
    
    # Step 4: Write the changes into account.conf file
    conf.set(account_choice, "api_key", new_api_key)
    conf.set(account_choice, "server_prefix", new_server_prefix)
    conf.set(account_choice, "service_account_file_path", sa_full_file_name)
    
    with open(path, 'w') as configfile:
        conf.write(configfile)