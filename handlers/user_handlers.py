from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, user_db
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards.bookmarks_kb import (create_edit_keyboard, create_bookmarks_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handing import book

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    user_db[message.from_user.id]['page'] = 1
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_keyboard('backward', f'{user_db[message.from_user.id]["page"]}/{len(book)}', 'forward'))

@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_keyboard('backward', f'{user_db[message.from_user.id]["page"]}/{len(book)}', 'forward'))

@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if user_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON[message.text], reply_markup=create_bookmarks_keyboard(*user_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

@router.callback_query(F.data == 'forward')
async def process_forward_command(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] < len(book):
        user_db[callback.from_user.id]['page'] += 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_keyboard('backward', f'{user_db[callback.from_user.id]["page"]}/{len(book)}', 'forward'))
    await callback.answer()

@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].add(user_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')

@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    user_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(text= text, reply_markup=create_pagination_keyboard('backward', f'{user_db[callback.from_user.id]["page"]}/{len(book)}', 'forward'))

@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON[callback.data], reply_markup=create_edit_keyboard(*user_db[callback.from_user.id]['bookmarks']))

@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])

@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmakrs'].remove(int(callback.data[:-3]))
    if user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['/bookmarks'], reply_markup=create_edit_keyboard(*user_db[callback.from_user.id]['bookmarks']))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
