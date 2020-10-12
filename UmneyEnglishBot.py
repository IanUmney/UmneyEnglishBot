
from utils import timestamp, vault, keyboards, gate_keeper, spell_check
from commands import oxford, urbandictionary, zoom, vocab, synonyms
from commands.onboarding import payment
import telebot, os, json, TOKENS
from commands.admin import admin
from telebot import types


token = TOKENS._TELEGRAM_TOKEN_
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['test'])
def command_test(message):
    print(bot.get_me().id)

def check_channel_is_registered(message):
    data = vault.get_data()
    if not str(message.chat.id) in data['channels']:
        gate_keeper.add_channel(message, timestamp.online(), bot.get_chat_members_count(message.chat.id))

@bot.message_handler(content_types=['new_chat_members'])
def new_member_added(message):
    '''There is a new member added to the group.
    If the bot is joined to a group, that group is added to the data.json.
    The group is then only basic tier until they use a key'''
    check_channel_is_registered(message)
    print(message.text)
    if str(message.json["new_chat_member"]["id"]) == str(bot.get_me().id):
        gate_keeper.add_channel(message, timestamp.online(), bot.get_chat_members_count(message.chat.id))
    command_start(message)

@bot.message_handler(content_types=['left_chat_member'])
def member_left(message):
    '''Someone left the chat.
    If the bot has been removed from a group then that group's data is deleted'''
    check_channel_is_registered(message)
    print(message.text)
    if str(message.json["left_chat_member"]["id"]) == str(bot.get_me().id):
        gate_keeper.remove_channel(message.chat.id)


@bot.message_handler(commands=['help'])
def command_help(message):
    check_channel_is_registered(message)
    print(message.text)
    bot.send_message(message.chat.id, '''<b>UmneyEnglish</b> Telegram bot help.

Here is a list of the commands:

🔸 <b>/dice</b>
Roll a die for a random number

🔸 <b>/zoom</b>
You can view, add, and delete Zoom meetings for your groups.
<b>/zoom</b> <i>- View existing Zoom links </i>
<b>/zoom add [teacher name] [Zoom link]</b>
<b>/zoom delete [teacher name]</b>

🔸 <b>/vocab</b>
You can save and view vocabulary lists.
<b>/vocab</b> - View all vocabulary lists.
<b>/vocab [topic]</b> View a specific list.
<b>/vocab [add] [topic] [words]</b> - Add a list. <i>/vocab add shopping discount sale bargain clothes</i>
<b>/vocab delete [topic]</b> - Delete a specific topic.

🔸 <b>/synonym</b>
Search for synonyms of words.
<b>/synonym [word]</b>
<b>/syn [word]</b>

🔸 <b>/urban</b>
You can define words and phrases with the Online Urban dictionary.
<b>/urban [word/phrase]</b>

🔸 <b>/define</b>
You can define words and phrases with the Oxford English Dictionary.
<b>/define [word/phrase]</b>

🔸 <b>/price</b>
View prices of premium keys and purchase one.

🔸 <b>/upgrade</b>
Upgrade a class group with a premium key for more features.''',parse_mode='HTML')


@bot.message_handler(commands=['start'])
def command_start(message):
    print(message.text)
    try:
        gate_keeper.add_channel(message, timestamp.online(), bot.get_chat_members_count(message.chat.id))
    except Exception as e:
        print(message, e)

    bot.send_message(message.chat.id, """<b>Learn English. The clever way! 👨🏼‍🎓</b>

Using the <i><b>UmneyEnglish</b></i> chatbot in Telegram you can:

✅ Search the Oxford English Dictionary

✅ Search for slang definitions

✅ Search for synonyms of words

<b>You cannot:</b>

❌ Learn how to bake an award-winning chocolate cake

Use /help for help with the commands.

<b>Getting Started</b>
You can join the bot to any group by simply adding a member, searching for <i>@Umney_English_Bot</i>, and inviting it.

Use /price to see the prices for premium keys
<i>Premium groups can access /vocab, /synonyms, and /zoom commands.
They can also search the OED 250 times per month.</i>

""", parse_mode="HTML")

@bot.message_handler(commands=['dice'])
def command_dice(message):
    check_channel_is_registered(message)
    print(message.text)
    bot.send_dice(message.chat.id, emoji='🎲', disable_notification=True)

