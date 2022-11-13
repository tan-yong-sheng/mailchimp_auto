from create_campaign import campaign_creation_function
import mailchimp_marketing


template_id = 13618381

client = mailchimp_marketing.Client()
client.set_config({
    "api_key": "d49b175e675ccea029bbe5beefad2e92-us1",
    "server": "us1"
    })
campaign_creation_function("TYONGSHENG", "my_weekly_newsletter", client=client, template_id=template_id)