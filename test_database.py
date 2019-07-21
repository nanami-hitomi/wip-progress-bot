import database

#need classes from these
import manga
import chapter

#Test initialization
database.initialize()
assert database.__connection_open, "Database connection not opened"
assert database.__connection is not None, "Connection object not initialized"
assert database.__cursor is not None, "Cursor not initialized"

#remove past test values...
database.__cursor.execute('delete from Manga where MangaID=12345')
database.__cursor.execute('delete from Chapters where RelatedMangaID=12345')

#Test creating values
test_write_manga = manga.Manga(12345, "kobayashi")
database.create_manga(test_write_manga)

#test creating chapters
database.create_chapter(test_write_manga, 1)
test_write_chapter = chapter.Chapter(test_write_manga, 2)
database.create_chapter_o(test_write_chapter)

#have to manually check in the sqlite files if these are present
print("Check in sqlite file after completion if the chapters and manga are present and correct")

#test getting ID from nickname
test_id = database.get_manga_id("kobayashi")
assert test_id, "Failed to get ID"
assert test_id == 12345, "ID is incorrect"

#test retreiving values
#for manga
test_read_manga = database.get_manga(12345)
assert test_read_manga, "Failed to get manga from database"
assert test_read_manga.manga_id == 12345, "Bad ID returned for Manga"
assert test_read_manga.nickname =="kobayashi", "Incorrect name returned for Manga"
assert not test_read_manga.full_name, "Bad value returned for Manga full name"
assert not test_read_manga.abandoned, "Incorrect default value for abandoned"
#for chapters
test_read_chapter = database.get_chapter(12345, 1)
assert test_read_chapter, "Failed to get chapter from database"
assert test_read_chapter.related_manga_id == 12345, "Incorrect related manga ID"
assert test_read_chapter.chapter_number == 1, "Incorrect chapter number"
assert not test_read_chapter.uploaded, "Incorrect default value for uploaded"
assert not test_read_chapter.translator, "Bad value returned for chapter's translator"

#test editing values for manga
database.set_manga(12345, "FullName", "Miss Kobayashi's Dragon Maid")
database.set_manga(12345, "Abandoned", 1)

#re-read the manga
test_read_manga = database.get_manga(12345)
assert test_read_manga.full_name == "Miss Kobayashi's Dragon Maid", "Text value failed to be correctly modified"
assert test_read_manga.abandoned, "Boolean value failed to correctly modify"

#test editing values for chapters
database.set_chapter(12345, 1, "Translator", "Tohru")
database.set_chapter(12345, 1, "Uploaded", 1)
database.set_chapter(12345, 1, "ChapterNumber", 3)

#re-read the chapter
test_read_chapter = database.get_chapter(12345, 3)
assert test_read_chapter.translator == "Tohru", "Text value for translator failed to modify correctly in chapter"
assert test_read_chapter.uploaded, "Boolean value for uploaded failed to modify in chapter"
assert test_read_chapter.chapter_number == 3, "Chapter number failed to modify"

print("Check that modifications worked in the .sqlite file")

#De-initialize the database
database.deinitialize()
assert not database.__connection_open, "Connection failed to close"

print("Check .sqlite file, but otherwise all checks succeeded")