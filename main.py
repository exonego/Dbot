from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import BaseFilter, Command, CommandStart
import re

# import BOT_TOKEN variable from created by you file 'bot_token.py' in root project folder
from bot_token import BOT_TOKEN


# create bot and dispatcher objects
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# filter that checks the correctness of a complete quadratic equation
class IsQuadratic(BaseFilter):
    def __init__(self) -> None:
        self.template = r"-?\d+[a-z]\^2[+-]\d+[a-z][+-]\d+=0"

    async def __call__(self, message: Message) -> bool:
        if re.fullmatch(self.template, message.text):

            # list of equation variables
            letters: list[str] = list()

            for i in message.text:
                if i.isalpha():
                    letters.append(i)
            if letters[0] == letters[1]:
                return {"variable": letters[0]}
        return False


# filter that responds to the "/start" command
@dp.message(CommandStart())
async def answer_command_start(message: Message):
    await message.answer(
        f"""Привет, {message.from_user.username}!
                         Я бот, умеющий решать полные квадратные уравнения с помощью дискриминанта.
                         Пожалуйста используйте такой шаблон для отправки уравнения:
                            ax^2+bx+c=0"""
    )


# filter responding to a regular quadratic equation
@dp.message(IsQuadratic())
async def answer_if_correct_equation(message: Message, variable: str):
    nums: list[int] = [i for i in message.text.split(variable)]
    a = int(nums[0])
    b = int(nums[1][2:])
    c = int(nums[2][:-2])

    discriminant = b**2 - (4 * a * c)
    if discriminant < 0:
        await message.reply("Корней нет")
    else:
        roots = sorted(
            [
                (-1 * b + discriminant**0.5) / (2 * a),
                (-1 * b - discriminant**0.5) / (2 * a),
            ]
        )
        await message.reply(f"{variable}1 = {roots[0]}\n{variable}2 = {roots[1]}")


if __name__ == "__main__":
    dp.run_polling(bot)
