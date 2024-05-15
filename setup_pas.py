import os
from secrets import token_hex

import dotenv
from cryptography.fernet import Fernet

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

os.environ["PASSWORD_KEY"] = Fernet.generate_key().decode()
os.environ["SECRET_KEY"] = token_hex(16)

dotenv.set_key(dotenv_file, "PASSWORD_KEY", os.environ["PASSWORD_KEY"])
dotenv.set_key(dotenv_file, "SECRET_KEY", os.environ["SECRET_KEY"])

print("Success")