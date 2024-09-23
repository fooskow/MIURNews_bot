import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import asyncio

app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

logging.basicConfig(level=logging.INFO)

async def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
    logging.info(f"Setting webhook to: {webhook_url}")  # Stampa l'URL del webhook
    await application.bot.delete_webhook()  # Rimuovi il webhook esistente
    await application.bot.set_webhook(url=webhook_url)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    logging.info(f"Received update: {update}")  # Log dell'aggiornamento ricevuto
    # Gestisci l'aggiornamento qui (ad esempio, invia notifiche)
    return 'ok'

async def main():
    global application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Imposta i gestori di comandi se necessario
    # application.add_handler(CommandHandler("start", start))
    
    await set_webhook()

if __name__ == '__main__':
    asyncio.run(main())
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
