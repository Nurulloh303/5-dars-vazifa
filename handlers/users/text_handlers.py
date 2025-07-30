from telebot.types import Message
from data.loader import bot, db
from config import TEXTS
from keyboards.default import make_buttons
from keyboards.inline import lang_buttons, travels_buttons
from .callbacks import get_name


# ekskursiya----------------------


@bot.message_handler(func=lambda message: message.text in TEXTS[db.get_lang(message.from_user.id)][101])
def reaction_to_packages(message: Message):
    chat_id = message.chat.id
    lang = db.get_lang(message.from_user.id)
    if message.text in ["⚙️Settings", "⚙️Настройки", "⚙️Sozlamalar"]:
        btn_texts = TEXTS[lang][102]
        text = TEXTS[lang][6]
        msg = bot.send_message(chat_id, text,
                                  reply_markup=make_buttons(btn_texts, lang=lang, back=True))
        bot.register_next_step_handler(msg, get_settings)
    elif message.text in TEXTS[lang][101][1]:
        travels_list = db.select_travels(lang)
        bot.send_message(chat_id, "Mashxur joylar ro'yhati",
                         reply_markup=travels_buttons(travels_list))

    elif message.text in ["📅 Ekskursiya jadvali", "📅 Расписание туров", "📅 Tour Schedule"]:
        chat_id = message.chat.id
        lang = db.get_lang(message.from_user.id)

        excursions = db.select_all_excursions()

        if not excursions:
            bot.send_message(chat_id, TEXTS[lang].get(103, "Hozircha hech qanday ekskursiya mavjud emas."))
            return

        text = "📅 Ekskursiya jadvali:\n\n"
        for ex in excursions:
            travel_id = ex[1]
            date = ex[2]
            comment = ex[3] if ex[3] else "—"

            travel_name = db.select_travel_name_by_id(travel_id, lang)
            text += f"🏞 {travel_name}\n📆 Sana: {date}\n📝 Izoh: {comment}\n\n"

        bot.send_message(chat_id, text)


# ekskursiya----------------------


def get_settings(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(message.from_user.id)
    if message.text in ["⬅️ortga", "⬅️back", "⬅️назад", "/start"]:
        btn_names = TEXTS[lang][101]
        text = TEXTS[lang][4]
        bot.send_message(chat_id, text,
                         reply_markup=make_buttons(btn_names))
    else:
        if message.text == TEXTS[lang][102][0]:
            text = TEXTS[lang][7]
            bot.send_message(chat_id, TEXTS[lang][7], reply_markup=lang_buttons())

@bot.message_handler(func=lambda message: message.text == TEXTS[db.get_lang(message.from_user.id)][102][1])
def reaction_to_re_register(message: Message):
    chat_id = message.chat.id
    lang = db.get_lang(message.from_user.id)
    text = TEXTS[lang][1]
    msg = bot.send_message(chat_id, text)
    bot.register_next_step_handler(msg, get_name)


