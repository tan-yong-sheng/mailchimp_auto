# mailchimp_auto

**auto_mailchimp** is a command line application to automate the email creation process on MailChimp based on the google spreadsheet input. What it does is using Jinja2 template engine to loop over dummy values (e.g., website url, image url, string) on html template in order to create the html template to be uploaded to MailChimp server.

(Note: This project is highly customized for personal use, but it's okay for reference.)

----
## Installing

`pip install auto_mailchimp`

---
## Configuration
Setup Mailchimp API, Mailchimp server prefix, Google Service account's json file, MUST SETUP this first before running this program.

`python -m auto_mailchimp.py config`