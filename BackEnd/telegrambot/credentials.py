from BackEnd.settings import WEBSITE_URL
TOKEN = '6800635126:AAGV8Ev4Wf4qsq4lPa-Vm-dcYNsoQ19h1So'
# NGROK = 'https://0aa0-37-156-152-117.ngrok-free.app' 
# URL = f'{NGROK}/getpost/' 
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'
WEB_HOOK_URL = f'{TELEGRAM_API_URL}/setWebhook?url={WEBSITE_URL}/telegrambot/getpost/'

#  https://api.telegram.org/bot6800635126:AAGV8Ev4Wf4qsq4lPa-Vm-dcYNsoQ19h1So/setWebhook?url=https://33e3-37-156-157-110.ngrok-free.app
# https://api.telegram.org/bot6800635126:AAGV8Ev4Wf4qsq4lPa-Vm-dcYNsoQ19h1So/setWebhook?url=https://0aa0-37-156-152-117.ngrok-free.app/telegrambot/getpost/
# ///////////