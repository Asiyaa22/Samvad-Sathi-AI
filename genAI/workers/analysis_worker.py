# workers/analysis_worker.py

import time
import json
from core.sqs import receive_message_from_analysis_queue, delete_message_from_queue
from core.llm import transcribe_audio, analyse_answer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from interviews.models import QuestionAttempt
from database import DATABASE_URL  # Your SQLAlchemy DB URL

# 🎯 Step 1: Setup database connection using SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def process_message(message_body):
    """
    🎯 Step 2: Handle a single SQS message.
    - Transcribe audio
    - Analyze the answer
    - Update database with results
    """
    data = json.loads(message_body)

    # Extract required fields
    question_attempt_id = data.get("question_attempt_id")
    audio_url = data.get("audio_url")

    if not question_attempt_id or not audio_url:
        print("❌ Invalid message format, skipping")
        return

    db = SessionLocal()

    try:
        # 🔊 Step 2.1: Transcribe the audio file using LLM
        transcription = transcribe_audio(audio_url)

        # 🧠 Step 2.2: Analyze the transcribed answer using LLM
        analysis = analyse_answer(transcription)

        # 📝 Step 2.3: Update the database with transcription and analysis
        attempt = db.query(QuestionAttempt).filter_by(id=question_attempt_id).first()
        if attempt:
            attempt.transcription = transcription
            attempt.analysis = analysis
            attempt.is_transcribed = True
            attempt.is_analysed = True
            db.commit()
            print(f"✅ Successfully processed QuestionAttempt ID {question_attempt_id}")
        else:
            print(f"❌ QuestionAttempt ID {question_attempt_id} not found in DB")

    except Exception as e:
        # 🚨 Handle any error gracefully
        db.rollback()
        print(f"❌ Error processing message: {str(e)}")
    finally:
        db.close()

def run_worker():
    """
    🌀 Step 3: Worker loop
    - Continuously poll the SQS queue for new messages
    - Process each message
    - Delete the message after processing
    """
    print("🟡 Analysis Worker started... polling for messages")

    while True:
        messages = receive_message_from_analysis_queue()

        # 💤 If no messages, wait and retry
        if not messages:
            time.sleep(3)
            continue

        for msg in messages:
            receipt_handle = msg['ReceiptHandle']
            body = msg['Body']

            # ⚙️ Process message (transcribe + analyze + update DB)
            process_message(body)

            # 🧹 Delete message from queue to avoid reprocessing
            delete_message_from_queue(receipt_handle)

# 🏁 Entry point
if __name__ == "__main__":
    run_worker()
