import os
import requests

def send_verification_email(to_email, verification_link):
    """
    Send the verification email using SendGrid.
    """
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("EMAIL_FROM")  # Make sure to set this environment variable
    if not sendgrid_api_key:
        raise ValueError("SendGrid API key is missing. Set the SENDGRID_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": f"noreply@{os.getenv('ROUTE_NAME', 'demo')}.cloudsan.me"},
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
