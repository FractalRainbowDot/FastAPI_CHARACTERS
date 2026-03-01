import logging
import os
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import html

# Загружаем переменные из .env файла в окружение
load_dotenv()

# --- Конфигурация ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Теперь os.getenv сможет найти переменную, загруженную из .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Правильный базовый URL, включающий префикс из main.py
API_BASE_URL = "http://127.0.0.1:8000/api/v1"


# --- Команды Бота ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    # Экранируем < и > чтобы избежать ошибки парсинга HTML
    create_example = html.escape("/create <имя> <класс>")
    delete_example = html.escape("/delete <ID>")
    pve_example = html.escape("/pve <ID персонажа> <уровень огра>")
    
    await update.effective_message.reply_html(
        rf"Привет, {update.effective_user.mention_html()}!"
        "\n\nЯ бот для управления персонажами в вашей игре."
        "\n\n<b>Основные команды:</b>"
        "\n/list - Показать всех персонажей"
        f"\n{create_example} - Создать персонажа"
        f"\n{delete_example} - Удалить персонажа"
        f"\n{pve_example} - Бой с огром"
        "\n\n<b>Доступные классы:</b> warrior, mage, rogue, cleric"
        "\n\n<b>Примеры:</b>"
        "\n/create Legolas rogue"
        "\n/pve 1 5"
    )


async def list_characters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получает и отображает список всех персонажей."""
    async with httpx.AsyncClient() as client:
        try:
            # Запрос теперь идет на правильный URL: http://127.0.0.1:8000/api/v1/characters/
            response = await client.get(f"{API_BASE_URL}/characters/")
            response.raise_for_status()

            characters = response.json()
            if not characters:
                await update.effective_message.reply_text("Персонажей пока нет.")
                return

            message = "<b>📜 Список персонажей:</b>\n\n"
            for char in characters:
                status = "✅" if char['alive'] else "💀"
                message += (
                    f"{status} <b>{html.escape(char['name'])}</b> (ID: {char['id']})\n"
                    f"    Класс: {char['char_class']}\n"
                    f"    HP: {char['current_health']} / {char['max_health']}\n"
                    f"    Уровень: {char['level']}\n\n"
                )
            await update.effective_message.reply_html(message)

        except httpx.RequestError as exc:
            logger.error(f"Ошибка запроса к API: {exc}")
            await update.effective_message.reply_text("Не удалось подключиться к серверу игры.")
        except httpx.HTTPStatusError as exc:
            logger.error(f"Ошибка статуса API: {exc.response.status_code} - {exc.response.text}")
            await update.effective_message.reply_text(f"Сервер игры вернул ошибку: {exc.response.status_code}")


async def create_character(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Создает нового персонажа."""
    args = context.args
    if len(args) != 2:
        await update.effective_message.reply_text(
            "Неверный формат. Используйте:\n" + html.escape("/create <имя> <класс>")
        )
        return

    name, char_class = args
    payload = {"name": name, "char_class": char_class.lower()}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{API_BASE_URL}/characters/", json=payload)
            response.raise_for_status()

            new_char = response.json()
            await update.effective_message.reply_html(
                f"🎉 Персонаж <b>{html.escape(new_char['name'])}</b> успешно создан!\n"
                f"<b>ID:</b> {new_char['id']}, <b>Класс:</b> {new_char['char_class']}"
            )

        except httpx.RequestError:
            await update.effective_message.reply_text("Не удалось подключиться к серверу игры.")
        except httpx.HTTPStatusError as exc:
            try:
                details = exc.response.json().get("detail", "Неизвестная ошибка.")
                if isinstance(details, list): # Обработка ошибок валидации Pydantic
                    error_messages = [err.get('msg', 'Ошибка') for err in details]
                    details = ". ".join(error_messages)
            except Exception:
                details = exc.response.text
            await update.effective_message.reply_text(f"Ошибка при создании: {details}")


async def delete_character(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаляет персонажа по ID."""
    if not context.args or not context.args[0].isdigit():
        await update.effective_message.reply_text("Укажите ID персонажа для удаления.\n" + html.escape("/delete <ID>"))
        return

    char_id = int(context.args[0])
    payload = {"id": char_id}

    async with httpx.AsyncClient() as client:
        try:
            # Обратите внимание: FastAPI ожидает тело запроса для DELETE
            response = await client.request("DELETE", f"{API_BASE_URL}/characters/", json=payload)
            response.raise_for_status()

            result = response.json()
            await update.effective_message.reply_text(result.get("message", "Персонаж удален."))

        except httpx.RequestError:
            await update.effective_message.reply_text("Не удалось подключиться к серверу игры.")
        except httpx.HTTPStatusError as exc:
            details = exc.response.json().get("detail", "Персонаж не найден или произошла ошибка.")
            await update.effective_message.reply_text(f"Ошибка: {details}")


async def pve_battle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запускает PvE бой."""
    args = context.args
    if len(args) != 2 or not args[0].isdigit() or not args[1].isdigit():
        await update.effective_message.reply_text(
            "Неверный формат. Используйте:\n" + html.escape("/pve <ID персонажа> <уровень огра>")
        )
        return

    attacker_id, npc_level = map(int, args)
    
    async with httpx.AsyncClient() as client:
        try:
            # POST запрос с query-параметрами
            response = await client.post(
                f"{API_BASE_URL}/battle/pve/{attacker_id}",
                params={"npc_level": npc_level}
            )
            response.raise_for_status()

            result = response.json()
            log_data = result.get("log", [])
            
            if not log_data:
                await update.effective_message.reply_text("Бой завершился без логов.")
                return

            # --- ИСПРАВЛЕНИЕ ---
            # Проверяем, является ли лог строкой. Если да, разбиваем ее на список.
            log_lines = []
            if isinstance(log_data, str):
                # Используем split() для разделения по пробелам, которые вы добавляли в логгере
                log_lines = log_data.strip().split('  ') # Разделяем по двойному пробелу или адаптируем
            elif isinstance(log_data, list):
                log_lines = log_data

            # Убираем пустые строки, которые могли появиться после разделения
            log_lines = [line.strip() for line in log_lines if line.strip()]

            # Форматируем лог для красивого вывода
            battle_report = "<b>⚔️ Отчет о бое:</b>\n\n" + "\n".join(html.escape(line) for line in log_lines)
            await update.effective_message.reply_html(battle_report)

        except httpx.RequestError:
            await update.effective_message.reply_text("Не удалось подключиться к серверу игры.")
        except httpx.HTTPStatusError as exc:
            details = exc.response.json().get("detail", "Произошла ошибка в бою.")
            await update.effective_message.reply_text(f"Ошибка: {details}")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на неизвестные команды."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не знаю такой команды.")


def main() -> None:
    """Запускает бота."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("!!! Токен не найден. Укажите TELEGRAM_BOT_TOKEN в вашем .env файле !!!")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", list_characters))
    application.add_handler(CommandHandler("create", create_character))
    application.add_handler(CommandHandler("delete", delete_character))
    application.add_handler(CommandHandler("pve", pve_battle))

    # Обработчик для неизвестных команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Бот запускается...")
    application.run_polling()


if __name__ == "__main__":
    main()
