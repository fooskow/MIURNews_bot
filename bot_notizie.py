import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Funzione per inviare notifiche
async def invia_notifica(context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://www.miur.gov.it/web/miur-usr-campania/notizie"
    response = requests.get(url)
    
    if response.status_code == 200:
        notizie = "Notizie aggiornate: " + url  # Modifica secondo le tue necessità
        chat_id = os.getenv('CHAT_ID')
        await context.bot.send_message(chat_id=chat_id, text=notizie)
    else:
        chat_id = os.getenv('CHAT_ID')
        await context.bot.send_message(chat_id=chat_id, text="Errore nel recupero delle notizie.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Ciao! Sono un bot! Usa /notifica per ricevere le ultime notizie.')

def main():
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    # Esempio di invio di notifiche, se necessario
    # application.job_queue.run_repeating(invia_notifica, interval=3600, first=0)

    # Avvio del polling
    application.run_polling()

if __name__ == '__main__':
    main()
