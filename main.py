import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,CallbackQueryHandler,MessageHandler, filters
TOKEN="5718005754:AAHmmSzqntFF0yn7hNSDT-8kg49xx_dmqPA"
bot=telegram.Bot(token=TOKEN)
updater=Updater(bot=bot, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start',start))
dispatcher = updater.dispatcher
bot = updater.bot

schedule_images_dir = "schedule_images"

days_of_week = {
    "понедельник": 1,
    "вторник": 2,
    "среда": 3,
    "четверг": 4,
    "пятница": 5,
    "суббота": 6,
    "воскресенье": 7,
}

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Расписание на сегодня", callback_data="today")],
        [InlineKeyboardButton("Расписание на завтра", callback_data="tomorrow")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

def show_schedule(update, context):
    query = update.callback_query
    query.answer()

    current_day = days_of_week.get(query.data)
    if current_day is None:
        query.message.reply_text("Ошибка при определении дня.")
        return
    is_odd_week = True

    next_day = (current_day % 7) + 1 if current_day != 7 else 1

    schedule_image_filename_today = f"{list(days_of_week.keys())[current_day - 1]}_{'odd' if is_odd_week else 'even'}.png"
    schedule_image_filename_tomorrow = f"{list(days_of_week.keys())[next_day - 1]}_{'odd' if is_odd_week else 'even'}.png"

    schedule_image_path_today = os.path.join(
        schedule_images_dir, schedule_image_filename_today
    )
    schedule_image_path_tomorrow = os.path.join(
        schedule_images_dir, schedule_image_filename_tomorrow
    )

    if os.path.exists(schedule_image_path_today):
        with open(schedule_image_path_today, "rb") as image_file:
            query.message.reply_photo(photo=image_file)
    else:
        query.message.reply_text("Изображение расписания на сегодня не найдено.")

    if os.path.exists(schedule_image_path_tomorrow):
        with open(schedule_image_path_tomorrow, "rb") as image_file:
            query.message.reply_photo(photo=image_file)
    else:
        query.message.reply_text("Изображение расписания на завтра не найдено.")


def unknown(update, context):
    update.message.reply_text("Извините, я не понимаю эту команду.")


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(
    CallbackQueryHandler(
        show_schedule,
        pattern="^(понедельник|вторник|среда|четверг|пятница|суббота|воскресенье)$",
    )
)
dispatcher.add_handler(MessageHandler(filters.command, unknown))

updater.start_polling()
updater.idle()