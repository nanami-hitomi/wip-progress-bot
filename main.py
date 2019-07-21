import database
import atexit

#setup database initialization and add de-initialization to be completed on exit
database.initialize()
atexit.register(database.deinitialize)

#add more here