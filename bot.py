import telebot
from telebot import types

# توکن بات
TOKEN = '8251776630:AAEimkTlsAHuhnCDS-dOXV6rjUcVVY_0Ct8'

# آیدی عددی صاحب بات (@zoro_900official)
OWNER_ID = 8251776630

bot = telebot.TeleBot(TOKEN)

# لیست برای ذخیره پیام‌های جدید
pending_messages = []

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    
    if user_id == OWNER_ID:
        # برای صاحب بات: نمایش پیام‌های جدید
        if pending_messages:
            bot.send_message(OWNER_ID, "📩 پیام‌های جدید:")
            for msg in pending_messages:
                username = msg.get('username', 'بدون_یوزرنیم')
                text = msg.get('text', '')
                bot.send_message(OWNER_ID, f"از @{username} (ID: {msg['user_id']}):\n{text}")
            pending_messages.clear()
            bot.send_message(OWNER_ID, "✅ پیام‌ها به‌روزرسانی و پاک شدن.")
        else:
            bot.send_message(OWNER_ID, "ℹ️ هیچ پیام جدیدی نیست.")
    else:
        # برای کاربران عادی: پیام خوش‌آمدگویی
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, "سلام! 👋\nاگر پیام بدید، مستقیم می‌ره پیش پشتیبانی. هر چی بنویسید، ارسال می‌شه.")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_id = message.from_user.id
    text = message.text
    
    if user_id == OWNER_ID:
        # برای صاحب بات: چک کردن فرمت پاسخ @idexample متن
        if text.startswith('@id') and ' ' in text:
            parts = text.split(' ', 1)
            target_id = parts[0][3:]  # حذف @id از اول
            reply_text = parts[1]
            
            try:
                # ارسال به user_id (با chat_id که همون user_id هست)
                bot.send_message(int(target_id), f"پاسخ پشتیبانی:\n{reply_text}")
                bot.send_message(OWNER_ID, f"✅ پاسخ به ID {target_id} ارسال شد.")
            except ValueError:
                bot.send_message(OWNER_ID, f"❌ خطا: آیدی {target_id} باید عددی باشه.")
            except Exception as e:
                bot.send_message(OWNER_ID, f"❌ خطا در ارسال به ID {target_id}: {str(e)}")
            return
    
        # اگر فرمت درست نبود، به صاحب اطلاع بده
        bot.send_message(OWNER_ID, "⚠️ فرمت پاسخ باید اینجوری باشه: @id123456789 متن")
        return
    
    # برای کاربران عادی: ذخیره و تأیید
    username = message.from_user.username or "بدون_یوزرنیم"
    pending_messages.append({
        'user_id': user_id,
        'username': username,
        'text': text
    })
    
    # ارسال بلافاصله به صاحب (با فرمت @id + user_id)
    bot.send_message(OWNER_ID, f"🆕 پیام جدید از @{username} (ID: @id{user_id}):\n{text}")
    
    # تأیید به کاربر
    bot.send_message(message.chat.id, "✅ پیام شما به پشتیبانی ارسال شد. منتظر پاسخ باشید!")

# اجرای بات
if __name__ == '__main__':
    print("بات شروع شد...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"خطا در اجرا: {e}")
