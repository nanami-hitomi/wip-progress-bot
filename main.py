import database
import bot
import atexit

#setup database initialization and add de-initialization to be completed on exit
database.initialize()
atexit.register(database.deinitialize)

#Start the bot
token = open('token.txt').read()
bot.bot.run(token)