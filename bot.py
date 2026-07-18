import telebot
import time
import os
from telebot import types

# ================== CONFIGURATION ==================
TOKEN = 'YOUR_BOT_TOKEN_HERE'                    # ← Put your bot token
GROUP_CHAT_ID = -100XXXXXXXXXX                   # ← Your group ID
CHANNEL_CHAT_ID = -100YYYYYYYYYY                 # ← Your channel ID
BAN_WORDS = ["nahi chlra", "bekar", "dm"]        # Add more lowercase words
WOW_IMAGE_PATH = 'wow.jpg'                       # Must be in same folder
# ===================================================

bot = telebot.TeleBot(TOKEN)

def is_admin(chat_id, user_id):
    """Check if user is admin/owner"""
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.id != GROUP_CHAT_ID:
        return
    
    # Download the highest quality photo
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Temporary save
    temp_path = 'temp_photo.jpg'
    with open(temp_path, 'wb') as f:
        f.write(downloaded_file)
    
    # Send to channel WITHOUT caption or sender info
    with open(temp_path, 'rb') as photo:
        bot.send_photo(CHANNEL_CHAT_ID, photo)
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    if message.chat.id != GROUP_CHAT_ID or not message.text:
        return
    
    user_id = message.from_user.id
    text_lower = message.text.lower()
    
    # === Special Trigger Message ===
    trigger = "⏳ wait...ya toh tune ping ka ss ni dia ya pahle se attack laga hua hai".lower()
    if trigger in text_lower:
        if os.path.exists(WOW_IMAGE_PATH):
            # Send wow.jpg in group
            with open(WOW_IMAGE_PATH, 'rb') as img:
                sent = bot.send_photo(GROUP_CHAT_ID, img)
            
            # Auto-delete after 3 seconds
            time.sleep(3)
            try:
                bot.delete_message(GROUP_CHAT_ID, sent.message_id)
            except:
                pass
        return  # Do NOT forward to channel

    # === Ban Words Filter (only normal members) ===
    if any(bw.lower() in text_lower for bw in BAN_WORDS):
        if not is_admin(GROUP_CHAT_ID, user_id) and user_id != bot.get_me().id:
            try:
                bot.delete_message(GROUP_CHAT_ID, message.message_id)
            except:
                pass
        return

# Start the bot
if __name__ == '__main__':
    print("🤖 Bot is running... (Images → Channel | Ban words | Special wow.jpg)")
    bot.infinity_polling()
