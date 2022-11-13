import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


# add template
file_path = r"C:\Users\tys\Documents\mailchimp-auto\output\index.htm"

with open(file_path,"r",encoding="utf-8") as file:
    html_content = file.read()

try:
  client = MailchimpMarketing.Client()
  client.set_config({
    "api_key": "d49b175e675ccea029bbe5beefad2e92-us1",
    "server": "us1"
  })

  response = client.templates.create({"name": "Freddie's Jokes", "html": html_content})
  print(response)
except ApiClientError as error:
  print("Error: {}".format(error.text))
  
  
# update template? -> e.g.,


# list down all template