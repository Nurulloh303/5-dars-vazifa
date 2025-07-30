from telebot.types import Message, ReplyKeyboardRemove
from keyboards.default import make_buttons
from data.loader import bot, db
from config import ADMINS

admin_buttons_names = [
    "➕ Sayohatlarni qoshish",
    "➕ Mashhur joylarni qoshish",
    "➕ Ekskursiya jadvalini qoshish",
    "➕ Narxlarni qoshish"
]

TRAVEL = {}

@bot.message_handler(func=lambda message: message.text == "Admin buyruqlari")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Admin buyruqlari", reply_markup=make_buttons(admin_buttons_names, back=True))


@bot.message_handler(func=lambda message: message.text == "➕ Mashhur joylarni qoshish")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Mashhur joy nomini o'zbek tilida kiriting: ", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_uz_travel)

def get_name_uz_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id] = {
        "name_uz": message.text
    }



    msg = bot.send_message(chat_id, "Mashhur joy nomini rus tilida kiriting: ")
    bot.register_next_step_handler(msg, get_name_ru_travel)


def get_name_ru_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["name_ru"] = message.text
    msg = bot.send_message(chat_id, "Mashhur joy nomini ingliz tilida kiriting: ")
    bot.register_next_step_handler(msg, get_name_en_travel)

def get_name_en_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["name_en"] = message.text
    msg = bot.send_message(chat_id, "Mashhur joyga borish narxini kiriting: ")
    bot.register_next_step_handler(msg, get_name_price)


def get_name_price(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["price"] = message.text
    msg = bot.send_message(chat_id, "Sayohat davomiyligini kiriting: ")
    bot.register_next_step_handler(msg, get_name_days)

def get_name_days(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["days"] = message.text
    msg = bot.send_message(chat_id, "Soyohat rasmi linkini yuboring: ")
    bot.register_next_step_handler(msg, get_image_travel)

def get_image_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not TRAVEL[from_user_id].get("images"):
        TRAVEL[from_user_id]["images"] = [message.text]
    else:
        TRAVEL[from_user_id]["images"].append(message.text)
    msg = bot.send_message(chat_id, "Yana rasm qoshasizmi: ",
                     reply_markup=make_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_travel)

def save_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text == "No":

        name_uz = TRAVEL[from_user_id]["name_uz"]
        name_ru = TRAVEL[from_user_id]["name_ru"]
        name_en = TRAVEL[from_user_id]["name_en"]
        price = int(TRAVEL[from_user_id]["price"])
        days = int(TRAVEL[from_user_id]["days"])
        images = TRAVEL[from_user_id]["images"]
        travel_id = db.insert_travel(name_uz, name_en, name_ru, price, days)
        print(travel_id)
        for image in images:
            db.insert_image(image, travel_id)
        bot.send_message(chat_id, "Sayohat saqlandi!",
                         reply_markup=make_buttons(admin_buttons_names, back=True))
    else:
        msg = bot.send_message(chat_id, "Soyohat rasmi linkini yuboring: ", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_image_travel)

# ekskursiya------------------------------

@bot.message_handler(func=lambda message: message.text == "➕ Ekskursiya jadvalini qoshish")
def start_add_excursion(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Sayohat ID raqamini kiriting:")  # mavjud travel_id ni
        bot.register_next_step_handler(msg, get_excursion_travel_id)

def get_excursion_travel_id(message: Message):
    from_user_id = message.from_user.id
    TRAVEL[from_user_id] = {
        "travel_id": int(message.text)
    }
    msg = bot.send_message(message.chat.id, "Ekskursiya sanasini kiriting (YYYY-MM-DD):")
    bot.register_next_step_handler(msg, get_excursion_date)

def get_excursion_date(message: Message):
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["date"] = message.text
    msg = bot.send_message(message.chat.id, "Izoh (ixtiyoriy):")
    bot.register_next_step_handler(msg, save_excursion_schedule)

def save_excursion_schedule(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    comment = message.text

    travel_id = TRAVEL[from_user_id]["travel_id"]
    date = TRAVEL[from_user_id]["date"]

    db.insert_excursion(travel_id, date, comment)
    bot.send_message(chat_id, "✅ Ekskursiya jadvali saqlandi!", reply_markup=make_buttons(admin_buttons_names, back=True))
