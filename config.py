SECRET_KEY = 'abcdefg23213conovo'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Flask-Mail
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your_gmail'
MAIL_PASSWORD = 'your_gmail_password'
