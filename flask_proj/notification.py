from dotenv import load_dotenv
import os 


def send_notification(url):  
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendmessage?chat_id={CHAT_ID}&text={url}')  