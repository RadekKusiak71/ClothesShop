
## ClothesShop - Clothes shop application

### Used technologies
  1. Django
  2. Python
  3. Bootstrap
  4. HTML
  5. CSS

### Installing

1. Clone the repository:
   ```shell
   git init
   git clone {link to repository}
   ```

2. Create a virtual environment:
   ```shell
   virtualenv env
   source env/bin/activate
   ```

3. Install the required libraries:
   ```shell
   pip install -r requirements.txt
   ```

4. Configure email backend in `ecommerce/settings.py` (at the bottom of the file):
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_HOST_USER = ''
   EMAIL_HOST_PASSWORD = ''
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   DEFAULT_FROM_EMAIL = ''
   ```

5. ADMIN USER credentials for the admin panel:
   - Username: admin
   - Password: 123

6. TEST USER credentials for testing purposes:
   - Username: TestUser
   - Password: !@#$%^&*

**Note:** Make sure to fill in the required information for the email settings and update the credentials accordingly.

Now, your ClothesShop application is ready to use!
