class Manga:
    def __init__(self, manga_id, nickname, full_name = None, translator = None,
                proofreader = None, redrawer = None, typesetter = None, qc = None):
        
        self.manga_id=manga_id
        self.full_name = full_name
        self.nickname = nickname
        
        self.translator = translator
        self.proofreader = proofreader
        self.redrawer = redrawer
        self.typesetter = typesetter
        self.qc = qc

        self.abandoned = False