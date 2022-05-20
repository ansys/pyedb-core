from dotenv import dotenv_values, find_dotenv

configs = dotenv_values(find_dotenv(".env.test"))
