metadata2 = {
    # for "noun" ("stem":String, "ending":String, "gender":String, "category":List)
    # Nouns with endings of "", "a", "o", or "e", have regular pluralization patterns
    # Sentient nouns with gendered endings need to have "o" as the default to reduce collisions with sentient non-gendered endings
    # for "adjective" ("stem":String, "ending":String, "category":List)
    # for "verb" ("stem":String, "ending":String, "irregularity":Dictionary, "transitivity":Bool)
    # for "adverb" ("stem":String, "variability":Bool)
    "LOS SALUDOS" {
        "noun": [
            # TODO: Make sure 'static-ending' is a good way to handle this
            ("dí", "as", "masculine", ["static-ending"]),
            ("tard", "es", "feminine", ["static-ending"]),
            ("noch", "es", "feminine", ["static-ending"]),
            ("hola", "", "", ["static-ending", "exclamation", "salutation"]) # TODO: Figure out exclamations and neuter nouns
        ],
        "adjective": [
            # 'prior' for adjective expressed before noun 
            # TODO: check this works well after fleshing out adjectives
            # TODO: Figure out how to force agreement with buenos/buenas
            ("buen", "os", ["prior", "always-plural"])
        ],
        "verb": [
        ]
    },
    "LAS DESPEDIDAS": {
        "noun": [
        ("adios", "", "", ["static-ending", "exclamation", "salutation"]),
        ("chau", "", "", ["static-ending", "exclamation", "salutation"]),
        ("luego", "", "", ["static-ending", "time"]),
        ("mañana", "", "", ["static-ending", "time"]),
        ("pronto", "", "", ["static-ending", "time"]),
        ("vemos", "", "", ["static-ending", "time"])
        ],
        "adjective": [
            ("hasta", "", ["preposition", "static-ending"]) # TODO: Do prepositions
        ],
        "verb": [
        ]
    },
    "LAS PREGUNTAS Y RESPUESTAS"{
        "noun": [
            ("especialización", "", "masculine", []),
            ("graci", "as", "", ["static-ending", "exclamation", "thanks"])
        ],
        "adjective": [
            ("Cómo", "", ["interrogative", "static-ending"]), # TODO: Clause construction using interrogative words (not just adjectives),
            ("Qué", "", ["interrogative", "static-ending"]),
            ("tal", "", ["static-ending"]),
            ("bien", "", ["static-ending", "estar"]),
            ("así así", "", ["static-ending", "estar"]),
            ("de", "", ["static-ending", "preposition"]),
            ("dónde", "", ["interrogative", "static-ending"]),
            ("Cuál", "", ["interrogative"]),
            ("y", "", ["preposition"]),
            ("much", "o", ["prior"]),
            ("much", "o", ["preporsition"]),
            ("igual", "", []) # TODO: Do adverbs (add 'mente' to adjectives (always feminine, consonant endings stay same))
        ],
        "verb": [
            ("llam", "ar", {}, True), # TODO: Disambiguate transitive and intransitive definitions; "They call me..." versus "I called out."
            ("pas", "ar", {}, False),
            ("hab", "er", {}, True), # TODO: Irregularities of 'haber'
            ("estudi", "ar", {}, False),
            ("sab", "er", {}, False), # TODO: Irregularites of 'saber'
            ("gust", "ar", {}, True)
        ],
    },
    {
    "Las humanidades": {
        "noun": [
            ("arquitectur", "a", "feminine", []),
            ("art", "e", "masculine", []),
            ("derech", "o", "masculine", []),
            ("español", "", "masculine", ["always-singular"]),
            ("filosofí", "a", "feminine", []),
            ("historia", "a", "feminine", []),
            ("idiom", "a", "masculine", []),
            ("inglés", "", "masculine", ["always-singular"]),
            ("literatur", "a", "feminine", []),
            ("músic", "a", "feminine", []),
            ("pedagogí", "a", "feminine", []),
            ("periodism", "o", "masculine", [])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    },
    {
    "Las ciencias naturales y formales": {
        "noun": [
            ("biologí", "a", "feminine", []),
            ("cienci", "a", "feminine", []),
            ("computación", "", "feminine", []),
            ("informática", "a", "feminine", []),
            ("físic", "a", "feminine", []),
            ("matemátic", "a", "feminine", []),
            ("medicin", "a", "feminine", []),
            ("químic", "a", "feminine", [])
        ],
        "adjective": [
            ("natural", "", [])
        ],
        "verb": [
        ]
    },
    {
    "Las ciencias sociales": {
        "noun": [
            ("cienci", "a", "feminine", []),
            ("administración", "", "feminine", []),
            ("comunicacion", "", "feminine", []),
            ("contabilidad", "", "feminine", []),
            ("economí", "a", "feminine", []),
            ("geografí", "a", "feminine", []),
            ("mercade", "o", "masculine", []),
            ("psicologí", "a", "feminine", []),
            ("sociologí", "a", "feminine", [])
        ],
        "adjective": [
            ("polític", "a", []),
            ("social", "", []),
            ("empres", "a", [])
        ],
        "verb": [
        ]
    },
    {
    "PARA HABLAR DE LOS CURSOS": {
        "noun": [
            ("curs", "o", "masculine", []),
            ("departament", "o", "masculine", []),
            ("examen", "", "masculine", []),
            ("horari", "o", "masculine", []),
            ("lección", "", "feminines", []),
            ("semestr", "e", "masculine", []),
            ("trimestr", "e", "masculine", []),
            ("", "o", "masculine", []),
            ("", "o", "masculine", [])
        ],
        "adjective": [
            ("difícil", "", []),
            ("fácil", "", [])
        ],
        "verb": [
            ("estudi", "ar", {}, False) # TODO: Decide what to do with duplicates
        ]
    }
}