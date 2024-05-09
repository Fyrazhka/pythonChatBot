import re
from random import random, randint
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import datetime


TOKEN = '6811190281:AAGyrZjcONPUSSMSYGPBg0VY_Z-7oNHdwJ8'
users_info_set = set()

# Функция для приветствия нового участника в группе
async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    new_members = update.effective_message.new_chat_members
    for member in new_members:
        welcome_message=f"""⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛
        Приветствуем, {member.first_name}!
        Рады видеть в кубическом и многопространственном сообществе.
        
        Спешу уведомить, как новичка, что имея большое желание
        нужно скинуться на новые обои в беседу.
        Это поспособствует позитивной и уважительной обстановке
        
        Мы всегда доброжелательны к тебе и другим (по возможности)
        Наши возрастные рамки от 14-24 лет.
        
        Наши преимущества на данный момент:
        🖤 удобный интерфейс
        🖤 опросы
        🖤 викторины
        🖤 игры
        🖤 понимающий и не очень коллектив
        🖤 индивидуальный подход и раскрытие каждого участника
        🖤 сбор средств админу на пиццу
        🖤 в сообщество можно пригласить родителей (если их по какой-то странной причине ещё здесь нет)
        
        ({member.first_name})ОБЯЗАТЕЛЬНО ознакомься с правилами нашего сообщества. В закрепе.
        Админ потом спросит на память.
        
        🤍Расскажи нам в краце о себе, мы с удовольствием тебя послушаем.
        Не забудь сказать нам 3 цифры на обороте карты!🤗🤍
        
        
        ⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛"""
        await context.bot.send_message(chat_id=chat_id, text=welcome_message)

# Функция для оповещения о выходе участника из группы
async def leave_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    left_members = update.effective_message.left_chat_member
    if left_members:
        leave_message = f"{left_members.first_name} покинул группу. Всего хорошего!"
        await context.bot.send_message(chat_id=chat_id, text=leave_message)


# Функция для обработки команд и текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "/start":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для группы.")


async def random_number(update, context):
    chat_id = update.effective_chat.id
    try:
        match = re.search(r'^/random\s+(\d+)-(\d+)$', update.message.text)
        print("Match:", update.message.text+" "+str(match)+" "+str(match.groups()))
        if match:
            start, end = match.groups()
            start = int(start)
            end = int(end)
            random_num = randint(start, end)
            await context.bot.send_message(chat_id=chat_id, text=f"Случайное число: {random_num}")
        else:
           await context.bot.send_message(chat_id=chat_id, text="Неверный формат команды. Используйте: /random 1-100")
    except Exception as e:
        print("Error:", e)
        await context.bot.send_message(chat_id=chat_id, text="Произошла ошибка при обработке команды.")

async def display_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    rules_message = """
    ОБЩИЕ ПРАВИЛА
    🔪 
    1. Уважение: 
    Следует проявлять уважение к собеседникам, избегая оскорблений, унижений и агрессивного поведения.
    По возможности.
    
    2. Не спамить: 
    Избегайте массовых рассылок или повторных сообщений без необходимости.
    За исключением порнографии.
    
    3. Уважение чужих мнений:
    Важно уважать различные точки зрения и начинать конфликты из-за разногласий.
    
    4. Не разглашать личную информацию: 
    Делитесь личными данными или конфиденциальной информацией в открытой беседе с открытыми людьми.
    
    5.Толерантность: 
    Мы толерантное общество и оскорбления не приветствуем. 
    В особенности называть человека:
    Червем - указывать на отсутствие конечностей у человека.
    Чурбаном - указывать на бесполезность человека.
    Гусем - указывать на утиное лицо человека.
    Злым - указывать на недоброжелательность человека.
    
    Эти правила помогут создать приятную и уважительную обстановку с участниками. 🔪
        """
    await context.bot.send_message(chat_id=chat_id, text=rules_message)


