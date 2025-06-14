EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your_email@example.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

WHATSAPP_API_URL = 'https://graph.facebook.com/v22.0/682992084897059/messages'
WHATSAPP_TOKEN = 'EAAKOL3EH9QgBO2vH1eK1flf2Ht31STP62geoP5h4WDC36D49cHeFXxMUKZBtQOfH0SvhcwuAMZCRejZAWEUAEwBGgJjKO9zNQZBDQlZAQB41yYcYbQqoUNjIMZCmLerTZCjZBMp5BbRsbrZB9m6ecavOqfNCimOSEPSj7p6flDOqFIgMvTzuqF16NyyPEBdbKcln67vtpa1IrTbRvmleiErRooveeIG5nd3OQXX60cAZDZD'
WHATSAPP_PHONE_NUMBER_ID = '682992084897059'  # Your WhatsApp phone number ID
