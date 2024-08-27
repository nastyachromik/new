from dataclasses import dataclass
from environs import Env

@dataclass
class Tg_bot:
    token: str
    admin_id: int


@dataclass
class Book:
    current_page: int
    dict_pages: dict[int, str]
    marked_pages: list[int]

@dataclass
class Config:
    tg_bot: Tg_bot

def load_config(path:  str = None) -> Config:
    env = Env()
    env.read_env()
    return Config(tg_bot=Tg_bot(token=env('BOT_TOKEN'), admin_id=env('ADMIN_ID')))
