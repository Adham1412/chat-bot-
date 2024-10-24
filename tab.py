import telebot
from textblob import TextBlob
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from datetime import datetime, timedelta

# Telegram Bot tokenini kiriting
API_TOKEN = '7663219810:AAEBvMay_uJ4XHMzCCjC2GTTL2xlPJKfAdI'

bot = telebot.TeleBot(API_TOKEN)

# Malumotlar bazasini ulaymiz
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Foydalanuvchilar jadvalini yaratamiz
cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (user_id INTEGER PRIMARY KEY, last_activity TEXT)''')

conn.commit()

# Xabarlar tarixini saqlash uchun ro'yxat
message_history = []

# Foydalanuvchini yangilash yoki yangi foydalanuvchi qo'shish
def update_user_activity(user_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT OR REPLACE INTO users (user_id, last_activity) 
                      VALUES (?, ?)''', (user_id, now))
    conn.commit()

# Oylik faol foydalanuvchilar sonini hisoblash
def get_monthly_active_users():
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''SELECT COUNT(DISTINCT user_id) FROM users WHERE last_activity >= ?''', (thirty_days_ago,))
    return cursor.fetchone()[0]

# O‘zbek tilini tahlil qilish uchun TextBlob'dan foydalanamiz
def uzbek_text_analysis(text):
    blob = TextBlob(text)
    return blob.correct()  # Xato so‘zlarni to‘g‘rilaydi

# Murakkab javoblar tuzish uchun
def get_response(message):
    message_text = message.text.lower()
    
    if "assalomu alaykum" in message_text or "salom" in message_text:
        return "Assalomu alaykum! Yordam bera olamanmi?"
    
    elif "ha" in message_text or "ha mayli" in message_text or "ok" in message_text:
        return "Men sizga qanday yordam bera olaman😊?"

    elif "ismingiz kim" in message_text or "Isming nima" in message_text:
        return "Mening ismim ChatBot🤖 O‘zbek tilida suhbatlashaman."

    elif "qalay" in message_text or "qanday" in message_text or "qandaysiz" in message_text:
        return "Rahmat, yaxshi! Sizda qanday yangiliklar?"

    elif "ob-havo" in message_text:
        return "Afsuski, men hozir ob-havo ma'lumotlarini yetkazib bera olmayman, lekin ob-havo ilovasidan foydalanishingiz mumkin."

    elif "xayr" in message_text:
        return "Siz bilan suhbatlashganimdan mamnunman."

    elif "xotin kerak" in message_text:
        return "men ChatBotman men siz bilan suhbatlashish uchun yaratilganman."

    elif "xayrli kun" in message_text:
        return "Sizga ham xayrli kun."

    elif "men kimman" in message_text:
        return "Siz insonsiz."

    elif "qayerdansan" in message_text:
        return "Men virtual botman va joylashuvim internetda."

    elif "nima qilayapsan" in message_text:
        return "Men siz bilan suhbatlashayapman."

    elif "rahmat" in message_text:
        return "Yordam bera olganimdan mamnunman."
    
    elif "seni kim yaratgan" in message_text:
        return "Meni 👉ADHAM👈 yaratgan lekin juda mukammal emasman❗"

    else:
        return "Bu savolga javob bera olmayman. Yana biror narsa so'rang."

# Pastki bo‘limli menyu yaratamiz
def create_main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    button1 = KeyboardButton("Isming kim❓")
    button2 = KeyboardButton("Seni kim yaratgan❓")
    button3 = KeyboardButton("ChatGPT bilan suhbat✅")
    
    markup.add(button1, button2, button3)
    return markup

# /start va /help komandalariga javob
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    main_menu = create_main_menu()
    first_name = message.from_user.first_name
    welcome_message_text = f"Assalomu alaykum🙋‍♂️🙋‍♂️ {first_name}🙋‍♂️🙋‍♂️! Men o‘zbek tilidagi suhbatdosh botman. Sizga qanday yordam bera olaman🤖 ❗"

    welcome_message = bot.reply_to(message, welcome_message_text, reply_markup=main_menu)
    
    # Yangi xabarlar identifikatorini ro'yxatga qo'shamiz
    message_history.append(message.id)  # /start xabari
    message_history.append(welcome_message.id)  # Botning javobi
    update_user_activity(message.chat.id)

# Medialarni qayta ishlash uchun alohida handlerlar
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Kechirasiz, men rasm o'qiy olmayman. Men faqat suhbatlashaman.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    bot.reply_to(message, "Kechirasiz, men fayl o'qiy olmayman. Men faqat suhbatlashaman.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "Kechirasiz, men video o'qiy olmayman. Men faqat suhbatlashaman.")

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.reply_to(message, "Kechirasiz, men stiker o'qiy olmayman. Men faqat suhbatlashaman.")

@bot.message_handler(content_types=['animation'])
def handle_animation(message):
    bot.reply_to(message, "Kechirasiz, men gif o'qiy olmayman. Men faqat suhbatlashaman.")

@bot.message_handler(content_types=['emoji'])
def handle_emoji(message):
    bot.reply_to(message, "Kechirasiz, men emoji o'qiy olmayman. Men faqat suhbatlashaman.")

# Foydalanuvchining xabarlariga javob qaytarish
@bot.message_handler(func=lambda message: message.content_type == 'text')
def respond_to_message(message):
    user_message = message.text
    user_id = message.from_user.id

    # Foydalanuvchini yangilash 
    update_user_activity(user_id)

    if user_message == "ChatGPT bilan suhbat✅":
        markup = InlineKeyboardMarkup()
        chatgpt_button = InlineKeyboardButton("ChatGPT bilan suhbatlashing✅", url="https://chat.openai.com/")
        markup.add(chatgpt_button)
        sent_message = bot.reply_to(message, "Assalomu alaykum❗ ChatGPT bilan suhbatlashish uchun tugmani bosing", reply_markup=markup)
    
    elif user_message == "Isming kim❓":
        sent_message = bot.reply_to(message, "Mening ismim ChatBot🤖 O‘zbek tilida suhbatlashaman. Qo'shimcha savollaringiz bo'lsa tepada yozishingiz mumkin❗")
    
    elif user_message == "Seni kim yaratgan❓":
        sent_message = bot.reply_to(message, "Meni 👉ADHAM👈 yaratgan lekin juda mukammal emasman❗Qo'shimcha savollaringiz bo'lsa tepada yozishingiz mumkin❗")

    else:
        corrected_message = uzbek_text_analysis(user_message)
        response = get_response(message)
        sent_message = bot.reply_to(message, response)
    
    # Yangi xabarlar identifikatorini ro'yxatga qo'shamiz
    message_history.append(message.id)
    message_history.append(sent_message.id)

# Oylik faol foydalanuvchilar sonini ko'rsatish uchun funksiya
@bot.message_handler(commands=['stats'])
def send_monthly_stats(message):
    active_users = get_monthly_active_users()
    bot.reply_to(message, f"Oylik faol foydalanuvchilar soni: {active_users}")

# Botni ishga tushirish
bot.polling()