from aiogram import Bot, Dispatcher, executor, types
import logging

from utils import voice_to_wav, find_face


API_TOKEN = ''  # здесь должен быть токен бота

logging.basicConfig(level=logging.INFO, filename="bot_logger.log", filemode="w")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer('Привет!\nЯ умею сохранять аудиосообщения и фото с лицами')


@dp.message_handler(content_types=['voice'])
async def dwnld_voice(message: types.Message):
    """Обработчик аудио сообщений, конвертирует и сохраняет в wav, удаляет оригинал"""
    filename = f'data/{message.from_user.id}/voice/audio_message_{message.message_id}.ogg'
    await message.voice.download(destination_file=filename)
    voice_to_wav(filename, message.message_id, message.from_user.id)
    await message.answer('Успешное сохранение вашей аудиозаписи!')


@dp.message_handler(content_types=['photo'])
async def dwnld_photo(message: types.Message):
    """Обработчик фото, распознает лицо и если есть то сохраняет фото"""
    filename = f'data/{message.from_user.id}/image/img{message.message_id}.jpg'
    await message.photo[-1].download(destination_file=filename)
    photo_with_face = find_face(filename)
    await message.answer(photo_with_face)


@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message):
    """Обработчик текста"""
    await message.answer('Моя миссия не поддержка беседы, хорошего дня)')


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
