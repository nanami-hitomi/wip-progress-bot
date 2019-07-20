create table if not exists Manga (
    MangaID int primary key,
    FullName text,
    Nickname text,

    Translator text,
    Proofreader text,
    Redrawer text,
    Typesetter text,
    QC text,

    Abandoned boolean default 0
)

create table if not exists Chapters (
    ID int primary key,
    RelatedManga int not null,

    ChapterNumber int not null,

    Translator text,
    Proofreader text,
    Redrawer text,
    Typesetter text,
    QC text,

    TranslationComplete boolean default 0,
    ProofreadComplete boolean default 0,
    RedrawComplete boolean default 0,
    TypesetComplete boolean default 0,
    QCComplete boolean default 0,
    Uploaded boolean default 0
)