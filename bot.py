from dotenv import load_dotenv
import os
from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

API_TOKEN = GCP_PROJECT_ID = os.getenv('API_TOKEN')

tag_targets = ['@Madsora', '@marianenko', '@yklymk', '@leakerman', '@bodichelly', ]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

EMOJI_RANGES_UNICODE = [
    ('\U0001F300', '\U0001F579'),
    ('\U0001F57B', '\U0001F5A3'),
    ('\U0001F5A5', '\U0001F5FF')
]


def random_emoji():
    emoji_ranges = EMOJI_RANGES_UNICODE

    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))

    point = randrange(weight_distr[-1])

    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = emoji_ranges[emoji_range_idx]

    point_in_range = point
    if emoji_range_idx != 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    emoji = chr(ord(emoji_range[0]) + point_in_range)
    emoji_name = unicode_name(emoji).capitalize()
    emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())
    return emoji


@dp.message_handler(commands=['lection'])
async def send_welcome(message: types.Message):
    tagged_users = []
    for username in tag_targets:
        if username != message.from_user.username:
            tagged_users.append(f'{username} {random_emoji()}\n')
    await message.reply("Внеманіє для:\n" + ''.join(tagged_users))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