@bot.message_handler(commands=['zoom'])
def command_zoom(message=None, reply=None, edit_message_id=None):
    '''Handles the /zoom commands and requests the appropriate action from the zoom.py module.
    '''
    check_channel_is_registered(message)
    print(message.text)
    data = vault.get_data()
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)

    if not data['channels'][chat_id]['premium']:
        bot.send_message(chat_id, 'This is a premium feature only.\nUse /price to buy a premium key.')
        return

    # NOTE: use this when implementing next feature for /zoom
    # bot.send_message(chat_id, f'<b>Zoom</b>\n{zoom.get_group_links(chat_id)}', parse_mode='HTML', reply_markup=keyboards.zoom_Keyboard())


    def send_error_message():
        bot.send_message(chat_id, 'You have made a mistake. Use /help.')

    args = message.text.split(" ")[1:] # remove the command and just get the body of the message (args)
    if len(args) <=0:
        bot.send_message(chat_id, zoom.get_group_links(chat_id))
    elif len(args) <=1 :
        if args[0].lower() in data['channels'][chat_id]['zoom']:
            bot.send_message(chat_id, zoom.get_teacher_link(chat_id, args[0].lower()))
        else:
            send_error_message()
    elif len(args) <= 2:
        if args[0].lower() == 'delete':
            bot.send_message(chat_id, zoom.delete_link(chat_id, args[1].lower()))
        else:
            send_error_message()
    elif len(args) <= 3:
        if args[0].lower() == 'add':
            bot.send_message(chat_id, zoom.add_link(chat_id, args[1].lower(), args[2]))
        else:
            send_error_message()

@bot.message_handler(commands=['stats', 'statistics'])
def command_stats(message):
    # NOTE: Can change this to change 'x search/searches' depending on the number
    chat_id = str(message.chat.id)
    data = vault.get_data()
    member_count = str(data['channels'][chat_id]['member_count'])
    oed_searches = str(data['channels'][chat_id]['oed_searches'])
    vocab_lists = str(len(data['channels'][chat_id]['vocabulary']))
    zoom_links = str(len(data['channels'][chat_id]['zoom']))
    if data['channels'][chat_id]['premium']:
        premium = 'Yes.'
    else:
        premium = 'No.'

    bot.send_message(chat_id, f'''<b>Statistics</b>
This group has {member_count} members.
You have {oed_searches} dictionary searches left for this month.
There are {vocab_lists} vocabulary lists.
There are {zoom_links} Zoom links.
Are you a premium member? {premium}''', parse_mode='HTML')

@bot.message_handler(commands=['vocab'])
def command_vocab(message):
    check_channel_is_registered(message)
    print(message.text)
    chat_id = str(message.chat.id)
    text = message.text
    data = vault.get_data()

    if not data['channels'][chat_id]['premium']:
        bot.send_message(chat_id, 'This is a premium feature only.\nUse /price to buy a premium key.')
        return
    # else:
    #     bot.send_message(chat_id, "Select from one of the options below", reply_markup=keyboards.vocab_Keyboard())


    try:
        split_text = text.split(" ", 1)[1].split(" ")
    except Exception as e:
        print(message, e)
        bot.send_message(chat_id, vocab.list_all(chat_id), parse_mode='HTML')
    else:
        if len(split_text) <= 1:
            if split_text[0] == 'add':
                bot.send_message(chat_id, 'You must give the name and word of the list to add.\n/vocab add shopping discount sale bargain ')
            elif split_text[0] == 'delete':
                bot.send_message(chat_id, 'You must give the name of the list to delete.\n/vocab delete shopping')
            elif split_text[0] in data['channels'][chat_id]['vocabulary']:
                bot.send_message(chat_id, vocab.list_individual(chat_id, split_text[0]), parse_mode='HTML')
        elif len(split_text) >=2:
            if split_text[0] == 'delete':
                list_name = split_text[1]
                bot.send_message(chat_id, vocab.delete_list(chat_id, list_name))
            elif split_text[0] == 'add':
                topic = split_text[1]
                words = split_text[2:]
                bot.send_message(chat_id, vocab.add_list(chat_id, topic, words))
            elif split_text[0] in data['channels'][chat_id]['vocabulary']:
                try:
                    words = split_text[1:]
                    bot.send_message(chat_id, vocab.add_list(chat_id, split_text[0], words))
                except Exception as e:
                    print(message, e)
                    bot.send_message(chat_id, 'An error occured. Please try again later.')

