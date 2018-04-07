import os

if "API_TOKEN_MOZART" not in os.environ or "GROUP_CHAT_ID_COTTAGE" not in os.environ:
    raise AssertionError("Please configure TELEBOT_BOT_TOKEN and GROUP_CHAT_ID as environment variables")

API_TOKEN = os.environ['API_TOKEN_MOZART']
GROUP_CHAT_ID = int(os.environ['GROUP_CHAT_ID_COTTAGE'])
NAME = 'Peregonivka_bot'
CHANNEL_NAME = '@Butenko_test'

WEBHOOK_HOST = 'butenko.asuscomm.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = '/var/www/web/telegram_bot/certificate.crt'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/var/www/web/telegram_bot/private.key'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


text_messages = {
    'welcome':
        u'Please welcome {name}!\n\n'
        u'This chat is intended for questions about and discussion of the pyTelegramBotAPI.\n'
        u'To enable group members to answer your questions fast and accurately, please make sure to study the '
        u'project\'s documentation (https://github.com/eternnoir/pyTelegramBotAPI/blob/master/README.md) and the '
        u'examples (https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples) first.\n\n'
        u'I hope you enjoy your stay here!',

    'info':
        u'My name is TeleBot,\n'
        u'I am a bot that assists these wonderful bot-creating people of this bot library group chat.\n'
        u'Also, I am still under development. Please improve my functionality by making a pull request! '
        u'Suggestions are also welcome, just drop them in this group chat!',

    'wrong_chat':
        u'Hi there!\nThanks for trying me out. However, this bot can only be used in the pyTelegramAPI group chat.\n'
        u'Join us!\n\n'
        u'https://telegram.me/joinchat/067e22c60035523fda8f6025ee87e30b'
}