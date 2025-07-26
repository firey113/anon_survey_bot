from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from storage import *
from config import *

ASK_OTHER = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_data()
    lang = get_language(data, user_id)
    keyboard = [
        [InlineKeyboardButton(p, callback_data=p)] for p in PARTIES[lang]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(MESSAGES["start"][lang], reply_markup=markup)

async def vote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    user_id = query.from_user.id
    user_hash = get_user_hash(user_id)

    data = load_data()
    lang = get_language(data, user_id)

    if user_hash in data["hashes"]:
        await query.edit_message_text(MESSAGES["already_voted"][lang])
        return

    if choice == "Другая" or choice == "Other":
        context.user_data["hash"] = user_hash
        await query.edit_message_text(MESSAGES["send_other"][lang])
        return ASK_OTHER

    record_vote(data, user_hash, choice)
    save_data(data)

    await query.edit_message_text(MESSAGES["thank_you"][lang].format(choice=choice))

async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_hash = context.user_data.get("hash")
    data = load_data()
    lang = get_language(data, update.effective_user.id)

    if user_hash in data["hashes"]:
        await update.message.reply_text(MESSAGES["already_voted"][lang])
        return ConversationHandler.END

    record_other(data, user_hash, text)
    save_data(data)
    await update.message.reply_text(MESSAGES["thank_you"][lang].format(choice=text))
    return ConversationHandler.END

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id = update.effective_user.id
    lang = get_language(data, user_id)

    if not data["counts"]:
        await update.message.reply_text(MESSAGES["no_votes"][lang])
        return

    total = sum(data["counts"].values())
    msg = MESSAGES["results_title"][lang] + "\n\n"
    for party, count in sorted(data["counts"].items(), key=lambda x: -x[1]):
        bar = "▓" * int((count / total) * 10)
        percent = (count / total) * 100
        msg += f"{party}: {bar} {percent:.1f}% ({count})\n"

    if data["other"]:
        msg += f"\nДругие варианты / Other: {len(data['other'])} submitted"

    await update.message.reply_text(msg)

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_data()
    new_lang = toggle_language(data, user_id)
    save_data(data)
    await update.message.reply_text(MESSAGES["set_lang"][new_lang])