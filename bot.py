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
    print(f"[LOG] /start received from user_id: {user_id}")
    
    if user_id == OWNER_ID:
        print(f"[LOG] Owner accessed /start. Current pending_messages: {pending_messages}")
        if pending_messages:
            bot.send_message(OWNER_ID, "📩 پیام‌های جدید:")
            for msg in pending_messages:
                username = msg.get('username', 'بدون_یوزرنیم')
                text = msg.get('text', '')
                bot.send_message(OWNER_ID, f"از @{username} (ID: @id{msg['user_id']}):\n{text}")
            pending_messages.clear()
            bot.send_message(OWNER_ID, "✅ پیام‌ها به‌روزرسانی و پاک شدن.")
        else:
            bot.send_message(OWNER_ID, "ℹ️ هیچ پیام جدیدی نیست.")
    else:
        bot.send_message(message.chat.id, "سلام! 👋\nاگر پیام بدید، مستقیم می‌ره پیش پشتیبانی. هر چی بنویسید، ارسال می‌شه.")
        print(f"[LOG] Welcome message sent to user_id: {user_id}")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_id = message.from_user.id
    text = message.text
    print(f"[LOG] Message received from user_id: {user_id}, text: {text}")
    
    if user_id == OWNER_ID:
        # برای صاحب بات: چک کردن فرمت پاسخ @username یا @idعددی
        if text.startswith('@') and ' ' in text:
            parts = text.split(' ', 1)
            target = parts[0][1:]  # حذف @ از اول
            reply_text = parts[1]
            
            try:
                if target.startswith('id'):
                    # فرمت @idعددی
                    target_id = int(target[2:])  # حذف id از اول
                    bot.send_message(target_id, f"پاسخ پشتیبانی:\n{reply_text}")
                    bot.send_message(OWNER_ID, f"✅ پاسخ به ID {target_id} ارسال شد.")
                    print(f"[LOG] Reply sent to user_id: {target_id}")
                else:
                    # فرمت @username
                    target_id = None
                    for msg in pending_messages:
                        if msg.get('username') == target:
                            target_id = msg['user_id']
                            break
                    if target_id:
                        bot.send_message(target_id, f"پاسخ پشتیبانی:\n{reply_text}")
                        bot.send_message(OWNER_ID, f"✅ پاسخ به @{target} ارسال شد.")
                        print(f"[LOG] Reply sent to username: @{target}, user_id: {target_id}")
                    else:
                        bot.send_message(OWNER_ID, f"❌ خطا: یوزرنیم @{target} پیدا نشد.")
                        print(f"[LOG] Username @{target} not found")
            except ValueError:
                bot.send_message(OWNER_ID, f"❌ خطا: آیدی {target} باید عددی باشه (مثل @id123456789).")
                print(f"[LOG] Invalid ID format: {target}")
            except Exception as e:
                bot.send_message(OWNER_ID, f"❌ خطا در ارسال به {target}: {str(e)}")
                print(f"[LOG] Error sending to {target}: {str(e)}")
            return
    
        bot.send_message(OWNER_ID, "⚠️ فرمت پاسخ باید اینجوری باشه: @username متن یا @id123456789 متن")
        print(f"[LOG] Invalid reply format from owner")
        return
    
    # برای کاربران عادی: ذخیره و تأیید
    username = message.from_user.username or "بدون_یوزرنیم"
    pending_messages.append({
        'user_id': user_id,
        'username': username,
        'text': text
    })
    print(f"[LOG] Message stored in pending_messages: {pending_messages}")
    
    # ارسال بلافاصله به صاحب
    try:
        bot.send_message(OWNER_ID, f"🆕 پیام جدید از @{username} (ID: @id{user_id}):\n{text}")
        print(f"[LOG] Notification sent to owner for user_id: {user_id}")
    except Exception as e:
        print(f"[LOG] Error sending notification to owner: {str(e)}")
    
    # تأیید به کاربر
    bot.send_message(message.chat.id, "✅ پیام شما به پشتیبانی ارسال شد. منتظر پاسخ باشید!")
    print(f"[LOG] Confirmation sent to user_id: {user_id}")

# اجرای بات
if __name__ == '__main__':
    print("بات شروع شد...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"[LOG] Error in polling: {str(e)}")
