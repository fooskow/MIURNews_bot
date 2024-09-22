import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

# Funzione per inviare notifiche
def invia_notifica(context: CallbackContext) -> None:
    url = "https://www.miur.gov.it/web/miur-usr-campania/notizie"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Qui puoi aggiungere la logica per estrarre le notizie
        # Ad esempio, puoi usare BeautifulSoup per fare scraping della pagina
        notizie = "Notizie aggiornate: " + url  # Modifica secondo le tue necessità
        
        # Invia il messaggio al CHAT_ID specificato
        chat_id = os.getenv('CHAT_ID')
        context.bot.send_message(chat_id=chat_id, text=notizie)
    else:
        chat_id = os.getenv('CHAT_ID')
        context.bot.send_message(chat_id=chat_id, text="Errore nel recupero delle notizie.")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Ciao! Sono un bot! Usa /notifica per ricevere le ultime notizie.')

def main():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Puoi programmare invii automatici qui, se necessario
    # Esempio: invia_notifica ogni ora
    # context.job_queue.run_repeating(invia_notifica, interval=3600, first=0)

    # Avvio del polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