@bot.message_handler(commands=['synonyms', 'syn', 'syns','synonym'])
def command_synonyms(message):
    check_channel_is_registered(message)

    if not data['channels'][chat_id]['premium']:
        bot.send_message(chat_id, 'This is a premium feature only.\nUse /price to buy a premium key.')
        return

    chat_id = str(message.chat.id)
    def get_word(message):
        try:
            word = message.text.split(" ",1)[1]
        except Exception as e:
            print(message, e)
            bot.send_message(chat_id, "You must give a word or phrase to define")
        else:
            corrected_word = spell_check.correct_spelling(word)
            if corrected_word != word:
                bot.send_message(chat_id, f'"{word}" is not spelled correctly.\nI am searching for the synonyms of {corrected_word} instead.')
            return corrected_word

    word_to_syn = get_word(message)

    bot.send_message(chat_id, synonyms.get_synonyms(word_to_syn), parse_mode='HTML')

@bot.message_handler(commands=['urban'])
def command_urban(message):
    check_channel_is_registered(message)
    print(message.text)
    bot.reply_to(message, urbandictionary.getDefinition(message))

@bot.message_handler(commands=['key', 'keys'])
def command_keys(message):
    check_channel_is_registered(message)
    print(message.text)
    user_id = str(message.from_user.id)
    data = vault.get_data()
    if len(data["admin"]["payments"]) >=1:
        for buyers in data["admin"]["payments"]:
            if user_id in buyers:
                if buyers[user_id]["keys"] >=1:
                    buyers[user_id]["keys"] -= 1
                    vault.dump_data(data)
                    bot.reply_to(message, vault.create_license_key())
                else:
                    bot.send_message(message.chat.id,"You have no more keys left.\n\nUse /pay to get more.")
            else:
                bot.send_message(message.chat.id,"You have not purchased any keys.")
    else:
        bot.send_message(message.chat.id, "You have not purchased any keys.")

@bot.message_handler(commands=['define'])
def command_define(message):
    check_channel_is_registered(message)
    print(message.text)
    chat_id = str(message.chat.id)
    bot.send_chat_action(chat_id, action='typing')

    def get_word(message):
        try:
            word = message.text.split(" ",1)[1]
        except Exception as e:
            print(message, e)
            bot.send_message(chat_id, "You must give a word or phrase to define")
        else:
            corrected_word = spell_check.correct_spelling(word)
            if corrected_word != word:
                bot.send_message(chat_id, f'"{word}" is not spelled correctly.\nI am searching for the definition of {corrected_word} instead.')
            return corrected_word

    word_to_define = get_word(message)

    def check_oed_searches(chat_id):
        data = vault.get_data()
        if data['channels'][chat_id]['oed_searches'] >= 1:
            return True
        if data['channels'][chat_id]['oed_searches'] == 0:
            bot.send_message(chat_id, f"You don't have any more dictionary searches remaining", parse_mode="HTML")
            return False

    def update_data(chat_id):
        data = vault.get_data()
        data['channels'][chat_id]['oed_searches'] -=1
        data['admin']['stats']['oed_searches'] += 1
        if data['channels'][chat_id]['oed_searches'] <=10:
            bot.send_message(chat_id, f"You have {data['channels'][chat_id]['oed_searches']} dictionary definitions remaining")
        vault.dump_data(data)

    # Checks if the sender's chat_id has enough remaining OED searches
    if check_oed_searches(chat_id):
        try:
            definition = oxford.define(word_to_define)
        except Exception as e:
            print(message, e)
            # bot.send_message(chat_id, f'I couldn\t find a definition for {word_to_define}.')
        else:
            bot.send_message(chat_id, definition, parse_mode='HTML')
            update_data(chat_id)

#Admin commands for bot owner
@bot.message_handler(commands=['admin'])
def command_admin(message):
    check_channel_is_registered(message)
    print(message.text)
    if message.from_user.id == 741444566:
        try:
            command = message.text.split(" ")[1]
            bot.send_message(message.chat.id,
            admin.secretary(command), parse_mode='HTML')
        except Exception as e:
            print(message, e)
            bot.send_message(message.chat.id,"You don\'t have the facilities for that, big man.")
    else:
        bot.send_message(message.chat.id,
        "🚫🖕🏽🖕🏽 Piss off 🖕🏽🖕🏽🚫")

