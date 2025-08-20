# core/sqs.py

import os
import boto3
import json
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

load_dotenv()

# Load SQS configuration
AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize the SQS client
sqs_client = boto3.client(
    "sqs",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def publish_to_analysis_queue(message: dict):
    """
    Publishes a message to the SQS analysis queue.
    Used to trigger downstream ML/LLM analysis of submitted answers.
    """
    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message)
        )
        return {
            "message": "Message sent to queue",
            "message_id": response.get("MessageId")
        }
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Failed to send message to SQS: {str(e)}")
