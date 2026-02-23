
metadata1 = {
    # for "noun" ("stem":String, "ending":String, "gender":String, "category":List)
    # Nouns with endings of "", "a", "o", or "e", have regular pluralization patterns
    # Sentient nouns with gendered endings need to have "o" as the default to reduce collisions with sentient non-gendered endings
    # for "adjective" ("stem":String, "ending":String, "category":List)
    # for "verb" ("stem":String, "ending":String, "irregularity":Dictionary, "transitivity":Bool)
    "LOS PERFILES": {
        "noun": [
            ("calendari", "o", "masculine", ["item", "paper"]),
            ("event", "o", "masculine", ["social"]),
            ("cronolog", "ía", "feminine", ["time"]),
            ("estad", "o", "masculine", ["place"]),
            ("fot", "o", "feminine", ["item"]),
            ("fotografí", "a", "feminine", ["item"]),
            ("perfil", "", "masculine", ["social", "technological"]),
            ("red", "", "masculine", ["group"]),
            ("vide", "o", "masculine", ["visual"])
        ],
        "adjective": [
            ("social", "", [])
        ],
        "verb": [
        ]
    },
    "LAS ACCIONES": {
        "noun": [
            ("mensaj", "e", "feminine", ["writing"]),
        ],
        "adjective": [
            ("social", "", [])
        ],
        "verb": [
            ("mand", "ar", {}, True),
            ("edit", "ar", {}, True),
            ("actualiz", "ar", {}, True),
            ("cre", "ar", {}, True)
        ]
    },
    "LA INFORMACIÓN BÁSICA": {
        "noun": [
            ("apellid", "o", "masculine", {}),
            ("e-mail", "", "masculine", {}),
            ("dirección", "", "feminine", {}),
            ("corre", "o", "masculine", {}),
            ("edad", "", "feminine", {}),
            ("nombr", "e", "masculine", {}),
            ("teléfon", "o", "masculine", {}),
            ("numer", "o", "masculine", {})
        ],
        "adjective": [
            ("electrónic", "o", [])
        ],
        "verb": [
        ]
    },
    "LA BIOGRAFÍA": {
        "noun": [
            ("ciudad", "", "feminine", []),
            ("cumpleañ", "os", "masculine", []), #TODO: Figure out how to handle a singular 'os' ending
            ("escuel", "a", "feminine", []),
            ("estad", "o", "masculine", []),
            ("fech", "a", "feminine", []),
            ("nacimient", "o", "masculine", []),
            ("país", "", "masculine", []),
            ("trabaj", "o", "masculine", []),
            ("universidad", "", "feminine", [])
        ],
        "adjective": [
            ("secundari", "o", [])
        ],
        "verb": [
        ]
    },
    "YO SOY ...": {
        "noun": [
        ],
        "adjective": [
            ("generos", "o", ["ser"]), # These words can be used in conjunction with 'ser'
            ("inteligent", "e", ["ser"]),
            ("sedentari", "o", ["ser"]),
            ("tímid", "o", ["ser"]),
            ("trabajado", "o", ["ser"]),
            ("activ", "o", ["ser"]),
            ("atlétic", "o", ["ser"]),
            ("aventurer", "o", ["ser"]),
            ("cómic", "o", ["ser"]),
            ("estudios" "o", ["ser"]),
        ],
        "verb": [
        ]
    },
    "AHORA ESTOY ...": {
        "noun": [
        ],
        "adjective": [
            ("aburrid", "o", ["estar"]), # These words can be used in conjunction with 'estar'
            ("cansad", "o", ["estar"]),
            ("content", "o", ["estar"]),
            ("emocionad", "o", ["estar"]),
            ("enojad", "o", ["estar"]),
            ("nervios", "o", ["estar"]),
            ("ocupad", "o", ["estar"]),
            ("relajad", "o", ["estar"])
        ],
        "verb": [
        ]
    },
    "AHORA TENGO ...": {
        "noun": [
            ("añ", "o", "masculine", ["tengo"]), # These words can be used in conjunction with 'tener'
            ("calor", "", "masculine", ["tengo"]),
            ("frí", "o", "masculine", ["tengo"]),
            ("hambr", "e", "masculine", ["tengo"]),
            ("mied", "o", "masculine", ["tengo"]),
            ("sueñ", "o", "masculine", ["tengo"]),
            ("sed", "", "masculine", ["tengo"]),
            ("vergüenz", "a", "feminine", ["tengo"])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    },
# TODO: Make numbers procedural so random integer in range can be used to generate them
    "Los números del 0 al 20": {
        "noun": [
            ("cero" , "", "masculine", ["number"]), # Numbers have special grammatical rules (they act as adjectives before word, and don't follow normal article rules)
            ("uno" , "", "masculine", ["number"]),
            ("dos" , "", "masculine", ["number"]),
            ("tres" , "", "masculine", ["number"]),
            ("cuatro" , "", "masculine", ["number"]),
            ("cinco" , "", "masculine", ["number"]),
            ("seis" , "", "masculine", ["number"]),
            ("siete" , "", "masculine", ["number"]),
            ("ocho" , "", "masculine", ["number"]),
            ("nueve" , "", "masculine", ["number"]),
            ("diez" , "", "masculine", ["number"]),
            ("once" , "", "masculine", ["number"]),
            ("doce" , "", "masculine", ["number"]),
            ("trece" , "", "masculine", ["number"]),
            ("catorce" , "", "masculine", ["number"]),
            ("quince" , "", "masculine", ["number"]),
            ("dieciséis" , "", "masculine", ["number"]),
            ("diecisiete" , "", "masculine", ["number"]),
            ("dieciocho" , "", "masculine", ["number"]),
            ("diecinueve" , "", "masculine", ["number"]),
            ("veinte" , "", "masculine", ["number"]),
            ("veintiuno" , "", "masculine", ["number"]),
            ("veintidós" , "", "masculine", ["number"]),
            ("veintitrés" , "", "masculine", ["number"]),
            ("veinticuatro" , "", "masculine", ["number"]),
            ("veinticinco" , "", "masculine", ["number"]),
            ("veintiséis" , "", "masculine", ["number"]),
            ("veintisiete" , "", "masculine", ["number"]),
            ("veintiocho" , "", "masculine", ["number"]),
            ("veintinueve" , "", "masculine", ["number"]),
            ("treinta" , "", "masculine", ["number"])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    },
    "Los números del 31 al 39": {
        "noun": [
            ("treinta y uno" , "", "masculine", ["number"]),
            ("treinta y dos" , "", "masculine", ["number"]),
            ("treinta y tres" , "", "masculine", ["number"]),
            ("treinta y cuatro" , "", "masculine", ["number"]),
            ("treinta y cinco" , "", "masculine", ["number"]),
            ("treinta y seis" , "", "masculine", ["number"]),
            ("treinta y siete" , "", "masculine", ["number"]),
            ("treinta y ocho" , "", "masculine", ["number"]),
            ("treinta y nueve" , "", "masculine", ["number"])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    },
    "Los números del 10 al 90": {
        "noun": [
            ("diez" , "", "masculine", ["number"]),
            ("veinte" , "", "masculine", ["number"]),
            ("treinta" , "", "masculine", ["number"]),
            ("cuarenta" , "", "masculine", ["number"]),
            ("cincuenta" , "", "masculine", ["number"]),
            ("sesenta" , "", "masculine", ["number"]),
            ("setenta" , "", "masculine", ["number"]),
            ("ochenta" , "", "masculine", ["number"]),
            ("noventa" , "", "masculine", ["number"])
        ] ,
        "adjective": [
        ],
        "verb": [
        ] 
    },
    "Los números del 100 al 900": {
        "noun": [
            ("cien" , "", "masculine", ["number"]),
            ("doscientos" , "", "masculine", ["number"]),
            ("trescientos" , "", "masculine", ["number"]),
            ("cuatrocientos" , "", "masculine", ["number"]),
            ("quinientos" , "", "masculine", ["number"]),
            ("seiscientos" , "", "masculine", ["number"]),
            ("setecientos" , "", "masculine", ["number"]),
            ("ochocientos" , "", "masculine", ["number"]),
            ("novecientos" , "", "masculine", ["number"])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    },
    "Los números del 1.000 al 10.000": {
        "noun": [
            ("mil" , "", "masculine", ["number"]),
            ("dos mil" , "", "masculine", ["number"]),
            ("tres mil" , "", "masculine", ["number"]),
            ("cuatro mil" , "", "masculine", ["number"]),
            ("cinco mil" , "", "masculine", ["number"]),
            ("seis mil" , "", "masculine", ["number"]),
            ("siete mil" , "", "masculine", ["number"]),
            ("ocho mil", "", "masculine", ["number"]),
            ("nueve mil", "", "masculine", ["number"]),
            ("diez mil", "", "masculine", ["number"])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    },
# To say 2,345,678 in Spanish, you would say:
# Dos millones trescientos cuarenta y cinco mil seiscientos setenta y ocho.
# 2,000,000: Dos millones
# 345,000: Trescientos cuarenta y cinco mil
# 678: Seiscientos setenta y ocho 
    "Los números del 10.000 a 2.000.000": {
        "noun": [
            ("diez mil", "", "masculine", ["number"]),
            ("veinte mil", "", "masculine", ["number"]),
            ("treinta mil", "", "masculine", ["number"]),
            ("cuarenta mil", "", "masculine", ["number"]),
            ("cincuenta mil", "", "masculine", ["number"]),
            ("sesenta mil", "", "masculine", ["number"]),
            ("setenta mil", "", "masculine", ["number"]),
            ("ochenta mil", "", "masculine", ["number"]),
            ("noventa mil", "", "masculine", ["number"]),
            ("un millón", "", "masculine", ["number"]),
            ("dos millones", "", "masculine", ["number"])
        ],
        "adjective": [
        ],
        "verb": [
        ]
    }
}