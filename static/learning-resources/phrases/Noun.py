
import random


class Noun :

    def __init__(self, tuple, definite=False, plural=False, random=False) :
        # for "noun" ("stem":String, "ending":String, "gender":String, "category":List)

        # The tuple which was passed in; useful for knowing if something is labeled 'sentient'
        self._original = tuple

        # Stem word
        self._stem = tuple[0]
        # Ending of word, usually 'o' or 'a', but 'universidad' would have empty ('') ending
        self._ending = tuple[1]
        # 'masculine', 'feminine', or 'sentient'
        self._gender = tuple[2]
        # List of key words; certain things might have syntax or grammatical uses ('no-article')
        # 
        self._category = tuple[3]

        # Put in for pronouns; also applicable to numbers
        if "no-article" in self._category :
            self._noArticle = True
        else :
            self._noArticle = False

        # Put in for pronouns (due to irregularity of 'yo', 'tu', and 'el'); not currently applicable to anything else, as only regular endings are changed so far
        if "static-ending" in self._category :
            self._staticEnding = True
        else :
            self._staticEnding = False

        # Used to keep pronouns singular (so no change to 'yoes' from 'yo', or something similar); also applicable to words like 'el mundo', but probably better implemented some other way
        if "only-definite" in self._category :
            self._onlyDefinite = True
        else :
            self._onlyDefinite = False

        # Either definite ('el', 'la', 'ellos', 'ellas'), or indefinite ('un', 'una'), as a bool
        self._definite = definite
        # Singular or plural, as a bool
        self._plural = plural

        if random :

            self.Randomize()

        else :

            if not self._definite :
                self._plural = False

            # Determines gender for sentients, then the article and ending
            self.DetermineGender()


    # Used to create random correct form
    def Randomize(self) :

        self.RandomizeGender()
        self.RandomizeDefiniteness()
        self.RandomizePlurality()

        self.DetermineArticle()
        self.DetermineEnding()


    # Used to randomly determine genders, then determine endings and articles, of sentient-gendered things
    def DetermineGender(self) :

        # If sentient, determine gender
        if ("sentient" == self._gender) :
            if 0 == random.randint(0,1) :
                self._gender = "masculine"
            else :
                self._gender = "feminine"

                # Change regular endings to match gender; leave irregular ones alone
                # "o" is going to be used as default for sentient nouns with regular "o" or "a" endings
                # This is to reduce collision with sentient nouns that have non-gendered endings
                if ("o" == self._ending) :
                    self._ending = "a"

        self.DetermineArticle()
        self.DetermineEnding()


    # This can be used to force things to have wrong gender
    def SetGender(self, string) :

        if ("masculine" | "feminine") == string :
            self._gender = string
            self.DetermineArticle()
            self.DetermineEnding()
        elif "sentient" == string :
            self.DetermineGender()

    def GetOriginalGender(self) :
        return self._original[2]

    def GetGender(self) :
        return self._gender

    def GetPlural(self) :
        return self._plural

    def GetOriginalEnding(self) :
        return self._original[1]

    # This can be used to create random correct forms
    def RandomizeGender(self) :
        
        if "sentient" == self.GetOriginalGender() :
            self.SetGender("sentient")


    def SetDefinite(self, bool) :

        if self._onlyDefinite : # For pronouns
            return

        self._definite = bool
        if not bool :
            self._plural = False


    def RandomizeDefiniteness(self) :

        if 0 == random.randint(0,1) :
            self.SetDefinite(False)
        else :
            self.SetDefinite(True)


    def SetPlural(self, bool) : # Will muck up pronouns

        _plural = bool


    def RandomizePlurality(self) : # Will muck up pronouns TODO: Find better system for pronoun handling

        if self._definite :
            if 0 == random.randint(0, 1) :
                self._plural = True
            else :
                self._plural = False
        else :
            self._plural = False


    def DetermineArticle(self) :

        if self._noArticle :
            self._article = ""
            return

        if not self._definite :
            if 'masculine' == self._gender :
                self._article = 'un'
            else :
                self._article = 'una'
        elif 'masculine' == self._gender  :
            if not self._plural :
                self._article = 'el'
            else :
                self._article = 'los'
        else :
            if not self._plural :
                self._article = 'la'
            else :
                self._article = 'las'

    # Resets sentient genders
    def DetermineEnding(self) :

        self._ending = self.GetOriginalEnding()

        if "sentient" == self.GetOriginalGender() :
            self.setGender("sentient")

        if self._plural and (not self._staticEnding) : # _staticEnding added for pronouns, but plurality is also problem for them; also applicable to 'cumpleanos', etc.
            if ('' == self._ending) :
                self._ending = 'es'
            else :
                if ("a" == self._ending) or ("o" == self._ending) or ("e" == self._ending) :
                    self._ending += 's'


    # As it would appear in a sentence
    def __str__(self) :

        string = ""

        if not self._noArticle : # _noArticle added for pronouns, but also applicable to numbers
            string += f"{self._article} "

        string += self._stem
        string += self._ending

        return string
