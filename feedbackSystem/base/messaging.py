import os

from twilio.rest import Client
from dotenv import load_dotenv

from feedbackSystem.settings import COUNTRY_E146_CODE

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

class MessageHandler:
    phoneNumber = ""
    otp = ""

    def __init__(self, phoneNumber: str, otp="0000"):
        self.phoneNumber = phoneNumber
        self.otp = otp

    def __otpTranslate__(self, language='en'):
        msgOTP = {
            'en': f"Your OTP for the Police Feedback System is {self.otp}.",
            'hi': f"पुलिस प्रतिक्रिया प्रणाली के लिए आपका ओटीपी {self.otp} है।"
        }
        return msgOTP.get(language, msgOTP['en'])

    def sendOTP(self, language='en'):
        if self.otp == "0000": raise ValueError("OTP not Provided")
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=self.__otpTranslate__(language),
            from_=f'{TWILIO_PHONE_NUMBER}',
            to=f'{COUNTRY_E146_CODE}{self.phoneNumber}'
        )

    def sendMessage(self, message: str):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=f'{TWILIO_PHONE_NUMBER}',
            to=f'{COUNTRY_E146_CODE}{self.phoneNumber}'
        )