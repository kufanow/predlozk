import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ForceReply

# Настройки — замени на свои
BOT_TOKEN = '7311228660:AAHz-o_d0R19dB4TTlW0lOmznVHJGkMUft0'                    # Токен бота
INVITE_LINK = 'https://t.me/+Ru9BwuOgMJ0wNTdi'  # Пригласительная ссылка на приватный канал
CHANNEL_ID = -1003014944285                      # ID приватного канала (бот должен быть админом!)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Тексты для приветствия
start_texts = [
    "Привет! Это бот для предложений идей в наш закрытый канал 🔥\nЧтобы отправить свою идею, нужно быть подписчиком.",
    "Добро пожаловать! Хочешь предложить идею для контента? Сначала присоединяйся к нашему приватному каналу 👇",
    "Привет! У нас эксклюзивное сообщество. Подпишись, чтобы предлагать свои идеи 😏"
]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    subscribe_button = types.InlineKeyboardButton(
        text="Присоединиться к приватному каналу 🔒",
        url=INVITE_LINK
    )
    idea_button = types.InlineKeyboardButton(
        text="Предложить идею 💡",
        callback_data="check_idea"
    )
    keyboard.add(subscribe_button)
    keyboard.add(idea_button)

    text = random.choice(start_texts)
    await message.answer(
        f"{text}\n\n"
        "После подписки нажми «Предложить идею» или напиши /idea",
        reply_markup=keyboard
    )

# Обработка нажатия кнопки и команды /idea
@dp.callback_query_handler(text="check_idea")
@dp.message_handler(commands=['idea', 'предложить', 'идея'])
async def check_for_idea(event):
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()  # Убираем "часики" у кнопки
    else:
        message = event

    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            # Подписан — просим ввести идею
            await message.answer(
                "Отлично! Ты в канале ✅\n\n"
                "Напиши свою идею, предложение или пожелание. Я передам её администрации канала 📝",
                reply_markup=ForceReply(selective=True)
            )
        else:
            # Не подписан
            await send_not_subscribed(message.chat.id)
    except Exception:
        await send_not_subscribed(message.chat.id)

async def send_not_subscribed(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="Присоединиться к каналу 🔒",
        url=INVITE_LINK
    ))
    await bot.send_message(
        chat_id,
        "❌ Чтобы предлагать идеи, нужно быть подписчиком приватного канала.\n"
        "Присоединяйся по ссылке ниже, а потом возвращайся и пиши /idea",
        reply_markup=keyboard
    )

# Приём самой идеи (ответ на ForceReply или любое сообщение после успешной проверки)
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def receive_idea(message: types.Message):
    # Проверяем, является ли это ответом на запрос идеи
    if message.reply_to_message and "Напиши свою идею" in message.reply_to_message.text:
        try:
            member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
            if member.status in ['member', 'administrator', 'creator']:
                # Пересылаем идею тебе (владелец бота) или в специальный чат/канал
                admin_chat_id = 123456789  # ← Замени на свой Telegram ID или ID чата для идей
                await bot.send_message(
                    admin_chat_id,
                    f"Новая идея от пользователя {message.from_user.full_name} (@{message.from_user.username or 'no_username'}):\n\n"
                    f"{message.text}"
                )
                await message.answer("✅ Спасибо! Твоя идея отправлена администрации канала. Мы обязательно её рассмотрим 😊")
            else:
                await send_not_subscribed(message.chat.id)
        except Exception:
            await send_not_subscribedessage.chat.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)