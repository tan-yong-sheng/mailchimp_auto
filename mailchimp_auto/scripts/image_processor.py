
import requests
import mailchimp_marketing
from mailchimp_marketing.api_client import ApiClientError
import base64
import re

def upload_image(image_url:str, client: mailchimp_marketing.Client) -> None:
    try:
        file_data = base64.b64encode(requests.get(image_url).content).decode('utf8')

        response = client.fileManager.upload(
            {"name": image_url.replace("https://","")+".jpg", # image name
            "file_data": file_data,
            }
        )

        #print(response)
        #print("Image URL:", response["full_size_url"]) # get image full size url
        return response["full_size_url"]
        
    except ApiClientError as error:
        print("Error: {}".format(error.text))

def update_image_link(content_info_dict:dict, client: mailchimp_marketing.Client):
    # change the previous link inside the content_info_dict to image link uploaded to mailchimp server 

    for dict_key, dict_val in content_info_dict.items():      
        for dict_key_l2, dict_val_l2 in dict_val.items():
            if re.search("image", dict_key_l2):
                for dict_key_l3, dict_val_l3 in dict_val_l2.items():
                    uploaded_image_url = upload_image(dict_val_l3, client)
                    content_info_dict[dict_key][dict_key_l2].update({dict_key_l3: uploaded_image_url})
    #print("version 2 data")
    #print(content_info_dict)
    #print("-----------------version 2 data---------")
    
    return content_info_dict