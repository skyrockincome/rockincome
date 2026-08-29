import telebot
import sqlite3
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") 
bot = telebot.TeleBot(BOT_TOKEN)

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
            (user_id, name, balance, referrals, ref_by)''')
conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if c.fetchone() is None:
        ref_by = message.text.split()[1] if len(message.text.split()) > 1 else 0
        c.execute("INSERT INTO users VALUES (?,?,?,?,?)", (user_id, name, 0, 0, ref_by))
        conn.commit()
        bot.send_message(user_id, f"Welcome {name}! 🎉\nYou joined RockIncome Tasks")
    else:
        bot.send_message(user_id, f"Welcome back {name}!")
    bot.send_message(user_id, "Use /tasks to earn, /balance to check money, /referrals for your link")

@bot.message_handler(commands=['tasks'])
def tasks(message):
    text = "Available Tasks:\n\n1. Follow our IG = ₦30\nSend screenshot\n2. Join Channel = ₦20\nSend screenshot\nMore tasks coming soon!"
    bot.send_message(message.from_user.id, text)

@bot.message_handler(commands=['balance'])
def balance(message):
    c.execute("SELECT balance FROM users WHERE user_id=?", (message.from_user.id,))
    result = c.fetchone()
    bal = result[0] if result else 0
    bot.send_message(message.from_user.id, f"Your Balance: ₦{bal}")

@bot.message_handler(commands=['referrals'])
def referrals(message):
    link = f"https://t.me/rockincome_bot?start={message.from_user.id}"
    bot.send_message(message.from_user.id, f"Your Referral Link:\n{link}\n\nEarn 10% of what your friends earn!")

bot.infinity_polling()
