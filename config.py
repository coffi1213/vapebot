import os 
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
MANAGER_CONTACT = os.getenv("MANAGER_CONTACT")

# Yandex Object Storage
YANDEX_BUCKET = os.getenv("YANDEX_BUCKET")
YANDEX_ACCESS_KEY = os.getenv("YANDEX_ACCESS_KEY")
YANDEX_SECRET_KEY = os.getenv("YANDEX_SECRET_KEY")
YANDEX_ENDPOINT = os.getenv("YANDEX_ENDPOINT")

DATABASE_PATH = "data/database.db"
BACKUP_DIR = "backups/"

# Реферальная ссылка
def get_ref_link(user_id: int) -> str:
    return f"https://t.me/vappeebot?start={user_id}"