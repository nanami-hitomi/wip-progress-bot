class Chapter:
    def __init__(self, Manga, chapter_number):
        self.related_manga_id=Manga.manga_id
        self.related_manga = Manga
        self.chapter_number=chapter_number
        
        self.translator = Manga.translator
        self.proofreader = Manga.proofreader
        self.redrawer = Manga.redrawer
        self.typesetter = Manga.typesetter
        self.qc = Manga.qc

        self.translation_complete = False
        self.proofread_complete = False
        self.redraw_complete = False
        self.typeset_complete = False
        self.qc_complete = False

        self.uploaded = False