
import random

# Imports Noun
import Pronoun

# Regular endings are kept here, in a dictionary with keys of form: (tense, ending, pronoun)
from conjugations.all_regular import regular_endings


class Verb :

    # Tenses here combine tense, mood, and aspect
    # I'm told these are the tenses in Spanish
    # https://www.spanishconjugation.net/conjugation-charts/all-tenses/
    '''
    Simple Tenses

    Present Tense / Presente (de indicativo)
    Imperfect Tense / Imperfecto (de indicativo)
    Preterite (Past Tense) / Pretérito (pretérito perfecto simple)
    Future Tense / Futuro
    Conditional Tense / Condicional (potencial simple)
    Subjunctive (Present Subjunctive) / Presente de subjuntivo
    Imperfect Subjunctive / Imperfecto de subjuntivo
    Future Subjunctive / Futuro de subjuntivo
    Imperative (Command) / Imperativo
    Past Participle / Participio Pasado
    Gerund (Present Participle) / Gerundio


    Compound Tenses

    Present Perfect / Perfecto de indicativo
    Past Perfect / Pluscuamperfecto (de indicativo)
    Past Anterior (Preterite Perfect) / Pretérito anterior
    Future Perfect / Futuro perfecto 
    Conditional Perfect / Condicional compuesto (potencial compuesto)
    Present Perfect Subjunctive / Perfecto de subjuntivo
    Pluperfect Subjunctive / Pluscuamperfecto de subjuntivo
    Future Perfect Subjunctive / Futuro perfecto de subjuntivo
    '''

    # These are the tense names (a working list)
    # Reflexive verbs in spn1131 grammar 4
    '''
    'present' # SPN1130 Grammar1
    'imperative' # SPN1131 Grammar1
    'preterite' # SPN1131 Grammar2
    'present perfect' or 'present progressive' # SPN1131 Grammar4
    'imperfect' # SPN1131 Grammar6
    'future'
    'conditional'
    '''

    def __init__(self, tuple, actor=None, tense="present") :
        # for "verb" ("stem":String, "ending":String, "irregularity":List, "transitivity":Bool)

        # The metadata tuple holding the word information
        # This may be useful to find original stems and endings
        self._original = tuple

        # The thing doing the verb (which isn't always the subject)
        # For example: in 'She hops after the *person who **is running** *' the 'person' is the direct object of 'hops', and is doing the 'is running' verb)
        # A Noun object (including Pronoun objects)
        self._actor = actor

        # Stem word
        self._stem = tuple[0]

        # 'ar, 'ir', or 'er'
        self._ending = tuple[1]

        # Irregular forms
        # Nested dictionary with keys of (tense, pronoun) mapped to values of (stem, ending)
        # I.E.: For 'tener': 
        # { ('present', 'yo'): ('ten', 'go'), ('present', 'tu'): ('tien', 'es'), ... }
        # Any regular form can simply omit the key, which means we only store and load the data we need to
        # https://en.wikipedia.org/wiki/Spanish_irregular_verbs
        self._irregularity = tuple[2]

        # Transitive verbs need objects, while intransitive verbs don't
        # Ex: 'to run' is  intransitive, because you can say 'He runs.'
        # Ex cont'd: 'to buy' is transitive, because it implies something being bought; you wouldn't say 'He buys.' without adding the thing being bought
        # We don't need this verb object to record it's actual object, because the verb form doesn't change depending on that,
        # However, we need to know if the verb is transitive for the greater sentence structure to make sense
        # As bool
        self._transitivity = tuple[3]

        # We may need to add reflexivity as a bool

        # 'present', 'preterite', 'imperfect', 'imperative', 'progressive', 'future'
        self._tense = tense

        # Determine overall form based on actor
        self.Conjugate()

    def Conjugate(self) :

        stem = self._stem
        ending = self._ending

        # If there's no actor, then the verb is infinitive ('to do' form)
        if None is self._actor :
            self._stem = stem
            self._ending = ending
        # Conjugate for Pronoun stems first, then anything left over is a regular Noun stem, which can be done by plurality
        # Just calls `ConjugateByPronoun` with relevant pronoun argument
        elif 'yo' == self._actor._stem :
            self.ConjugateByPronoun('yo')
        elif 'tú' == self._actor._stem :
            self.ConjugateByPronoun('tu')
        elif 'vosotr' == self._actor._stem :
            self.ConjugateByPronoun('vosotros')
        elif 'nosotr' ==  self._actor._stem :
            self.ConjugateByPronoun('nosotros')
        elif 'usted' == self._actor._stem :
            if 'es' == self._actor._ending :
                self.ConjugateByPronoun('ustedes')
            else :
                self.ConjugateByPronoun('usted')
        # 'el noun', 'la noun', 'el', and 'ella'
        elif self._actor._plural :
            self.ConjugateByPronoun('ustedes')
        # 'los nouns', 'las nouns', 'ellos', and 'ellas'
        else :
            self.ConjugateByPronoun('usted')

    def GetOriginalStem(self) :
        return self._original[0]

    def GetOriginalEnding(self) :
        return self._original[1]

    def SetActor(self, actor) :
        self._actor = actor

    def GetActor(self) :
        return self._actor

    def ConjugateByPronoun(self, pronoun) :
        '''
        Searches irregularity, or regular-conjugation, dictionaries, based on pronoun,
        and changes stem and/or ending based on results
        '''

        # Revert to original for already-conjugated verbs
        # For stem-changing
        stem = self.GetOriginalStem()
        # For ending
        ending = self.GetOriginalEnding()

        # Get key
        key = (self._tense, pronoun)
        if key in self._irregularity :
            stem = self._irregularity[key][0]
            ending = self._irregularity[key][1]
        else :
            # Find regular ending for tense, infinitive form ending, and relevant pronoun
            ending = regular_endings[(self._tense, self.GetOriginalEnding(), pronoun)]

        self._stem = stem
        self._ending = ending


    def __str__(self) :

        return f"{self._stem}{self._ending}"