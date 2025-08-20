import boto3
import os
from dotenv import load_dotenv
import json

load_dotenv()

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

REPORT_QUEUE_URL = os.getenv("REPORT_QUEUE_URL")

def send_message_to_report_queue(message_body: dict):
    """
    Push message to report-generation-queue
    """
    response = sqs.send_message(
        QueueUrl=REPORT_QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )
    return response


def receive_message_from_report_queue():
    """
    Pull one message from queue (long polling)
    """
    response = sqs.receive_message(
        QueueUrl=REPORT_QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    return messages[0] if messages else None


def delete_message_from_queue(receipt_handle):
    """
    Delete a message after successful processing
    """
    sqs.delete_message(
        QueueUrl=REPORT_QUEUE_URL,
        ReceiptHandle=receipt_handle
    )
