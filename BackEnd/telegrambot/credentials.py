TOKEN = '6800635126:AAGV8Ev4Wf4qsq4lPa-Vm-dcYNsoQ19h1So'
NGROK = 'https://a882-37-44-62-110.ngrok-free.app' 
URL = f'{NGROK}/getpost/' 
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'
WEB_HOOK_URL = f'{TELEGRAM_API_URL}/setWebhook?url={NGROK}/telegrambot/getpost/'

#  https://api.telegram.org/bot6800635126:AAGV8Ev4Wf4qsq4lPa-Vm-dcYNsoQ19h1So/setWebhook?url=https://33e3-37-156-157-110.ngrok-free.app
# https://api.telegram.org/bot6800635126:AAGV8Ev4Wf4qsq4lPa-Vm-dcYNsoQ19h1So/setWebhook?url=https://a882-37-44-62-110.ngrok-free.app/telegrambot/getpost/