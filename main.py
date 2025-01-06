from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7599521676:AAGAkoJJ4YOaYvlhH9OnwP1Zrp9GpWuZxoI'
BOT_USERNAME: Final = '@Test_andalus_bot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am Sheref From Sheref media')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Sheref! Please type some thing so I can respond')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')


# Handle responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there!'

    if 'How are you!' in processed:
        return 'I am good!'

    if 'I love python' in processed:
        return 'Remember to subscribe'

    return 'I do not understand what you wrote'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        rsponse: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

    if __name__ == '__main__':
        print('Starting bot...')
        app = Application.builder().token(TOKEN).build()

        #Commands
        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(CommandHandler('help', start_command))
        app.add_handler(CommandHandler('start', start_command))

        #Messages
        app.add_handler(MessageHandler(filters.TEXT, handle_message))

        #Errors
        app.add_error_handler(error)

        #polls the bot
        print('Polling...')
        app.run_polling(poll_interval=3)