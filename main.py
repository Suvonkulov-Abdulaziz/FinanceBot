from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from supabase import create_client, Client
import os

# Supabase connection
SUPABASE_URL = ""
SUPABASE_KEY = ""
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Telegram bot token
TELEGRAM_TOKEN = ''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /income or /expense to log your finances.')

async def log_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE, transaction_type: str) -> None:
    try:
        amount = float(context.args[0])
        comment = ' '.join(context.args[1:]) if len(context.args) > 1 else None
        data = {
            'type': transaction_type,
            'amount': amount,
            'comment': comment,
        }
        response = supabase.table('transactions').insert(data).execute()
        await update.message.reply_text(f'{transaction_type.capitalize()} logged successfully!')
    except Exception as e:
        await update.message.reply_text(f'Error logging {transaction_type}: {e}')

async def log_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await log_transaction(update, context, 'income')

async def log_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await log_transaction(update, context, 'expense')

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers for the commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("income", log_income))
    application.add_handler(CommandHandler("expense", log_expense))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
