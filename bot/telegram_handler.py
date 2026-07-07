import os
import logging
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from llm.normalizer import MedicamentoNormalizer

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

normalizer = MedicamentoNormalizer()

# Mensaje de instrucciones (reutilizable)
INSTRUCCIONES = (
    "🤖 *Instrucciones de uso:*\n\n"
    "1️⃣ */medicamento <nombre>*: Busca información sobre un medicamento en México.\n"
    "   _Ejemplo: `/medicamento Paracetamol`_\n\n"
    "2️⃣ *Cualquier otro mensaje*: Repetiré el texto que me envíes (función de eco).\n\n"
    "Usa /start para reiniciar o /ayuda para ver este mensaje de nuevo."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot asistente.\n\n" + INSTRUCCIONES,
        parse_mode="Markdown"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(INSTRUCCIONES, parse_mode="Markdown")

async def buscar_medicamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Por favor, dime qué medicamento buscar.\n"
            "Ejemplo: `/medicamento Paracetamol`",
            parse_mode="Markdown"
        )
        return

    nombre = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)

    resultado = normalizer.normalizar(nombre)

    if "error" in resultado:
        await update.message.reply_text(f"❌ Error: {resultado['error']}")
        return

    respuesta = (
        f"*📋 Ficha de {resultado.get('nombre_ingresado', nombre)}*\n\n"
        f"*Nombre genérico:* {resultado.get('nombre_generico', 'N/D')}\n"
        f"*Uso principal:* {resultado.get('uso_principal', 'N/D')}\n"
        f"*¿Requiere receta?* {'Sí' if resultado.get('requiere_receta') else 'No'}"
    )
    await update.message.reply_text(respuesta, parse_mode="Markdown")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Eco: {update.message.text}")

def run_telegram_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN no configurado")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("medicamento", buscar_medicamento))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.info("Bot de Telegram iniciado (polling)")
    app.run_polling()