import os
import json
from email_service import send_verification_email

def lambda_handler(event, context):
    try:
        # Parse the event
        record = event['Records'][0]
        message = json.loads(record['Sns']['Message'])
        email = message.get("email")
        token = message.get("verification_token")

        if not email or not token:
            raise ValueError("Invalid payload: Missing email or token.")

        # Construct the verification link
        base_url = os.getenv("BASE_URL", "http://dev.cloudsan.me")
        verification_link = f"{base_url}/verify?user={email}&token={token}"

        # Send the email
        print(f"INFO: Sending email to {email}")
        send_verification_email(email, verification_link)

        return {"statusCode": 200, "body": "Verification email sent successfully."}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"statusCode": 500, "body": "Internal server error."}
