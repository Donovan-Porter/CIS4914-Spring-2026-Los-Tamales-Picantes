
from Noun import Noun

class Pronoun(Noun) :
    '''
    SPN1130 : Subject pronouns
    SPN1131 : Direct object pronouns, indirect object pronouns
    '''

    def __init__(self, person=1, plural=False, gender="masculine", formality="informal", function="subject", region="america", reference=None, stem=None, ending=None) :
        # for "noun" ("stem":String, "ending":String, "gender":String, "category":List)

        # Pronouns default to definite; indefinite would force singularity
        self._definite = True
        self._category = ["no-article", "static-ending", "only-definite"]
        # Pronouns don't have articles
        self._noArticle = True # Also applicable to numbers
        self._staticEnding = True # Also applicable to cumpleanos, etc
        # 'yo', 'tu', and 'el' are irregular, so I'm just manually setting endings, and telling the Noun class to not change them; doesn't affect plurality
        self._onlyDefinite = True # Also applicable to 'El mundo', etc.
        # TODO: Find better system than bunches of booleans in a list

        # 1st, 2nd, or 3rd, as integer
        self._person = person
        # Plural or singular as bool
        self._plural = plural
        # 'masculine' or 'feminine' (sentient doesn't apply)
        self._gender = gender
        # 'formal' or 'informal'
        self._formality = formality
        # Pronouns change if pronoun for subject, direct object, or indirect object; only subject implemented as of 2/18/2026
        self._function = function
        # Common usage in America, versus Spain, for vosotros v. ustedes; 'america' versus anything else
        self._region = region
        # Reference Noun object; probably not necessary as the Pronoun class has all the information that the Noun class does
        self._reference = reference


        if stem is not None :

            self._stem = stem
            self._ending = ending

        elif (1 == self._person) and (False == self._plural) :

            self._stem = "yo"
            self._ending = ""
            self._staticEnding = True

        elif (1 == self._person) and (True == self._plural) :

            self._stem = "nosotr"

            if ("feminine" == self._gender) :
                self._ending = "as"

            else :
                self._ending = "os"

        elif (2 == self._person) and (False == self._plural) :

            if ("formal" == self._formality) :
                self._stem = "usted"
                self._ending = ""
            else :
                self._stem = "tú"
                self._ending = ""
            
        elif (2 == self._person) and (True == self._plural) :

            if ("america" == self._region) or ("formal" == self._formality) :
                self._stem = "usted"
                self._ending = "es"

            else :

                self._stem = "vosotr"

                if ("feminine" == self._gender) :
                    self._ending = "as"
                else :
                    self._ending = "os"

        elif (3 == self._person) and (False == self._plural) :

            if ("feminine" == self._gender) :
                self._stem = "ell"
                self._ending = "a"
            else :
                self._stem = "él"
                self._ending = ""

        elif (3 == self._person) :

            if ("feminine" == self._gender) :
                self._stem = "ell"
                self._ending = "as"
            else :
                self._stem = "ell"
                self._ending = "os"

        self._original = (self._stem, self._ending, self._gender, self._category)

    @staticmethod
    def FromNoun(noun) :
        return Pronoun(person=3, plural=noun.GetPlural(), gender=noun.GetGender(), reference=noun)

    @staticmethod
    def FromForm(string) :

        person=1
        plural=False
        gender="masculine"
        formality="informal"
        region="america"
        stem = ""
        ending = ""

        if "yo" == string :
            stem = "yo"

        elif ("tú" ==string) or ("tu" == string) : #

            person = 2
            stem = "tú"

        elif "usted" == string :

            person = 2
            formality = "formal"
            stem = "usted"

        elif "nosotros" == string :

            plural = True
            stem = "nosotr"
            ending = "os"

        elif "nosotras" == string :

            plural = True
            gender = "feminine"
            stem = "nosotr"
            ending = "as"

        elif "vosotros" == string :

            person = 2
            plural = True
            region = "spain"
            stem = "vosotr"
            ending = "os"

        elif "vosotras" == string :

            person = 2
            plural = True
            gender = "feminine"
            region = "spain"
            stem = "vosotr"
            ending = "as"

        elif "ustedes" == string :

            person = 2
            plural = True
            formality = "formal"
            stem = "usted"
            ending = "es"

        elif ("él" == string) or ("el" == string) : 

            person = 3
            stem = "él"

        elif "ellos" == string :

            person = 3
            plural = True
            stem = "ell"
            ending = "os"

        elif "ella" == string :

            person = 3
            gender="feminine"
            stem = "ell"
            ending = "a"

        elif "ellas" == string :

            person = 3
            plural = True
            gender="feminine"
            stem = "ell"
            ending = "as"

        return Pronoun(person=person, plural=plural, gender=gender, formality=formality, region=region, stem=stem, ending=ending)

    @staticmethod
    def Random(person=None, plural=None, gender=None, formality=None, function="subject", region="america") :

        if None is person :
            person = random.randint(1,2,3)

        if None is plural :

            if random.randint(0,1) :
                plural = True
            else :
                plural = False

        if None is gender :

            if random.randint(0,1) :
                gender = "masculine"
            else :
                gender = "feminine"

        if None is formality :

            if random.randint(0,1) :
                formality = "formal"
            else :
                formality = "informal"

        return Pronoun(person=person, plural=plural, gender=gender, formality=formality, function=function, region=region)

    # As it would appear in a sentence
    def __str__(self) :
        return f"{self._stem + self._ending}"