# Функция для временного мута участника
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.message.from_user
    chat_member = await context.bot.get_chat_member(chat_id, user.id)
    if chat_member.status == "administrator" or chat_member.status == "creator":
        try:
            command, username, mute_time_str = update.message.text.split()
            mute_time = int(mute_time_str)
            user_id = find_user_id_by_username(username)
            if user_id is None:
                await context.bot.send_message(chat_id=chat_id, text="Пользователь с таким именем не найден.")
                return
            user = await context.bot.get_chat_member(chat_id, user_id)
            if user.status in ["creator", "administrator"]:
                await context.bot.send_message(chat_id=chat_id, text="Невозможно замутить администратора или создателя группы.")
                return

            # Получаем текущее время в UTC
            current_time_utc = datetime.datetime.now(datetime.UTC)
            # Вычисляем длительность мута и прибавляем ее к текущему времени
            until_date_utc = current_time_utc + datetime.timedelta(seconds=mute_time)

            await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=ChatPermissions(can_send_messages=False), until_date=until_date_utc)
            await context.bot.send_message(chat_id=chat_id, text=f"Пользователь {user.user.username} был замучен на {mute_time} сек.")
        except (IndexError, ValueError):
            await context.bot.send_message(chat_id=chat_id, text="Неверный формат команды. Используйте: /mute username 300")


async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.message.from_user
    chat_member = await context.bot.get_chat_member(chat_id, user.id)
    if chat_member.status == "administrator" or chat_member.status == "creator":
        try:
            command, username = update.message.text.split()
            user_id = find_user_id_by_username(username)
            if user_id is None:
                await context.bot.send_message(chat_id=chat_id, text="Пользователь с таким именем не найден.")
                return
            user = await context.bot.get_chat_member(chat_id, user_id)
            if user.status in ["creator", "administrator"]:
                await context.bot.send_message(chat_id=chat_id, text="Невозможно замутить администратора или создателя группы.")
                return

            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.send_message(chat_id=chat_id, text=f"Пользователь {user.user.username} был исключен из беседы.")
        except (IndexError, ValueError):
            await context.bot.send_message(chat_id=chat_id, text="Неверный формат команды. Используйте: /kick username")

def find_user_id_by_username(username):
    with open('user_info.txt', 'r') as file:
        for line in file:
            line_username, user_id = line.strip().split(' ')
            if line_username == username:
                return int(user_id)
    return None

async def delete_message_containing_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_text = update.effective_message.text
    message_sender = update.effective_message.from_user
    print(message_text+ " "+str(message_sender ))
    user_info = (message_sender.username, message_sender.id)
    users_info_set.add(user_info)
    save_users_info_to_file(users_info_set)
    # Удаляем сообщения, если они отправлены от пользователя El_futurRo
    if message_sender.is_bot == True:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.effective_message.message_id)

    # Проверяем наличие определенных текстов и удаляем сообщение при необходимости
    if "@ChatKeeperBot" in message_text or "@ChatKeeperBotEN" in message_text:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.effective_message.message_id)

def save_users_info_to_file(users_info_set):
    with open('user_info.txt', 'w') as file:
        for user_info in users_info_set:
            file.write(f"{user_info[0]} {user_info[1]}\n")
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    welcome_handler = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_user)
    application.add_handler(welcome_handler)

    leave_handler = MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, leave_user)
    application.add_handler(leave_handler)

    random_handler = CommandHandler("random", random_number)
    application.add_handler(random_handler)

    rules_handler = CommandHandler("rules", display_rules)
    application.add_handler(rules_handler)

    mute_handler = CommandHandler("mute", mute_user)
    application.add_handler(mute_handler)

    kick_handler = CommandHandler("kick", kick_user)
    application.add_handler(kick_handler)

    delete_handler = MessageHandler(filters=filters.TEXT, callback=delete_message_containing_text)
    application.add_handler(delete_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == '__main__':
    main()