"""User credentials setting"""
import os
from dotenv import load_dotenv

load_dotenv()
user_login = os.getenv("AUTH_LOGIN")
user_pass = os.getenv("AUTH_PASS")
user_email = os.getenv("AUTH_EMAIL")

gmail_password_registered = os.getenv("PWD_REGISTERED")
gmail_user_registered = os.getenv("USR_REGISTERED")
gmail_password_not_registered = os.getenv("PWD_NOT_REGISTERED")
gmail_user_not_registered = os.getenv("USR_NOT_REGISTERED")
