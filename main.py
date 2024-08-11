import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from messages import start_message, selection_message
from google_api import search_coordinates, search_nearby_restaurants, gmaps, min_review, min_rating, radius, search_photogenic_spots
from unsplash_api import location_photos, unsplash
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ASK_SELECTION, ASK_LOCATION, ASK_FOOD, ASK_PHOTO, ASK_RESTART = range(5)

keyboard = [
    ['FOOD'],
    ['PHOTOS']
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


# call back function that initiates options for food or photos when /start is pressed
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_message, reply_markup=reply_markup)
    return ASK_SELECTION


# handles anything typed that is not /start or any other commands or valid responses
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Invalid input. Please type /start to restart the conversation.')
    return ConversationHandler.END


# handles the selection of custom keyboard choices by prompting user to enter desired location to search
async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_selection = update.message.text

    if user_selection == 'FOOD':
        await update.message.reply_text('Please enter your location (city, neighbourhood, country, etc.)')
        return ASK_FOOD

    elif user_selection == 'PHOTOS':
        await update.message.reply_text('Please enter your location (city, neighbourhood, country, etc.)')
        return ASK_PHOTO


# handles the location response for restaurants nearby
async def handle_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text
    try:
        latitude, longitude = search_coordinates(gmaps, location)

    except TypeError:
        await update.message.reply_text('Your location was not recognized. Please try again.')
        return ASK_FOOD

    if latitude and longitude:
        restaurants = search_nearby_restaurants(gmaps, min_rating, min_review, latitude, longitude, radius)
        response = ''
        for restaurant in restaurants:
            name = restaurant.get('name')
            rating = restaurant.get('rating')
            user_ratings_total = restaurant.get('user_ratings_total')
            response += f"Name: {name}\nRating: {rating}\nReviews: {user_ratings_total}\n\n"

        await update.message.reply_text(response)
        await update.message.reply_text('Do you want to restart? (yes/no)')
        return ASK_RESTART


# handles messages to send photos and the names of those places
async def handle_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text

    try:
        latitude, longitude = search_coordinates(gmaps, location)

    except TypeError:
        await update.message.reply_text('Your location was no recognized. Please try again.')
        return ASK_PHOTO

    if latitude and longitude:
        photo_spots = search_photogenic_spots(gmaps, latitude, longitude)
        for location in photo_spots:
            photo = location_photos(location, unsplash)
            await update.message.reply_photo(photo)
            await update.message.reply_text(location)

        await update.message.reply_text('Do you want to restart? (yes/no)')
        return ASK_RESTART


# handles restarts of conversations
async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text

    if answer == 'yes':
        await update.message.reply_text(selection_message, reply_markup=reply_markup)
        return ASK_SELECTION
    elif answer == 'no':
        await update.message.reply_text('Thank you for using our service. Have a nice day.')
        return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()

    # Handlers
    global_fallback_handler = MessageHandler(~filters.Regex('/start'), cancel)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_SELECTION: [MessageHandler(filters.Regex('^(FOOD|PHOTOS)$'), handle_selection)],
            ASK_FOOD: [MessageHandler(filters.TEXT, handle_restaurant)],
            ASK_RESTART: [MessageHandler(filters.Regex('^(yes|no)$'), handle_restart)],
            ASK_PHOTO: [MessageHandler(filters.TEXT, handle_photos)]
        },
        fallbacks=[MessageHandler(filters.TEXT, cancel)]
    )

    # Add Handlers
    application.add_handler(conv_handler)
    application.add_handler(global_fallback_handler)

    # run until stop
    application.run_polling()
