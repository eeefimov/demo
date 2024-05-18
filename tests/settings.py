"""User credentials setting"""
import os
from dotenv import load_dotenv

load_dotenv()
user_login = os.getenv("auth_login")
user_pass = os.getenv("auth_pass")
user_email = os.getenv("auth_email")

gmail_password_registered = os.getenv("pwd_registered")
gmail_user_registered = os.getenv("usr_registered")
gmail_password_not_registered = os.getenv("pwd_not_registered")
gmail_user_not_registered = os.getenv("usr_not_registered")
#
# # api
# valid_email_api = os.getenv("valid_email")
# valid_name_api = os.getenv("valid_name")
# valid_pwd_api = os.getenv("valid_pwd")
# accessToken_api = os.getenv("accessToken")
# refreshToken_api = os.getenv("refreshToken")
