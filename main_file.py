from typing import Final
import telegram.constants
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN : Final = '6425279982:AAGCB742RG0O52ZW7gsgy9A8YEwtvCzh2mc'
BOT_USERNAME : Final = '@queue_3213_bot'
queue = []
skippers = []
answerer: int = -1
whitelist = [int(i) for i in open('whitelist.txt').readlines()]

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(update.message.chat_id, f'Привет! Это бот на очередь, напиши /help для более подробной информации', 'HTML')
    print(f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} start_command in {update.message.chat.type}\n'
          f'========================\n'
          f'{update.message.from_user.id}\n'
          f'========================')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(update.message.chat_id, f'<b>Для всех</b>\U0001F610\n'
                                                          f'/start - Получить приветствующее сообщение\n'
                                                          f'/help - Выводит список команд\n'
                                                          f'/list - Выводит очередь\n'
                                                          f'/join - Войти в очередь\n'
                                                          f'/skip - Даёт остальным возможность идти вперёд тебя, без потери своего места\n'
                                                          f'/return - Возвращает обратно в очередь, после /skip\n'
                                                          f'/leave - Выйти из очереди\n\n'
                                                          f'<b>Только для тех, кто в whitelist`е</b>\U0001F913\n'
                                                          f'/next - Вызывает человека\n'
                                                          f'/clear - Очищает очередь\n\n'
                                                          f'<b>Только для разработчика</b>\U0001F60E\n'
                                                          f'/whitelist_add - Добавить человека в whitelist\n'
                                                 /         f'/whitelist_remove - Удалить человека из whitelist`а',
                                  'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} help_command in {update.message.chat.type}')

async def queue_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = f"<a href='tg://user?id={update.message.from_user.id}'>{update.message.from_user.username}</a>"
    if user not in queue:
        queue.append(user)
        await context.bot.sendMessage(update.message.chat_id, f'{user} был добавлен в очередь!', 'HTML')
    else:
        await context.bot.sendMessage(update.message.chat_id, f'{user} ты не можешь добавиться в очередь дважды', 'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} queue_add in {update.message.chat.type}')

async def queue_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = f"<a href='tg://user?id={update.message.from_user.id}'>{update.message.from_user.username}</a>"
    if user not in skippers and user in queue:
        skippers.append(user)
        await context.bot.sendMessage(update.message.chat_id, f'{user} был добавлен в пропускающих!', 'HTML')
    elif user not in queue:
        await context.bot.sendMessage(update.message.chat_id, f'{user} тебе нужно сначала войти в очередь', 'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} queue_skip in {update.message.chat.type}')

async def queue_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = f"<a href='tg://user?id={update.message.from_user.id}'>{update.message.from_user.username}</a>"
    if user in skippers:
        skippers.remove(user)
        await context.bot.sendMessage(update.message.chat_id, f'{user} вернулся в очередь!', 'HTML')
    else:
        await context.bot.sendMessage(update.message.chat_id, f'{user} ты не можешь вернуться в очередь так как тебя нет в пропускающих', 'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} queue_return in {update.message.chat.type}')

def __get_user():
    for user in queue:
        if user not in skippers:
            return user
    return 'null'

async def queue_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.from_user.id
    if id in whitelist:
        user = __get_user()
        if (user == 'null'):
            await context.bot.sendMessage(update.message.chat_id, f'Никого нет в очереди', 'HTML')
        else:
            await context.bot.sendMessage(update.message.chat_id, f'Поторопись, {user}, настал твой черёд!', 'HTML')
            queue.remove(user)
    else:
        await context.bot.sendMessage(update.message.chat_id, f'Извини, у тебя нет прав', 'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} next in {update.message.chat.type}')

async def queue_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    line: str = '<b>ОЧЕРЕДЬ</b>'
    if len(queue) == 0:
        line += ' пуста'
    else:
        line += '\n'
        for i in range (0, len(queue)):
            line += f'{i + 1}) {queue[i]}\n'
        if len(skippers) != 0:
            line += '\n<b>ПРОПУСКАЮЩИЕ</b>\n'
            for j in range (0, len(skippers)):
                line += f'{j + 1}) {skippers[j]}\n'
    await context.bot.sendMessage(update.message.chat_id, line, 'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} queue_list in {update.message.chat.type}')

