import time
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.sqs import receive_message_from_report_queue, delete_message_from_queue
from app.database import SQLALCHEMY_DATABASE_URL  # Your DB connection
from app.reports.services import generate_and_save_report

# Setup DB session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def process_message(message_body: dict):
    """
    Core logic to handle each incoming SQS message.
    """
    db = SessionLocal()
    try:
        interview_attempt_id = message_body["interview_attempt_id"]

        # Generate and store report
        report = generate_and_save_report(db, interview_attempt_id=interview_attempt_id)

        print(f"✅ Report generated: {report.report_id}")

    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")

    finally:
        db.close()


def start_report_worker():
    """
    Continuously poll the SQS queue for new report generation tasks.
    """
    print("📡 Report worker started. Waiting for messages...")

    while True:
        message = receive_message_from_report_queue()

        if message:
            receipt_handle = message['ReceiptHandle']
            body = json.loads(message['Body'])

            print(f"📥 Received message: {body}")

            process_message(body)

            # Delete from queue after successful processing
            delete_message_from_queue(receipt_handle)

        else:
            # No message? wait for a short interval
            time.sleep(5)
