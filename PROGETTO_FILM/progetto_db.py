import sqlite3

def dbinit():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo TEXT NOT NULL,
    trama TEXT,
    anno INTEGER,
    url_locandina TEXT,
    tmdb_id TEXT,
    utente_id INTEGER,
    FOREIGN KEY (utente_id) REFERENCES utenti(id)
)
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS elementi_video (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        film_id INTEGER NOT NULL,
        utente_id INTEGER NOT NULL,
        url_video_youtube TEXT NOT NULL,
        commento TEXT,
        FOREIGN KEY (film_id) REFERENCES film (id),
        FOREIGN KEY (utente_id) REFERENCES utenti (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film_id INTEGER NOT NULL,
    utente_id INTEGER NOT NULL,
    testo TEXT NOT NULL,
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (utente_id) REFERENCES utenti(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        token TEXT
    )
    """)

    conn.commit()

    # Controllo se è vuoto
    cursor.execute("SELECT * FROM film")
    risultato = cursor.fetchall()

    if not risultato:
        film_esempi = [

    (
        "Inception",
        "Un ladro che ruba segreti aziendali attraverso l'uso della tecnologia di condivisione dei sogni riceve il compito inverso di piantare un'idea nella mente di un CEO.",
        2010,
        "https://image.tmdb.org/t/p/w500/5QHWgqaBxZI1eM5e3YhyKzY5o3z.jpg",
        "27205"
    ),

    (
        "The Matrix",
        "Un hacker scopre da misteriosi ribelli la vera natura della sua realtà e il suo ruolo nella guerra contro i suoi controllori.",
        1999,
        "https://image.tmdb.org/t/p/w500/yQZX4scmfYtj4ccKFNGZJlOj1y9.jpg",
        "603"
    ),

    (
        "Interstellar",
        "Un gruppo di esploratori viaggia attraverso un wormhole nello spazio nel tentativo di garantire la sopravvivenza dell'umanità.",
        2014,
        "https://image.tmdb.org/t/p/w500/bMKiLh0mES4Uiococ240lbbTGXQ.jpg",
        "157336"
    ),

    (
        "Il Gladiatore",
        "Un ex generale romano cerca vendetta contro l'imperatore corrotto che ha assassinato la sua famiglia e lo ha condannato alla schiavitù.",
        2000,
        "https://image.tmdb.org/t/p/w500/euOKjQaV1QXtzLyNZAa1PMHGJlJ.jpg",
        "98"
    ),

    (
        "Pulp Fiction",
        "Le vite di due assassini della mafia, di un pugile, della moglie di un gangster e di una coppia di banditi di periferia si intrecciano in quattro storie di violenza e redenzione.",
        1994,
        "https://image.tmdb.org/t/p/w500/hOpN58hkQGZph5LHhyRrryy1hzF.jpg",
        "680"
    ),

    (
        "Fight Club",
        "Un impiegato insonne e un disinvolto produttore di sapone formano un club di combattimento clandestino che si evolve in qualcosa di molto più grande.",
        1999,
        "https://image.tmdb.org/t/p/w500/rtNLQ8HbPElzEfrHjrzSr07prKT.jpg",
        "550"
    ),

    (
        "Il Cavaliere Oscuro",
        "Quando la minaccia nota come il Joker semina caos e distruzione a Gotham City, Batman deve accettare uno dei più grandi test psicologici e fisici della sua vita.",
        2008,
        "https://image.tmdb.org/t/p/w500/qIhsgno1mjbzUbs4H6DaRjhskAR.jpg",
        "155"
    ),

    (
        "Forrest Gump",
        "Le presidenze di Kennedy e Johnson, gli eventi del Vietnam, del Watergate e altre vicende storiche si snodano attraverso la prospettiva di un uomo dell'Alabama con un basso quoziente intellettivo.",
        1994,
        "https://image.tmdb.org/t/p/w500/gsbmOBQKIzO3q57pITk9Ol4urV2.jpg",
        "13"
    ),

    (
        "Avatar",
        "Un marine paraplegico inviato sul pianeta Pandora in una missione unica si ritrova diviso tra il seguire gli ordini e il proteggere il mondo che sente come la sua nuova casa.",
        2009,
        "https://image.tmdb.org/t/p/w500/cu6CTvQqVvaTUmWNGWydpf7EzmV.jpg",
        "19995"
    ),

    (
        "La Città Incantata",
        "Durante il trasloco della sua famiglia in periferia, una bambina di 10 anni vaga in un mondo governato da dei, streghe e spiriti, dove gli umani vengono trasformati in bestie.",
        2001,
        "https://image.tmdb.org/t/p/w500/3PV6lq9BNmoyyDXr5tdNeeESEMn.jpg",
        "129"
    ),

    (
        "Spider-Man: Into the Spider-Verse",
        "Il adolescente Miles Morales diventa lo Spider-Man del suo universo e deve unirsi ad altri cinque eroi ragno provenienti da altre dimensioni per fermare una minaccia totale.",
        2018,
        "https://image.tmdb.org/t/p/w500/7pgJHduD3OVwF3EGFnGBq0nOUYv.jpg",
        "324857"
    ),

    (
        "Whiplash",
        "Un promettente giovane batterista si iscrive a un conservatorio musicale d'élite dove i suoi sogni di grandezza sono guidati da un istruttore che non si fermerà davanti a nulla pur di realizzare il potenziale dello studente.",
        2014,
        "https://image.tmdb.org/t/p/w500/jQwkXN38AGrK2s3LJqxZow1Ic7z.jpg",
        "244786"
    ),

    (
        "Parasite",
        "L'avidità e la discriminazione di classe minacciano il neonato rapporto simbiotico tra la ricca famiglia Park e la famiglia Kim, decisamente meno abbiente.",
        2019,
        "https://image.tmdb.org/t/p/w500/mMM8kcfspicib7AmPTvf97Rarwn.jpg",
        "496243"
    ),

    (
        "Il Signore degli Anelli: La Compagnia dell'Anello",
        "Un timido Hobbit della Contea e otto compagni intraprendono un viaggio per distruggere il potente Unico Anello e salvare la Terra di Mezzo dal Signore Oscuro Sauron.",
        2001,
        "https://image.tmdb.org/t/p/w500/iZTDPQYgr3rhL7hPIYFt17ATp8.jpg",
        "120"
    ),

    (
        "Star Wars: Una Nuova Speranza",
        "Luke Skywalker unisce le forze con un cavaliere Jedi, un pilota arrogante, un Wookiee e due droidi per salvare la galassia dall'arma di distruzione di massa dell'Impero, salvando la principessa Leia.",
        1977,
        "https://image.tmdb.org/t/p/w500/aWq0skBAaZYzZFVdiJwqF0bU4NO.jpg",
            "11"
        ),

(
    "Oppenheimer",
    "La storia dello scienziato che guidò il Progetto Manhattan.",
    2023,
    "https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg",
    "872585"
),

(
    "Dune",
    "Paul Atreides affronta il proprio destino sul pianeta desertico Arrakis.",
    2021,
    "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
    "438631"
),

(
    "Titanic",
    "Una storia d'amore nasce a bordo del transatlantico destinato ad affondare.",
    1997,
    "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "597"
),

(
    "The Prestige",
    "Due illusionisti rivali ossessionati dal successo si sfidano fino all'estremo.",
    2006,
    "https://image.tmdb.org/t/p/w500/5MXyQfz8xUP3dIFPTubhTsbFY6N.jpg",
    "1124"
),

(
    "Memento",
    "Un uomo affetto da perdita di memoria a breve termine cerca l'assassino della moglie.",
    2000,
    "https://image.tmdb.org/t/p/w500/fKTPH2WvH8nHTXeBYBVhawtRqtR.jpg",
    "77"
),

(
    "Django Unchained",
    "Uno schiavo liberato cerca di salvare la moglie da un crudele proprietario terriero.",
    2012,
    "https://image.tmdb.org/t/p/w500/7oWY8VDWW7thTzWh3OKYRkWUlD5.jpg",
    "68718"
),

(
    "Joker",
    "La trasformazione di Arthur Fleck nel criminale noto come Joker.",
    2019,
    "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
    "475557"
),

(
    "Blade Runner 2049",
    "Un replicante scopre un segreto capace di cambiare il destino dell'umanità.",
    2017,
    "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
    "335984"
),

(
    "The Shawshank Redemption",
    "Due detenuti instaurano una profonda amicizia durante gli anni trascorsi in prigione.",
    1994,
    "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    "278"
),

(
    "The Green Mile",
    "Una guardia carceraria assiste a eventi straordinari nel braccio della morte.",
    1999,
    "https://image.tmdb.org/t/p/w500/velWPhVMQeQKcxggNEU8YmIo52R.jpg",
    "497"
),

(
    "Goodfellas",
    "L'ascesa e la caduta di un membro della mafia italoamericana.",
    1990,
    "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
    "769"
),

(
    "Il Padrino",
    "La famiglia mafiosa Corleone affronta una fase di transizione del potere.",
    1972,
    "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "238"
),

(
    "Il Padrino - Parte II",
    "Il passato e il presente della famiglia Corleone si intrecciano.",
    1974,
    "https://image.tmdb.org/t/p/w500/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg",
    "240"
),

(
    "Se7en",
    "Due detective danno la caccia a un serial killer ossessionato dai sette peccati capitali.",
    1995,
    "https://image.tmdb.org/t/p/w500/6yoghtyTpznpBik8EngEmJskVUO.jpg",
    "807"
),

(
    "The Wolf of Wall Street",
    "La storia dell'ascesa e degli eccessi di Jordan Belfort.",
    2013,
    "https://image.tmdb.org/t/p/w500/34m2tygAYBGqA9MXKhRDtzYd4MR.jpg",
    "106646"
),

(
    "Shutter Island",
    "Due agenti investigano sulla scomparsa di una paziente in un ospedale psichiatrico.",
    2010,
    "https://image.tmdb.org/t/p/w500/4GDy0PHYX3VRXUtwK5ysFbg3kEx.jpg",
    "11324"
),

(
    "The Truman Show",
    "Un uomo scopre che tutta la sua vita è un programma televisivo.",
    1998,
    "https://image.tmdb.org/t/p/w500/vuza0WqY239yBXOadKlGwJsZJFE.jpg",
    "37165"
),

(
    "The Social Network",
    "La nascita di Facebook e i conflitti tra i suoi fondatori.",
    2010,
    "https://image.tmdb.org/t/p/w500/n0ybibhJtQ5icDqTp8eRytcIHJx.jpg",
    "37799"
),

(
    "Inglourious Basterds",
    "Un gruppo di soldati progetta di eliminare i vertici del Terzo Reich.",
    2009,
    "https://image.tmdb.org/t/p/w500/7sfbEnaARXDDhKm0CZ7D7uc2sbo.jpg",
    "16869"
),

(
    "La La Land",
    "Una giovane attrice e un musicista inseguono i propri sogni a Los Angeles.",
    2016,
    "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
    "313369"
),

(
    "The Revenant",
    "Un cacciatore lotta per sopravvivere dopo essere stato abbandonato dal suo gruppo.",
    2015,
    "https://image.tmdb.org/t/p/w500/ji3ecJphATlVgWNY0B0RVXZizdf.jpg",
    "281957"
),

(
    "Rocky",
    "Un pugile sconosciuto riceve l'occasione della vita.",
    1976,
    "https://image.tmdb.org/t/p/w500/czKnE6xFUTtYBSE8hR4gWQnkM4Q.jpg",
    "1366"
),

(
    "Alien",
    "L'equipaggio di una nave spaziale affronta una creatura letale.",
    1979,
    "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg",
    "348"
),

(
    "Aliens",
    "Ripley torna sul pianeta infestato dagli xenomorfi.",
    1986,
    "https://image.tmdb.org/t/p/w500/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg",
    "679"
),

(
    "Terminator 2: Il giorno del giudizio",
    "Un cyborg viene inviato per proteggere il futuro leader della resistenza.",
    1991,
    "https://image.tmdb.org/t/p/w500/5M0j0B18abtBI5gi2RhfjjurTqb.jpg",
    "280"
),

(
    "Ritorno al Futuro",
    "Un adolescente viaggia accidentalmente nel passato.",
    1985,
    "https://image.tmdb.org/t/p/w500/7lyBcpYB0Qt8gYhXYaEZUNlNQAv.jpg",
    "105"
),

(
    "Jurassic Park",
    "Un parco popolato da dinosauri clonati sfugge al controllo.",
    1993,
    "https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg",
    "329"
),

(
    "Il Re Leone",
    "Un giovane leone deve affrontare il proprio destino per diventare re.",
    1994,
    "https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
    "8587"
),

(
    "Toy Story",
    "I giocattoli prendono vita quando gli esseri umani non sono presenti.",
    1995,
    "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg",
    "862"
),

(
    "Il Silenzio degli Innocenti",
    "Una giovane agente dell'FBI chiede l'aiuto di un brillante ma pericoloso serial killer per catturarne un altro.",
    1991,
    "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg",
    "274"
),

(
    "American Beauty",
    "Un uomo di mezza età attraversa una profonda crisi esistenziale che sconvolge la sua vita familiare.",
    1999,
    "https://image.tmdb.org/t/p/w500/wby9315QzVKdW9BonAefg8jGTTb.jpg",
    "14"
),

(
    "Mad Max: Fury Road",
    "In un deserto post-apocalittico un gruppo di ribelli fugge da un tiranno spietato.",
    2015,
    "https://image.tmdb.org/t/p/w500/hA2ple9q4qnwxp3hKVNhroipsir.jpg",
    "76341"
),

(
    "Salvate il Soldato Ryan",
    "Durante la Seconda Guerra Mondiale un gruppo di soldati parte per una missione impossibile dietro le linee nemiche.",
    1998,
    "https://image.tmdb.org/t/p/w500/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg",
    "857"
),

(
    "Schindler's List",
    "Un imprenditore salva centinaia di ebrei durante l'Olocausto impiegandoli nelle proprie fabbriche.",
    1993,
    "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
    "424"
),

(
    "The Departed",
    "Un poliziotto infiltrato e una talpa della mafia cercano di smascherarsi a vicenda.",
    2006,
    "https://image.tmdb.org/t/p/w500/nT97ifVT2J1yMQmeq20Qblg61T.jpg",
    "1422"
),

(
    "The Shining",
    "Uno scrittore accetta un lavoro come custode di un hotel isolato dove iniziano a verificarsi eventi inquietanti.",
    1980,
    "https://image.tmdb.org/t/p/w500/xazWoLealQwEgqZ89MLZklLZD3k.jpg",
    "694"
),

(
    "Il Pianista",
    "Un pianista ebreo lotta per sopravvivere nella Varsavia occupata dai nazisti.",
    2002,
    "https://image.tmdb.org/t/p/w500/2hFvxCCWrTmCYwfy7yum0GKRi3Y.jpg",
    "423"
),

(
    "Cast Away",
    "Un dipendente di una compagnia aerea rimane bloccato per anni su un'isola deserta.",
    2000,
    "https://image.tmdb.org/t/p/w500/7GJHj4ThD5M4aXAmL0bhTOiaYKD.jpg",
    "8358"
),

(
    "Il Sesto Senso",
    "Un bambino che sostiene di vedere i morti viene seguito da uno psicologo infantile.",
    1999,
    "https://image.tmdb.org/t/p/w500/fIssD3w3SvIhPPmVo4WMgZDVLID.jpg",
    "745"
)
]

        cursor.executemany("""
            INSERT INTO film (titolo, trama, anno, url_locandina, tmdb_id) 
            VALUES (?, ?, ?, ?, ?)
        """, film_esempi)

        conn.commit()
        print("Inseriti con successo 15 film di prova nel database!")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS playlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo_playlist TEXT NOT NULL,
        utente_id INTEGER NOT NULL,
        film_id INTEGER,
        FOREIGN KEY (utente_id) REFERENCES utenti (id)
    )
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS playlist_film ( 
        playlist_id INTEGER NOT NULL, 
        film_id INTEGER NOT NULL, 
        PRIMARY KEY (playlist_id, film_id), 
        FOREIGN KEY (playlist_id) REFERENCES playlist (id) ON DELETE CASCADE, 
        FOREIGN KEY (film_id) REFERENCES film (id) ON DELETE CASCADE 
    ) 
    """)
    cursor.execute("DROP TABLE IF EXISTS playlist_vide")
    cursor.execute("DROP TABLE IF EXISTS playlist_video")
    conn.commit()

    conn.close()
    print("Inizializzazione DB completata")
