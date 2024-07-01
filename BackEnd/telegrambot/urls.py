from django.urls import path
from . import views


urlpatterns = [
  path('getpost/', views.telegram_bot, name='telegram_bot'),
  path('setwebhook/', views.SetWebhookView.as_view({'get' : 'get'}), name='setwebhook'),
]

# telegrambot/setwebhook/