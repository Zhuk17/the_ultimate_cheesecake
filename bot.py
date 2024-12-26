from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text  # Получаем текст от пользователя
    response = f"Вы сказали: {user_message}"  # Формируем ответ
    await update.message.reply_text(response)  # Отправляем ответ пользователю

# Главная функция
if __name__ == "__main__":
    app = ApplicationBuilder().token("7457717168:AAHXHsJwMCfUOUzB9QrcofrmMvo8fMYvZM4").build()
    
    # Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен!")
    app.run_polling()
