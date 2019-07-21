import sqlite3

import manga as mn
import chapter as ch

#Configuration variables
__database_file = 'database.sqlite'
__tables_setup_script_file = 'tables.sql'

#Index variables for the results of __cursor.fetchone() or fetchall()
#The variables are named by the SQL field
#for the manga table
__manga_index_MangaID = 0
__manga_index_FullName = 1
__manga_index_Nickname = 2
__manga_index_Translator = 3
__manga_index_Proofreader = 4
__manga_index_Redrawer = 5
__manga_index_Typesetter = 6
__manga_index_QC = 7
__manga_index_Abandoned = 8
#for the chapters table
__chapter_index_ID = 0
__chapter_index_RelatedMangaID = 1
__chapter_index_ChapterNumber = 2
__chapter_index_Translator = 3
__chapter_index_Proofreader = 4
__chapter_index_Redrawer = 5
__chapter_index_Typesetter = 6
__chapter_index_QC = 7
__chapter_index_TranslationComplete = 8
__chapter_index_ProofreadComplete = 9
__chapter_index_RedrawComplete = 10
__chapter_index_TypesetComplete = 11
__chapter_index_QCComplete = 12
__chapter_index_Uploaded = 13

#Sqlite3 connection and cursor for the connection
__connection = None
__cursor = None
#Variables defining the state of the sqlite3 connection
__connection_open = False

#Sets up the database.
#This is called every time to guarantee the database is properly set up-
#`not exists` guarantees there aren't errors.
def __setup_database():
    setup_tables_query = open(__tables_setup_script_file).read()
    __cursor.executescript(setup_tables_query)
    __connection.commit()
    global __connection_open
    __connection_open = True

#Forces the connection to be open for any database changes
def __force_connection():
    if not __connection_open:
        initialize()


def __tuple_to_manga(tuple):
    #basic information
    manga = mn.Manga(tuple[__manga_index_MangaID], tuple[__manga_index_Nickname])
    manga = mn.Manga(tuple[__manga_index_MangaID], tuple[__manga_index_Nickname])
    manga.full_name = tuple[__manga_index_FullName]
    #fields for people working on it
    manga.translator = tuple[__manga_index_Translator]
    manga.proofreader = tuple[__manga_index_Proofreader]
    manga.redrawer = tuple[__manga_index_Redrawer]
    manga.typesetter = tuple[__manga_index_Typesetter]
    manga.qc = tuple[__manga_index_QC]
    #abandoned status
    manga.abandoned = tuple[__manga_index_Abandoned]
    return manga

def __manga_to_tuple(Manga):
    return (Manga.manga_id, Manga.full_name, Manga.nickname, Manga.translator,
            Manga.proofreader, Manga.redrawer, Manga.typesetter, Manga.qc,
            Manga.abandoned)

def __tuple_to_chapter(tuple):
    #"basic information"
    related_manga = get_manga(tuple[__chapter_index_RelatedMangaID])
    chapter = ch.Chapter(related_manga,tuple[__chapter_index_ChapterNumber])
    #people involved
    chapter.translator = tuple[__chapter_index_Translator]
    chapter.proofreader = tuple[__chapter_index_Proofreader]
    chapter.redrawer = tuple[__chapter_index_Redrawer]
    chapter.typesetter = tuple[__chapter_index_Typesetter]
    chapter.qc = tuple[__chapter_index_QC]
    #status of various stages
    chapter.translation_complete = tuple[__chapter_index_TranslationComplete]
    chapter.proofread_complete = tuple[__chapter_index_ProofreadComplete]
    chapter.redraw_complete = tuple[__chapter_index_RedrawComplete]
    chapter.typeset_complete = tuple[__chapter_index_TypesetComplete]
    chapter.qc_complete = tuple[__chapter_index_QCComplete]
    chapter.uploaded = tuple[__chapter_index_Uploaded]
    return chapter

# Warning- this is not the same type of tuple as returned by __cursor.fetchone()!
# This does NOT include the ID in the tuple (as that isn't needed for the insertion,
# unlike the manga)
def __chapter_to_tuple(Chapter):
    return (Chapter.related_manga_id, Chapter.chapter_number, Chapter.translator,
            Chapter.proofreader, Chapter.redrawer, Chapter.typesetter, Chapter.qc,
            Chapter.translation_complete, Chapter.proofread_complete,
            Chapter.redraw_complete, Chapter.typeset_complete, Chapter.qc_complete,
            Chapter.uploaded)

def initialize():
    #adapt bool to int
    global __connection
    __connection = sqlite3.connect(__database_file)
    global __cursor
    __cursor = __connection.cursor()
    __setup_database()

def deinitialize():
    global __connection_open
    if __connection_open:
        __cursor.close()
        #make sure to save all statements
        global __connection
        __connection.commit()
        __connection.close()
        __connection_open=False


def get_manga_id(nickname):
    __force_connection()
    __cursor.execute('select * from Manga where Nickname=? collate nocase', (nickname,))
    #only return the ID from the manga's list format
    return __cursor.fetchone()[__manga_index_MangaID]


def get_manga(manga_id):
    __force_connection()
    __cursor.execute('select * from Manga where MangaID=?',(manga_id,))
    #This is in a list format, whereas an object needs to be returned
    manga = __cursor.fetchone()
    return __tuple_to_manga(manga)

def get_chapter(manga_id, chapter_number):
    __force_connection()
    __cursor.execute('select * from Chapters where RelatedMangaID=? and ChapterNumber=?',
                    (manga_id,chapter_number))
    #this is the list format of the chapter
    chapter = __cursor.fetchone()
    return __tuple_to_chapter(chapter)

def get_latest_chapter(manga_id):
    __force_connection()
    __cursor.execute('select max(ChapterNumber) from Chapters Where RelatedMangaID=?',
                    (manga_id,))
    return __cursor.fetchone()[0]

def set_manga(manga_id,field_name,new_value):
    if not field_name in ["FullName", "Nickname", "Translator", "Proofreader",
                                "Redrawer", "Typesetter", "QC", "Abandoned"]:
        return
    __force_connection()
    __cursor.execute('update Manga set '+field_name+'=? where MangaID=?',
                    (new_value,manga_id))
    __connection.commit()

def set_chapter(manga_id,chapter_number,field_name,new_value):
    if not field_name in ["RelatedMangaID", "ChapterNumber", "Translator",
                            "Proofreader", "Redrawer", "Typesetter", "QC",
                            "TranslationComplete", "ProofreadComplete",
                            "RedrawComplete", "TypesetComplete", "QCComplete",
                            "Uploaded"]:
        return
    __force_connection()
    __cursor.execute('update Chapters set '+field_name+'=? where RelatedMangaID=? and ChapterNumber=?',
                    (new_value,manga_id,chapter_number))
    __connection.commit()


def create_manga(Manga):
    __force_connection()
    __cursor.execute('insert into Manga values (?,?,?,?,?,?,?,?,?)',
                        __manga_to_tuple(Manga,))
    __connection.commit()

def create_chapter(Manga,chapter_number):
    chapter = ch.Chapter(Manga, chapter_number)
    create_chapter_o(chapter)

def create_chapter_o(Chapter):
    __force_connection()
    __cursor.execute("""insert into Chapters (RelatedMangaID, ChapterNumber,
                        Translator, Proofreader, Redrawer, Typesetter, QC,
                        TranslationComplete, ProofreadComplete, RedrawComplete,
                        TypesetComplete, QCComplete, Uploaded)
                        values (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    __chapter_to_tuple(Chapter))
    __connection.commit()