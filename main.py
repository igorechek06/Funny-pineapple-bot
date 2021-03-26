import config
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import executor
import optparse


parser = optparse.OptionParser(conflict_handler="resolve")
parser.add_option('-t', '--test',
                  action="store_true",
                  dest='test',
                  help='test token')
parser.add_option('-m', '--main',
                  action="store_true",
                  dest='main',
                  help='main token')
values, args = parser.parse_args()

if values.test:
    config.token = config.token_test
elif values.main:
    config.token = config.token_main
else:
    raise ValueError("Argument please (-t or -m)")

if True:
    from bot import dp
    import src
    from objects import MessageData


async def on_shutdown(dp: Dispatcher):
    await MessageData.del_all()


async def on_startup(dp: Dispatcher):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
