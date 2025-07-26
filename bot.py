from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from handlers import (
    start, 
    vote_callback, 
    handle_other, 
    results, 
    set_lang, 
    ASK_OTHER
)    
import os

TOKEN = ""

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(vote_callback)],
        states={ASK_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other)]},
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("results", results))
    app.add_handler(CommandHandler("lang", set_lang))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()