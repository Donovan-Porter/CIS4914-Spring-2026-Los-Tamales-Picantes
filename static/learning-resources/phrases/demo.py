from Noun import Noun
from Pronoun import Pronoun
from Verb import Verb
from data.spn1130.metadata1 import metadata1

import random


print()


nouns = []
pronouns = ["yo", "tu", "usted", "ustedes", "el", "ellos", "ella", "ellas", "vosotros", "vosotras", "nosotros", "nosotras"]
verbs = []
tenses = ['present', 'preterite', 'imperfect', 'imperative', 'progressive', 'future']

for key in metadata1.keys() :

    for noun in metadata1[key]["noun"] :
        if "number" not in noun[3] :
            nouns.append(noun)

    for verb in metadata1[key]["verb"] :
        verbs.append(verb)

for n in range(0,15) :

    subject = None
    if random.randint(0,1) :
        subject = Pronoun.FromForm(pronouns[random.randint(0,11)])
    else :
        subject = Noun(nouns[random.randint(0,len(nouns)-1)], random=True)

    the_verb = verbs[random.randint(0,len(verbs)-1)]
    the_tense = tenses[random.randint(0,len(tenses)-1)]

    action = Verb(the_verb, actor=subject, tense=the_tense)

    object = Noun(nouns[random.randint(0,len(nouns)-1)], random=True)

    
    print(f"{the_tense}: \n {subject} {action} {object}\n")

print()