async def queue_leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = f"<a href='tg://user?id={update.message.from_user.id}'>{update.message.from_user.username}</a>"
    if user in skippers:
        skippers.remove(user)
    if user in queue:
        queue.remove(user)
    await context.bot.sendMessage(update.message.chat_id, f'{user} вышел из очереди!', 'HTML')
    print(
        f'{datetime.now().strftime('%H:%M:%S')} {update.message.from_user.username} queue_delete in {update.message.chat.type}')

async def queue_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.from_user.id
    if id in whitelist:
        queue.clear()
        skippers.clear()
        await context.bot.sendMessage(update.message.chat_id, f'Очередь была очищена!', 'HTML')
    else:
        await context.bot.sendMessage(update.message.chat_id, f'Извини, у тебя нет прав', 'HTML')
    print(
        f'************************\n'
        f'{datetime.now().strftime('%H:%M:%S')} '
        f'{update.message.from_user.username} clear in {update.message.chat.type}\n'
        f'************************')

async def whitelist_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == 826871795:
        file = open('whitelist.txt', 'r')
        lines = file.readlines()
        file.close()
        file = open('whitelist.txt', 'w')
        lines.append(update.message.text.replace(BOT_USERNAME, '').replace('/whitelist_add', '').strip() + '\n')
        file.writelines(lines)
        file.close()
        await context.bot.sendMessage(update.message.chat_id, f'Пользователь был добавлен в whitelist', 'HTML')
    else:
        await context.bot.sendMessage(update.message.chat_id, f'Извини, у тебя нет прав', 'HTML')
    print(
        f'************************\n'
        f'{datetime.now().strftime('%H:%M:%S')} '
        f'{update.message.from_user.username} whitelist_add in {update.message.chat.type}\n'
        f'************************')

async def whitelist_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == 826871795:
        file = open('whitelist.txt', 'r')
        lines = file.readlines()
        user = update.message.text.replace(BOT_USERNAME, '').replace('/whitelist_remove', '').strip()
        file = open('whitelist.txt', 'w')
        for line in lines:
            if user != line.strip():
                file.write(line)
        await context.bot.sendMessage(update.message.chat_id, f'Пользователь был удалён из whitelist`а', 'HTML')
        file.close()
    else:
        await context.bot.sendMessage(update.message.chat_id, f'Извини, у тебя нет прав', 'HTML')
    print(
        f'************************\n'
        f'{datetime.now().strftime('%H:%M:%S')} '
        f'{update.message.from_user.username} whitelist_remove in {update.message.chat.type}\n'
        f'************************')

# Responses handler
def handle_response(text) -> str:
    if 'очередь' in text:
        print(text)
        return 'напиши /join чтобы войти в очередь'
    return ''

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private' or BOT_USERNAME in update.message.text:
        text: str = update.message.chat.type + ': ' + update.message.text.replace(BOT_USERNAME, '').strip().lower()
        response: str = handle_response(text)
        await  context.bot.sendMessage(update.message.chat_id, response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"{datetime.now().strftime('%H:%M:%S')} {Update.message.from_user.username} in {update.message.chat.type} "
          f"chat caused error \"{context.error}\"\n"
          f"{update}\"")



#main
if __name__ == '__main__':
    print(f'{datetime.now().strftime('%H:%M:%S')} Starting the bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('join', queue_join))
    app.add_handler(CommandHandler('skip', queue_skip))
    app.add_handler(CommandHandler('return', queue_return))
    app.add_handler(CommandHandler('next', queue_next))
    app.add_handler(CommandHandler('list', queue_list))
    app.add_handler(CommandHandler('leave', queue_leave))
    app.add_handler(CommandHandler('clear', queue_clear))
    app.add_handler(CommandHandler('whitelist_add', whitelist_add))
    app.add_handler(CommandHandler('whitelist_remove', whitelist_remove))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print(f'{datetime.now().strftime('%H:%M:/%S')} Polling...')
    app.run_polling(poll_interval=3)

