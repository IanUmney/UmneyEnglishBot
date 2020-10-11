from telebot.types import LabeledPrice
from utils import timestamp, vault
import json, TOKENS

provider_token =  TOKENS._PAYMENT_TOKEN_# @BotFather -> Bot Settings -> Payments
subscriptions = {
1:{
    "price":[LabeledPrice(label='Individual group', amount=8500)],
    "description":"\n1 license key to use in 1 group.\n\nPremium Benefits:\n + Zoom Integration\n + Custom Vocabulary Lists\n + 500 dictionary searches"
    },
5:{
    "price":[LabeledPrice(label='Solo teacher', amount=30000)],
    "description":"\n5 licence keys to use in 5 groups.\n\nPremium Benefits:\n + Zoom Integration\n + Custom Vocabulary Lists\n + 500 dictionary searches",
    },
15:{
    "price":[LabeledPrice(label='Small team', amount=110000)],
    "description":"\n15 license keys to use in 15 groups.\n\nPremium Benefits:\n + Zoom Integration\n + Custom Vocabulary Lists\n + 500 dictionary searches",
    }
}

def payment(bot, message, number_of_groups, edit_message_id):
    # bot.send_invoice(message.chat.id, title=f'{number_of_groups} key',
    #                  description=f"{subscriptions[number_of_groups]['description']}",
    #                  provider_token=provider_token,
    #                  currency='uah',
    #                  photo_height=0,  # !=0/None or picture won't be shown
    #                  photo_width=0  ,
    #                  photo_size=0 ,
    #                  is_flexible=False,  # True If you need to set up Shipping Fee
    #                  prices=subscriptions[number_of_groups]["price"],
    #                  start_parameter='UmneyEnglish_payment',
    #                  invoice_payload=f"{number_of_groups}")
    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_message_id, text='Send the full payment to one of the following accounts:\n\n<b>MonoBank:</b>\n<i>5375414116727354\nмоно банк Умнеи Неля</i>\n\n<b>PrivatBank</b>\n<i>5168742239805835\nприватбанк Умнеи Н</i>\n\nKeys are used to upgrade your Telegram groups to the premium tier.\n\n<u>Payments through Telegram will be supported soon.</u>', parse_mode='HTML')
    bot.send_message(message.chat.id, 'When you have paid, send @ianumney a screenshot of your payment. You will receive your keys ASAP')

def payment_success(message):
    time_stamp = timestamp.get_time_stamp()
    teacher_keys = vault.create_license_key(subscriptions[message.json['successful_payment']['invoice_payload']]["teachers"])
    dictionary_allowance = subscriptions[message.json['successful_payment']['invoice_payload']]["searches"]
    date_online = timestamp.online()

    data = vault.get_data()
    data["admin"]["payments"] = {
    "telegram_data":{
        "admin_fist_name":message.json['from']['first_name'],
        "admin_telegram_id": message.json['from']['id'],
        "telegram_chat_type":message.json['chat']['type']
        },
    "stripe_payment_data":{
        "stripe_payment_charge_id": message.json['successful_payment']['provider_payment_charge_id'],
        "total_mount": message.json['successful_payment']['total_amount'],
        "Invoice payload": message.json['successful_payment']['invoice_payload']
        },
    "bot_data":{
        "teacher_allowance":teacher_allowance,
        "teachers":None,
        "teacher_keys":teacher_keys,
        "channels":None,
        "dictionary_allowance":dictionary_allowance,
        "dictionary_usage":None,
        "date_online":date_online
        }
    }
    vault.dump_data(data)
