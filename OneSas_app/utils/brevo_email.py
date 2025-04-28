# utils/brevo_email.py
import os
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

def send_brevo_email(to_email, subject, html_content):
    """Send email via Brevo API"""
    config = Configuration()
    config.api_key['api-key'] = os.getenv('BREVO_API_KEY')
    
    # Initialize API client with the config
    api_client = ApiClient(config)
    api_instance = TransactionalEmailsApi(api_client)
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_name = os.getenv('SENDER_NAME')
    
    email = {
        'sender': {
            'email': sender_email,
            'name': sender_name
        },
        'to': [{'email': to_email}],
        'subject': subject,
        'htmlContent': html_content,
        'headers': {
            'X-Mailer': 'OneSasApp',
            'X-Priority': '1'
        }
    }
    
    try:
        # Debug: Print the API key prefix (don't log full key)
        print(f"Using API key: {config.api_key['api-key'][:10]}...") 
        
        api_response = api_instance.send_transac_email(email)
        print("Email sent! Message ID:", api_response.message_id)
        return True
    except ApiException as e:
        print("Brevo API Exception:")
        print("Status code:", e.status)
        print("Reason:", e.reason)
        print("Body:", e.body)
        return False