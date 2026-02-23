
'''
-ar, -ir, -er verbs
reflexive verbs
transitive verbs
objects
ser adjectives
estar adjectives
sentient nouns
pronouns
non-sentient nouns
article-noun-adjective agreement



clause => (<noun> <adjective>*)? (<verb> <adverb>*){1} (<noun> <adjective>*)?

main_clause => <clause>

main_clause.subject => main_clause.noun

noun.stem # I.E. stem of 'gente' is 'gent', 'persona' is 'person', 'universidad' is 'universidad' etc.
noun.category # food, sport, body part, etc. used for transitive verbs (you wouldn't generally eat a sport)
noun.gender => <'sentient'|'masculine'|'feminine'>

if 'sentient' == noun.gender :
    if random.randint(0,1) :
        noun.gender = 'masculine'
        noun.ending = 'o'
    else :
        noun.gender = 'feminine'
        noun.ending = 'a'

# These are variable
noun.definite => <True|False>
noun.plural => <True|False>

if noun.definite :
    noun.plural = False

noun.article => <'el'|'los'|'la'|'las'|'un'|'una'>
noun.ending => <'o'|'a'|'e'|''>

noun.article = '?'
if !noun.definite :
    if 'masculine' == noun.gender :
        noun.article = 'un'
    else :
        noun.article = 'una'
elif 'masculine' == noun.gender  :
    if !noun.plural :
        noun.article = 'el'
    else :
        noun.article = 'los'
else :
    if  !noun.plural :
        noun.article = 'la'
    else :
        noun.article = 'las'

if noun.plural :
    if '' == noun.ending :
        noun.ending = 'es'
    else :
        noun.ending += 's'

# Adjective endings: 'ista', 'or', 'a', 'e', 'o', '' (consonant)
if 


verb.ending => <'ar'|'ir'|'er'>
verb.irregularity => <True|False> # Provide dictionary of irregular conjugation forms (I.E. {'yo':'tengo'})
verb.stemChange => <True|False> # There are so few, should probably provide forms under irregularities instead of seperately
verb.transitivity => <True|False>

if verb.transitivity :
    verb.object_category # I.E. 'comer' would have the object_category of 'food', and 'jugar' the object_category of 'game'


tense => <present|preterite|imperfect|future|conditional>
mood => <indicative|subjunctive|imperative>
'''


from Noun import Noun
from Pronoun import Pronoun
from Verb import Verb
from data.spn1130.metadata1 import metadata1
from Number import Number


nouns = []
pronouns = ["yo", "tu", "usted", "ustedes", "el", "ellos", "ella", "ellas", "vosotros", "vosotras", "nosotros", "nosotras"]
verbs = []

for key in metadata1.keys() :

    for noun in metadata1[key]["noun"] :
        if "number" not in noun[3] :
            nouns.append(noun)

    for verb in metadata1[key]["verb"] :
        verbs.append(verb)

print("Nouns:")
print()
for word in nouns :

    print(Noun(word))
    print(Noun(word, definite=True))
    print(Noun(word, definite=True, plural=True))
print()
print()

print("Pronouns:")
print()
for word in pronouns :

    pronoun = Pronoun.FromForm(word)

    person = pronoun._person
    gender = pronoun._gender
    plural = pronoun._plural
    formality = pronoun._formality
    region = pronoun._region

    print(f"{pronoun} is {person}-person, gendered {gender}, plural: {plural}, {formality}, from {region}")

    pronoun = Pronoun(person=person, plural=plural, gender=gender, formality=formality, region=region)

    print(f"If we use those to create a pronoun, it is: {pronoun}")
    print()
print()
print()

print("Verbs:")
print()
for word in verbs :

    for pronoun in pronouns :
        pronoun = Pronoun.FromForm(pronoun)
        
        # Present indicative for all pronouns
        verb = Verb(word, actor=pronoun)
        verb.Conjugate()
        print(f"{pronoun} {verb}")
print()
print()

for n in range(0, 10) :
    num = Number()
    print(num)


    
#print(vocab["unit1"])
#print()


