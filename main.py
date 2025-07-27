from data.loader import bot, db
import handlers


if __name__ == '__main__':
    db.create_table_users()
    db.create_table_travels()
    db.creta_table_images()
    bot.infinity_polling()