@bot.message_handler(commands=['price', 'pay'])
def command_price(message):
    check_channel_is_registered(message)
    print(message.text)
    bot.send_message(message.chat.id,
    "How many license keys would you like to buy?\n\n1 key = 85 UAH\n5 keys = 300UAH\n15 keys = 1100UAH\n\nYou can use 1 license key per group", reply_markup=keyboards.pay_Keyboard())

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    check_channel_is_registered(message)
    print(message.text)
    hide_board = types.ReplyKeyboardRemove()

    invoice_id = message.json["successful_payment"]["provider_payment_charge_id"]
    print(message.json)

    data = vault.get_data()
    data["admin"]["payments"].append({message.from_user.id:{"date_time":timestamp.get_time_stamp(),"invoice_id":invoice_id,"number_of_keys_bought":int(message.json["successful_payment"]["invoice_payload"]),"keys":int(message.json["successful_payment"]["invoice_payload"])}})

    vault.dump_data(data)

    bot.send_message(message.chat.id, "Use the /key command to generate a key")

@bot.message_handler(commands=['upgrade'])
def got_payment(message):

    chat_id = str(message.chat.id)
    data = vault.get_data()
    check_channel_is_registered(message)
    if message.from_user.id == 741444566:
        data['channels'][chat_id]['premium'] = True
        vault.dump_data(data)
        bot.send_message(chat_id, 'This group is now upgraded.')
        return

    if message.chat.id == message.from_user.id:
        bot.send_message(chat_id, "❗️ You cannot upgrade our private chat ❗️")
        bot.send_message(chat_id, "Go to a group with your students and use the /upgrade command")
    elif data['channels'][chat_id]['premium']:
        bot.send_message(chat_id, "This group is already upgraded")
    else:
        try:
            key_used = str(message.text.split(" ")[1])
            msg = gate_keeper.upgrade_channel(chat_id, key_used)
        except Exception as e:
            print(message, e)
            bot.send_message(chat_id, "You need to give me a key.")
            bot.send_message(chat_id, "/upgrade [key]")
        else:
            bot.send_message(chat_id, msg)

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")

@bot.message_handler(func=lambda m: True)
def find_key_words(message):
    print(message.text)

#Callback handler for inline keyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    edit_message_id = call.message.json["message_id"] #This is the message the inline keyboard is linked to
    chat_id = call.message.json["chat"]["id"]
    user_id = call.message.from_user.id
    if call.data == 'zoom_add':
        command_zoom(reply=call.data, edit_message_id=edit_message_id)
    elif call.data == 'zoom_view':
        command_zoom(reply=call.data, edit_message_id=edit_message_id)
    elif call.data == 'zoom_delete':
        command_zoom(reply=call.data, edit_message_id=edit_message_id)



    '''The below code is for the panel/settings function'''
    # if call.data == "panel_help":
    #     bot.answer_callback_query(call.id, "panel_help") # remove this
    #     panel_screen(bot, panel_message, user_id)
    #     # bot.edit_message_text(message_id = panel_message, chat_id=chat_id, text="You want help?", reply_markup=keyboards.panel_Keyboard ())
    # elif call.data == "panel_keys":
    #     bot.answer_callback_query(call.id, "panel_keys")
    # elif call.data == "panel_statistics":
    #     bot.answer_callback_query(call.id, "panel_statistics")
    # elif call.data == "panel_settings":
    #     bot.answer_callback_query(call.id, "panel_settings")



    '''The below code is for the payment function'''
    # if call.data == "pay_request_1":
    #     # if call.message.json["chat"]["type"] == "private":
    #     payment.payment(bot, call.message, 1, edit_message_id)
    #     # else:
    #     #     bot.answer_callback_query(call.id, "Cannot pay in public chat!")
    #     #     bot.send_message(call.message.chat.id, "You must be in a private chat with me to pay.")
    # elif call.data == "pay_request_5":
    #     # if call.message.json["chat"]["type"] == "private":
    #     payment.payment(bot, call.message, 5, edit_message_id)
    #     # else:
    #     #     bot.answer_callback_query(call.id, "Cannot pay in public chat!")
    #     #     bot.send_message(call.message.chat.id, "You must be in a private chat with me to pay.")
    # elif call.data == "pay_request_15":
    #     # if call.message.json["chat"]["type"] == "private":
    #     payment.payment(bot, call.message, 15, edit_message_id)
    #     # else:
    #     #     bot.answer_callback_query(call.id, "Cannot pay in public chat!")
    #     #     bot.send_message(call.message.chat.id, "You must be in a private chat with me to pay.")
    #
    # # if call.data == 'vocab_add':


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
