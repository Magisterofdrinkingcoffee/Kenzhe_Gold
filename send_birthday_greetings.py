import os
import django
import datetime
import requests


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewellery_site.settings')
django.setup()

from store.models import BirthdayClient


ULTRAMSG_INSTANCE_ID = 'instance125773'
ULTRAMSG_TOKEN = 'iikr53bc9sfebgdq'
ADMIN_PHONE = '+77017707593'  

def send_birthday_messages():
    today = datetime.date.today()
    clients = BirthdayClient.objects.filter(
        birthday__month=today.month,
        birthday__day=today.day
    )
    print("Скрипт запущен")
    print(f"Сегодня: {today}")
    print(f"Найдено клиентов: {clients.count()}")

    for client in clients:
        if client.phone_number:
            send_whatsapp(client.phone_number, f"С днём рождения, {client.full_name}! 🎉")
        if client.instagram_username:
            notify_admin(f"Сегодня у @{client.instagram_username} день рождения!")

def send_whatsapp(phone, message):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": phone,
        "body": message
    }

    try:
        response = requests.post(url, data=payload)
        print(f"[WhatsApp] -> {phone}: {message}")
        print(f"[UltraMsg Response] {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"[Ошибка отправки WhatsApp]: {e}")

def notify_admin(message):
    send_whatsapp(ADMIN_PHONE, message)

if __name__ == "__main__":
    send_birthday_messages()
