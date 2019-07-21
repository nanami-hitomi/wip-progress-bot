import database

def estimate_time(Chapter):
    raise Exception("Not implemented")
        


def __get_manga_id_from_nickname(manga_nickname):
    return database.get_manga_id(manga_nickname)

def __guarantee_manga_id(manga_id_or_nickname):
    try:
        return int(manga_id_or_nickname)
    except:
        return database.get_manga_id(manga_id_or_nickname)

def get_manga(manga_id):
    return database.get_manga()

def get_chapter_or_latest(manga_id,chapter_number=-1):
    manga_id = __guarantee_manga_id(manga_id)
    if chapter_number==-1:
        chapter_number=database.get_latest_chapter(manga_id)
    return database.get_chapter(manga_id,chapter_number)

def get_progress(Chapter):
    raise Exception("Not implemented")


def manga_set_property(Manga,property_name,new_value):
    raise Exception("Not implemented")

def chapter_set_property(Chapter,property_name,new_value):
    raise Exception("Not implemented")

def get_help(command=""):
    if command=="":
        return open('resources/help.txt').read()
    else:
        #TODO: make a help_{command}.txt for each command and use those here
        if command in ["progress", "manga", "chapter", "edit", "estimate", "help"]:
            return "Help for %s"%command
        else:
            return "Not so fast!"