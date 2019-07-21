create table if not exists Manga (
    MangaID integer primary key,
    FullName text,
    Nickname text not null,

    Translator text,
    Proofreader text,
    Redrawer text,
    Typesetter text,
    QC text,

    Abandoned integer default 0
);

create table if not exists Chapters (
    ID integer primary key,
    RelatedMangaID integer not null,

    ChapterNumber int not null,

    Translator text,
    Proofreader text,
    Redrawer text,
    Typesetter text,
    QC text,

    TranslationComplete integer default 0,
    ProofreadComplete integer default 0,
    RedrawComplete integer default 0,
    TypesetComplete integer default 0,
    QCComplete integer default 0,
    Uploaded integer default 0
);