from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
DATABASE_URL = env.str("DATABASE_URL")
TIME_BETWEEN_NOTIFICATION_UPDATES = env.int("TIME_BETWEEN_NOTIFICATION_UPDATES", 60 * 60 * 24)

TIMEZONE = env.str("TIMEZONE", "Europe/Moscow")
