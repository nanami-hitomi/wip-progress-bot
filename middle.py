import database

def estimate_time(Chapter):
    raise Exception("Not implemented")

def __guarantee_manga_id(manga_id_or_nickname):
    try:
        return database.get_manga_id(manga_id_or_nickname)
    except:
        return int(manga_id_or_nickname)

def get_manga(manga_id):
    try:
        manga_id = __guarantee_manga_id(manga_id)
        return database.get_manga(manga_id)
    except:
        return None

def get_chapter_or_latest(manga_id,chapter_number=-1):
    try:
        manga_id = __guarantee_manga_id(manga_id)
        if chapter_number==-1:
            chapter_number=database.get_latest_chapter(manga_id)
        return database.get_chapter(manga_id,chapter_number)
    except:
        return None

def get_progress(Chapter):
    if Chapter is None:
        return {}
    return {
        "Translator":Chapter.translator,
        "Translation Complete": Chapter.translation_complete,
        "Proofreader": Chapter.proofreader,
        "Proofread Complete": Chapter.proofread_complete,
        "Redrawer": Chapter.redrawer,
        "Redraw Complete": Chapter.redraw_complete,
        "Typesetter": Chapter.typesetter,
        "Typeset complete": Chapter.typeset_complete,
        "QC": Chapter.qc,
        "QC Complete": Chapter.qc_complete
    }


def manga_set_property(Manga,property_name,new_value):
    raise Exception("Not implemented")

def chapter_set_property(Chapter,property_name,new_value):
    raise Exception("Not implemented")

def new_manga(Manga):
    try:
        database.create_manga(Manga)
        return "Created successfully"
    except:
        return "Failed to create: Does this manga already exist?"

def new_chapter(Manga,chapter_number):
    try:
        database.create_chapter(Manga,int(chapter_number))
        return "Created Successfully"
    except ValueError:
        return "Chapter number needs to be of type int"
    except:
        return "Failed to create: Does this chapter already exist?"

def new_chapter_o(Chapter):
    try:
        database.create_chapter_o(Chapter)
        return "Created successfully"
    except: 
        return "Failed to create: Does this chapter already exist?"

def get_help(command=""):
    if command=="":
        return open('resources/help.txt').read()
    else:
        #TODO: make a help_{command}.txt for each command and use those here
        if command in ["progress", "manga", "chapter", "edit", "estimate", "help"]:
            return "Help for %s"%command
        else:
            return "Not so fast!"
