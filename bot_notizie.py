import os
import requests
from bs4 import BeautifulSoup
import telegram
import time

# Ottieni variabili di ambiente
TOKEN = '7876152396:AAFwB1511A5o59QShrs7N-6CrRlLqo0uISA'
CHAT_ID = '119121853'

bot = telegram.Bot(token=TOKEN)
url = "https://www.miur.gov.it/web/miur-usr-campania/notizie"

def get_latest_news():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='contentTitle')
    news_list = []
    
    for article in articles:
        title = article.text.strip()
        link = article.find('a')['href']
        full_link = f"https://www.miur.gov.it{link}"
        news_list.append((title, full_link))
    
    return news_list

def send_telegram_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

latest_news = set()

while True:
    try:
        news = get_latest_news()
        
        for title, link in news:
            if title not in latest_news:
                send_telegram_message(f"Nuova notizia: {title}\nLink: {link}")
                latest_news.add(title)
        
        time.sleep(3600)
    except Exception as e:
        print(f"Errore: {e}")
        time.sleep(3600)
