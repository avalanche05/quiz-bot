from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет {update.effective_user.first_name}. Скорее начинай решать задачки!')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот, который будет давать тебе задачки. Меня сделали как тестовый '
                                    'проект от "Время 31-х"\n\nВыбери на клавиатуре тест, котороый ты хочешь пройти.')


app = ApplicationBuilder().token("5812448710:AAEa6lV4pvXBesAqfBhHRfQU0kNwnlZnErc").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))

app.run_polling()
