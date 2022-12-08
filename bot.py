import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters
import parse

SELECT_TEST = 1
QUERY_QUESTION = 2
CHECK_ANS = 3


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет {update.effective_user.first_name}. Скорее начинай решать задачки!')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tests = parse.get_tests()
    test_names = []
    for test in tests:
        test_names.append([test['title']])

    await update.message.reply_text('Привет! Я бот, который будет давать тебе задачки. Меня сделали как тестовый '
                                    'проект от "Время 31-х"\n\nВыбери на клавиатуре тест, котороый ты хочешь пройти.',
                                    reply_markup=telegram.ReplyKeyboardMarkup(keyboard=test_names))
    return SELECT_TEST


async def select_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    test_title = update.message.text

    test = {}
    for t in parse.get_tests():
        if t['title'] == test_title:
            test = t
            break

    context.user_data['questions'] = test['questions']
    context.user_data['q_index'] = 0
    await update.message.reply_text(f'Тест {test_title} выбран. Сейчас я начну задавать вам вопросы.',
                                    reply_markup=telegram.ReplyKeyboardMarkup(keyboard=[['Поехали!']]))
    return QUERY_QUESTION


async def query_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    questions = context.user_data['questions']
    q_index = context.user_data['q_index']

    if q_index >= len(questions):
        await update.message.reply_text('Вопросов больше нет.')
        return telegram.ext.ConversationHandler.END

    question = questions[q_index]

    context.user_data['variants'] = question['variants']
    context.user_data['ans'] = question['ans']

    variants = [[t] for t in question['variants']]

    await update.message.reply_text(question['text'], reply_markup=telegram.ReplyKeyboardMarkup(keyboard=variants))
    return CHECK_ANS


async def check_ans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_variant = update.message.text
    right_variant = context.user_data['variants'][context.user_data['ans']]

    if user_variant == right_variant:
        await update.message.reply_text('У-р-р-ра, ты молодец!) Следующий вопрос...',
                                        reply_markup=
                                        telegram.ReplyKeyboardMarkup(keyboard=[['Ура! Скорее ещё вопросов!']])
                                        )
    else:
        await update.message.reply_text('Извини, но твой ответ не верный.',
                                        reply_markup=
                                        telegram.ReplyKeyboardMarkup(keyboard=[['Жаль( Давай следующий вопрос...']]))

    context.user_data['q_index'] += 1
    return QUERY_QUESTION


app = ApplicationBuilder().token("5812448710:AAEa6lV4pvXBesAqfBhHRfQU0kNwnlZnErc").build()

conv_handler = telegram.ext.ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECT_TEST: [telegram.ext.MessageHandler(filters.TEXT & ~filters.COMMAND, select_test)],
        QUERY_QUESTION: [telegram.ext.MessageHandler(filters.TEXT & ~filters.COMMAND, query_question)],
        CHECK_ANS: [telegram.ext.MessageHandler(filters.TEXT & ~filters.COMMAND, check_ans)]
    },
    fallbacks=[]
)

app.add_handler(CommandHandler("hello", hello))
app.add_handler(conv_handler)

app.run_polling()
