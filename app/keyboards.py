from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Որոնել որպես հյուր")],
                                     [KeyboardButton(text="Գրանցվել")]
                                     ],
                            resize_keyboard=True,
                            input_field_placeholder="Ընտրեք գործողությունը")
