from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON

router = Router()

@router.message()
async def send_other_text(message: Message):
    await message.answer(text=LEXICON['other_text'])