from data.loader import bot, db
import handlers


if __name__ == '__main__':
    db.create_table_users()
    # db.drop_table_travels()
    # db.drop_table_excursion_schedule()
    db.create_table_travels()
    db.create_table_excursion_schedule()
    db.creta_table_images()
    bot.infinity_polling()