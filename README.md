## ClothesShop
  Clothes shop application

# Installing
1. Clone repository
  ```
  git init
  git clone {link to repository}
  ```
2.Create virtualenv
3.Install libraries
  ```
  pip install -r requirements.txt
  ```
4.To make emails work you have to configure email backend in ecommerce/settings.py (its on the bottom of a file)
5.Enjoy

# REMEMBER TO CONFIGURE EMAIL BACKED IN SETTINGS.PY
1. Just type data in blindspots also in views in send_mail()
  ```
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_HOST_USER = ''
  EMAIL_HOST_PASSWORD = ''
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  DEFAULT_FROM_EMAIL = '' 
  ```
