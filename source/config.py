MONGODB_URI = 'mongodb+srv://walletwatchr:walletwatchrpassword@cluster0.ehtddne.mongodb.net/'
BOT_TOKEN = '6502984988:AAEE65Mor8XNvxhb3irkxtR8WqDHcbdinL8'
HELIUS_KEY = '9e17b24d-b88d-41e2-86e1-0bb6bf5b8095'
HELIUS_WEBHOOK_URL = 'https://walletwatchr-cacf9141608c.herokuapp.com/wallet'
HELIUS_WEBHOOK_ID = '5d8cadd0-ce36-4cb9-8cbc-6dc3d21705f'

import os

MONGODB_URI = os.environ.get('MONGODB_URI')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
HELIUS_KEY = os.environ.get('HELIUS_KEY')
HELIUS_WEBHOOK_URL = os.environ.get('HELIUS_WEBHOOK_URL')
HELIUS_WEBHOOK_ID = os.environ.get('HELIUS_WEBHOOK_ID')