import json
import os
from email_service import send_verification_email  # Ensure this file is part of your Lambda deployment package

def lambda_handler(event, context):
    """
    Lambda handler for processing SNS messages and sending verification emails.
    """
    try:
        # Parse the SNS message
        record = event['Records'][0]
        message = json.loads(record['Sns']['Message'])

        email = message.get("email")
        token = message.get("verification_token")

        # Validate message payload
        if not email or not token:
            raise ValueError("Invalid payload: Missing required fields.")

        # Construct verification link
        base_url = os.getenv("BASE_URL", "http://dev.cloudsan.me")
        verification_link = f"{base_url}/verify?user={email}&token={token}"

        # Send the verification email
        send_verification_email(email, verification_link)

        # Log the successful operation (optional database logging can be added here)
        print(f"INFO: Verification email sent to {email}")

        return {"statusCode": 200, "body": "Verification email sent successfully."}

    except Exception as e:
        print(f"ERROR: Error processing SNS message: {e}")
        return {"statusCode": 500, "body": "Internal server error."}
