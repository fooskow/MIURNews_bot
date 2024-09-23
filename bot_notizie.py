import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Inizializza il logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

# Variabili di ambiente
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')  # Assicurati di impostare il CHAT_ID come variabile di ambiente
PORT = int(os.environ.get('PORT', 5000))

# Costruisci l'applicazione Telegram
application = ApplicationBuilder().token(TOKEN).build()

# Funzione di start che risponde con il CHAT_ID dell'utente
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    CHAT_ID = update.message.CHAT_ID
    await update.message.reply_text(f'Il tuo CHAT_ID è: {CHAT_ID}')

# Funzione per inviare una notifica manuale
@app.route('/send_notification', methods=['POST'])
def send_notification():
    message = request.form.get('message', 'Notifica di default')
    if CHAT_ID:
        async def send_message():
            await application.bot.send_message(CHAT_ID=CHAT_ID, text=message)
        application.create_task(send_message())
        return "Messaggio inviato!"
    return "Errore: CHAT_ID non impostato"

# Funzione per gestire il webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    async def process_update():
        await application.process_update(update)
    application.create_task(process_update())
    return "OK", 200

# Imposta il webhook all'avvio dell'applicazione
async def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
    await application.bot.set_webhook(url=webhook_url)

# Aggiungi il comando /start
application.add_handler(CommandHandler("start", start))

# Avvia Flask
if __name__ == '__main__':
    import asyncio
    # Imposta il webhook all'avvio dell'app
    asyncio.run(set_webhook())
    # Avvia l'app Flask
    app.run(host="0.0.0.0", port=PORT)
