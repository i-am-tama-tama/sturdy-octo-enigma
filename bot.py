
import subprocess
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ContextTypes
from datetime import datetime
import show_circle

BOT_TOKEN = "7278814940:AAGL59HQhLy1zGVwtUn_b_eylVtI05dAJDI"

def timesd():
    # Получаем текущую дату и время
    current_time = datetime.now()
    # Форматируем дату и время в строку
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return time_string

# Замените на ваш Telegram ID
AUTHORIZED_IDS = [1792031171, 6390378305]

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что запрос исходит от авторизованного пользователя
    if update.effective_user.id not in AUTHORIZED_IDS:
        # Предупреждаем владельца о попытке несанкционированного доступа
        for id in AUTHORIZED_IDS:
            await context.bot.send_message(
                chat_id=id,
                text=(
                    f"Попытка несанкционированного доступа: пользователь "
                    f"@{update.effective_user.username} ({update.effective_user.id}) "
                    f"вызвал команду /screenshot. {timesd()}"
                ),
            )
        # Не отвечаем на запрос неавторизованного пользователя
        return

    print(f"{update.effective_user.username} ({update.effective_user.id}) вызвал команду /screenshot {timesd()}")
    image_path = "/Users/annahodareva/.screenshot-tg-bot/screenshot.png"
    try:
        # Делаем скриншот
        subprocess.run(["screencapture", "-Cx", image_path], check=True)

        # Отправляем изображение пользователю и получаем объект Photo
        with open(image_path, "rb") as image_file:
            sent_photo = await update.message.reply_photo(photo=image_file)

        # Удаляем временный файл
        os.remove(image_path)

        # Получаем file_id отправленного фото
        file_id = sent_photo.photo[-1].file_id  # Берем последнее (самое большое) фото
        file_info = await context.bot.get_file(file_id)
        image_url = file_info.file_path

        # Создаем клавиатуру с WebApp-кнопкой
        keyboard = [[InlineKeyboardButton("Поставить указатель", web_app=WebAppInfo(url=f"https://i-am-tama-tama.github.io/sturdy-octo-enigma/pickpointer.html?image={image_url}"))]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # **Редактируем сообщение с фото**, добавляя к нему кнопку
        await sent_photo.edit_reply_markup(reply_markup)
        # Удаляем временный файл после отправки
        os.remove(image_path)
    except FileNotFoundError:
        await update.message.reply_text("Утилита screencapture не найдена. Убедитесь, что вы используете MacOS.")
    except subprocess.CalledProcessError:
        await update.message.reply_text("Ошибка при выполнении команды screencapture.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in AUTHORIZED_IDS:
        # Предупреждаем владельца о попытке несанкционированного доступа
        for id in AUTHORIZED_IDS:
            await context.bot.send_message(
                chat_id=id,
                text=(
                    f"Попытка несанкционированного доступа: пользователь "
                    f"@{update.effective_user.username} ({update.effective_user.id}) "
                    f"вызвал команду /start. {timesd()}"
                ),
            )
        # Не отвечаем на запрос неавторизованного пользователя
        return

    print(f"{update.effective_user.username} ({update.effective_user.id}) вызвал команду /start {timesd()}")
    await update.message.reply_text("Бот работает. Используйте команду /screenshot для скриншота.")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in AUTHORIZED_IDS:
        # Предупреждаем владельца о попытке несанкционированного доступа
        for id in AUTHORIZED_IDS:
            await context.bot.send_message(
                chat_id=id,
                text=(
                    f"Попытка несанкционированного доступа: пользователь "
                    f"@{update.effective_user.username} ({update.effective_user.id}) "
                    f"вызвал команду /start. {timesd()}"
                ),
            )
        # Не отвечаем на запрос неавторизованного пользователя
        return

    print(f"{update.effective_user.username} ({update.effective_user.id}) вызвал команду /alert {timesd()}")
    message = (update.message.text[7:] if len(update.message.text) > 7 and not update.message.text.__contains__("\"") else "Пустое сообщение")

    subprocess.run([
        "osascript", 
        "-e", f'display dialog "{message}" with title "Тама-Тама" buttons '+'{"OK"}'+' default button "OK"'
    ], check=True)
    await update.message.reply_text("Отправлено")

# Обработчик web_app_data (когда WebApp отправляет данные)
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data  # Получаем данные от WebApp
    await update.message.reply_text(f"Получены данные из WebApp: {data}")

def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего Telegram-бота
    
    # Создаем приложение
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("screenshot", screenshot))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))  # Обработка WebApp данных

    # Запускаем бота
    app.run_polling()

if __name__ == '__main__':
    # Screenshot test
    image_path = "/Users/annahodareva/.screenshot-tg-bot/screenshot.png"
    try:
        # Делаем скриншот с помощью утилиты screencapture (MacOS)
        subprocess.run(["screencapture", "-Cx", image_path], check=True)
        
        # Удаляем временный файл после отправки
        os.remove(image_path)
    except Exception as e:
        pass

    main()
