import os
import boto3
import requests
import json

# Initialize AWS Secrets Manager client
secrets_client = boto3.client('secretsmanager')

def get_secret(secret_name):
    """
    Fetch a secret from AWS Secrets Manager.
    """
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret
    except Exception as e:
        print(f"ERROR: Failed to retrieve secret {secret_name}: {e}")
        raise e

def send_verification_email(to_email, verification_link):
    """
    Send the verification email using SendGrid.
    """
    # Fetch email service credentials from Secrets Manager
    secret_name = os.getenv("EMAIL_SECRET_NAME", "email-service-secret")
    credentials = get_secret(secret_name)

    # Extract credentials
    sendgrid_api_key = credentials.get("SENDGRID_API_KEY")
    email_from = credentials.get("EMAIL_FROM")

    if not sendgrid_api_key or not email_from:
        raise ValueError("Missing required email service credentials.")

    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": email_from},
        "subject": "Verify Your Email",
        "content": [
            {
                "type": "text/plain",
                "value": f"Please verify your email by clicking this link: {verification_link}"
            }
        ]
    }

    response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)

    if response.status_code != 202:
        raise Exception(f"Failed to send email: {response.status_code}, {response.text}")

    print(f"INFO: Email sent successfully to {to_email}")
