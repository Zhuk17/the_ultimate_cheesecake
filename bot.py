from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import gspread
import openai

# Настройка API
openai.api_key = 'your-openai-api-key'
gc = gspread.service_account(filename="credentials.json")
sheet = gc.open("FAQ Database").sheet1  # Название таблицы

# Извлечение текста из документа Google Docs
def get_document_text(document_id):
    document = service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')
    
    text = ''
    for element in content:
        if 'paragraph' in element:
            for text_run in element['paragraph']['elements']:
                if 'textRun' in text_run:
                    text += text_run['textRun']['content']
    return text

# Обработка вопроса с OpenAI
def get_answer_from_openai(document_text, question):
    prompt = f"Текст документа: {document_text}\n\nВопрос: {question}\nОтвет:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

# Функция для обработки текста и вопроса
async def handle_message(update: Update, context):
    user_message = update.message.text  # Получаем текст от пользователя
    document_text = get_document_text('your-google-doc-id')  # Извлекаем текст документа
    answer = get_answer_from_openai(document_text, user_message)  # Получаем ответ
    await update.message.reply_text(answer)  # Отправляем ответ пользователю

# Главная функция
if __name__ == "__main__":
    app = ApplicationBuilder().token("7457717168:AAHXHsJwMCfUOUzB9QrcofrmMvo8fMYvZM4").build()
    
    # Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен!")
    app.run_polling()
