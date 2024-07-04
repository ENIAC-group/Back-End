from django.urls import path
from . import views


urlpatterns = [
  path('getpost/', views.telegram_bot, name='telegram_bot'),
  path('setwebhook/', views.SetWebhookView.as_view({'get' : 'set_webhook'}), name='setwebhook'),
]

# telegrambot/setwebhook/