# AUTO WAGE BACKEND Setup
To fully run the application you're required to open three terminal tab
1. For redis-server
2. For celery-api for redis
3. Application server
4. And postgres database

## Configurations
```bash
pip install -r requirements.txt
export PAYSTACK_API =$YOUR_API
export MAIL_USER=$YOUR_MAIL_USER
export DATABASE_NAME=$DATABASE_NAME
export DATABASE_HOST=$DATABASE_HOST
export DATABASE_USER=$DATABASE_USER
export DABASE_PORT=$DATABASE_PORT
export DATABASE_PASSWORD=$DATABASE_PASSWORD

```
To create a user for the application
run the following command
```bash
python manage.py createsuperuser --username $username --email $email
```
*Linux and Windows Subsytem Linux*
```bash
sudo apt-get install redis-server
```
*Mac Os*
```zsh
brew install redis-server
```
## Run program
1. redis-server
```bash 
redis-server
```
2. celery api for python in another terminal
```bash
python -m celery -A auto_wage_schedule worker --beat --scheduler django -l info
```
3. Application server
```bash
python manage.py runserver
```