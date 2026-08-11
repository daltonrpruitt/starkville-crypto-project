"""
Send an SMS to a newline-separated list of phone numbers using Twilio.

Setup:
    pip install twilio python-dotenv

.env file (same directory) should contain:
    TWILIO_ACCOUNT_SID=your_account_sid
    TWILIO_AUTH_TOKEN=your_auth_token
    TWILIO_FROM_NUMBER=+1XXXXXXXXXX

Usage:
    python send_sms.py numbers.txt "Your message here"

numbers.txt should contain one phone number per line, e.g.:
    +15551234567
    +15559876543
"""

import os
import sys
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")


def load_numbers(path):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def send_messages(numbers, body):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for number in numbers:
        try:
            message = client.messages.create(
                body=body,
                from_=FROM_NUMBER,
                to=number,
            )
            print(f"Sent to {number}: SID {message.sid}")
        except TwilioRestException as e:
            print(f"Failed to send to {number}: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python send_sms.py <numbers_file> <message>")
        sys.exit(1)

    if not (ACCOUNT_SID and AUTH_TOKEN and FROM_NUMBER):
        print("Missing Twilio credentials. Check your .env file.")
        sys.exit(1)

    numbers_file, message_body = sys.argv[1], sys.argv[2]
    numbers = load_numbers(numbers_file)

    if not numbers:
        print("No phone numbers found in file.")
        sys.exit(1)

    send_messages(numbers, message_body)


if __name__ == "__main__":
    main()