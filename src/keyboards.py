from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_settings = InlineKeyboardButton('Настройки', callback_data='settings_keyboard') 
menu = InlineKeyboardMarkup(row_width=1).add(btn_settings)


btn_city = InlineKeyboardButton('Установить город', callback_data='settings_set_city')
btn_type = InlineKeyboardButton('Установить тип поисков', callback_data='settings_set_search_type')
btn_done = InlineKeyboardButton('Готово', callback_data='settings_done')
settings = InlineKeyboardMarkup(row_width=3).add(btn_city, btn_type, btn_done)


btn_msk = InlineKeyboardButton('Москва', callback_data='settings_select_msk') 
menu = InlineKeyboardMarkup(row_width=1).add(btn_msk)