from telebot import types

def panel_Keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="Help", callback_data="panel_help")
    itembtn2 = types.InlineKeyboardButton(text="Keys", callback_data="panel_keys")
    itembtn3 = types.InlineKeyboardButton(text="Statistics", callback_data="panel_statistics")
    itembtn4 = types.InlineKeyboardButton(text="Settings", callback_data="panel_settings")
    inline_keyboard.add(itembtn1, itembtn2, itembtn3, itembtn4)
    return inline_keyboard

def pay_Keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="1 key", callback_data="pay_request_1")
    itembtn2 = types.InlineKeyboardButton(text="5 keys", callback_data="pay_request_5")
    itembtn3 = types.InlineKeyboardButton(text="15 keys", callback_data="pay_request_15")
    inline_keyboard.add(itembtn1, itembtn2, itembtn3)
    return inline_keyboard

def vocab_Keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="Add a vocabulary list", callback_data="vocab_add")
    itembtn2 = types.InlineKeyboardButton(text="View a vocabulary list", callback_data="vocab_view")
    itembtn3 = types.InlineKeyboardButton(text="Delete a vocabulary list", callback_data="vocab_delete")
    inline_keyboard.add(itembtn1, itembtn2, itembtn3)
    return inline_keyboard

def zoom_Keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="Add a Zoom link", callback_data="zoom_add")
    itembtn2 = types.InlineKeyboardButton(text="View a Zoom link", callback_data="zoom_view")
    itembtn3 = types.InlineKeyboardButton(text="Delete a Zoom link", callback_data="zoom_delete")
    inline_keyboard.add(itembtn1, itembtn2, itembtn3)
    return inline_keyboard
