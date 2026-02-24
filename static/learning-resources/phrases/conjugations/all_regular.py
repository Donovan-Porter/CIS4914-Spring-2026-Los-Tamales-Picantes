# Regular endings are kept here, in a dictionary with keys of form: (tense, ending, pronoun)
regular_endings = {
    # Present indicative
    ('present', 'ar', 'yo'): 'o', ('present', 'ar', 'tu'): 'as', ('present', 'ar', 'usted'): 'a', ('present', 'ar', 'ustedes'): 'an', ('present', 'ar', 'nosotros'): 'amos', ('present', 'ar', 'vosotros'): 'áis',
    ('present', 'er', 'yo'): 'o', ('present', 'er', 'tu'): 'es', ('present', 'er', 'usted'): 'e', ('present', 'er', 'ustedes'): 'en', ('present', 'er', 'nosotros'): 'emos', ('present', 'er', 'vosotros'): 'éis',
    ('present', 'ir', 'yo'): 'o', ('present', 'ir', 'tu'): 'es', ('present', 'ir', 'usted'): 'e', ('present', 'ir', 'ustedes'): 'en', ('present', 'ir', 'nosotros'): 'imos', ('present', 'ir', 'vosotros'): 'ís',

    # Imperfect
    ('imperfect', 'ar', 'yo'): 'aba', ('imperfect', 'ar', 'tu'): 'abas', ('imperfect', 'ar', 'usted'): 'aba', ('imperfect', 'ar', 'ustedes'): 'aban', ('imperfect', 'ar', 'nosotros'): 'ábamos', ('imperfect', 'ar', 'vosotros'): 'abais',
    ('imperfect', 'er', 'yo'): 'ía', ('imperfect', 'er', 'tu'): 'ías', ('imperfect', 'er', 'usted'): 'ía', ('imperfect', 'er', 'ustedes'): 'ían', ('imperfect', 'er', 'nosotros'): 'íamos', ('imperfect', 'er', 'vosotros'): 'íais',
    ('imperfect', 'ir', 'yo'): 'ía', ('imperfect', 'ir', 'tu'): 'ías', ('imperfect', 'ir', 'usted'): 'ía', ('imperfect', 'ir', 'ustedes'): 'ían', ('imperfect', 'ir', 'nosotros'): 'íamos', ('imperfect', 'ir', 'vosotros'): 'íais',

    # Preterite
    ('preterite', 'ar', 'yo'): 'é', ('preterite', 'ar', 'tu'): 'aste', ('preterite', 'ar', 'usted'): 'ó', ('preterite', 'ar', 'ustedes'): 'aron', ('preterite', 'ar', 'nosotros'): 'amos', ('preterite', 'ar', 'vosotros'): 'asteis',
    ('preterite', 'er', 'yo'): 'í', ('preterite', 'er', 'tu'): 'iste', ('preterite', 'er', 'usted'): 'ió', ('preterite', 'er', 'ustedes'): 'ieron', ('preterite', 'er', 'nosotros'): 'imos', ('preterite', 'er', 'vosotros'): 'isteis',
    ('preterite', 'ir', 'yo'): 'í', ('preterite', 'ir', 'tu'): 'iste', ('preterite', 'ir', 'usted'): 'ió', ('preterite', 'ir', 'ustedes'): 'ieron', ('preterite', 'ir', 'nosotros'): 'imos', ('preterite', 'ir', 'vosotros'): 'isteis',

    # Imperative
    # TODO: Add to Verb class. If imperative, subject can't be 'yo'
    ('imperative', 'ar', 'yo'): '', ('imperative', 'ar', 'tu'): 'a', ('imperative', 'ar', 'usted'): 'e', ('imperative', 'ar', 'ustedes'): 'en', ('imperative', 'ar', 'nosotros'): 'emos', ('imperative', 'ar', 'vosotros'): 'ad',
    ('imperative', 'er', 'yo'): '', ('imperative', 'er', 'tu'): 'e', ('imperative', 'er', 'usted'): 'a', ('imperative', 'er', 'ustedes'): 'an', ('imperative', 'er', 'nosotros'): 'amos', ('imperative', 'er', 'vosotros'): 'ed',
    ('imperative', 'ir', 'yo'): '', ('imperative', 'ir', 'tu'): 'e', ('imperative', 'ir', 'usted'): 'a', ('imperative', 'ir', 'ustedes'): 'an', ('imperative', 'ir', 'nosotros'): 'amos', ('imperative', 'ir', 'vosotros'): 'id',

    # Present progressive participles
    # TODO: Add to verb class(?). If present progressive, requires 'estar' as auxilliary verb + participle
    # Possibly put in Clause class when written
    ('progressive', 'ar', 'yo'): 'ando', ('progressive', 'ar', 'tu'): 'ando', ('progressive', 'ar', 'usted'): 'ando', ('progressive', 'ar', 'ustedes'): 'ando', ('progressive', 'ar', 'nosotros'): 'ando', ('progressive', 'ar', 'vosotros'): 'ando',
    ('progressive', 'er', 'yo'): 'iendo', ('progressive', 'er', 'tu'): 'iendo', ('progressive', 'er', 'usted'): 'iendo', ('progressive', 'er', 'ustedes'): 'iendo', ('progressive', 'er', 'nosotros'): 'iendo', ('progressive', 'er', 'vosotros'): 'iendo',
    ('progressive', 'ir', 'yo'): 'iendo', ('progressive', 'ir', 'tu'): 'iendo', ('progressive', 'ir', 'usted'): 'iendo', ('progressive', 'ir', 'ustedes'): 'iendo', ('progressive', 'ir', 'nosotros'): 'iendo', ('progressive', 'ir', 'vosotros'): 'iendo',

    # Future
    ('future', 'ar', 'yo'): 'aré', ('future', 'ar', 'tu'): 'ás', ('future', 'ar', 'usted'): 'ará', ('future', 'ar', 'ustedes'): 'arán', ('future', 'ar', 'nosotros'): 'aremos', ('future', 'ar', 'vosotros'): 'aréis',
    ('future', 'er', 'yo'): 'eré', ('future', 'er', 'tu'): 'ás', ('future', 'er', 'usted'): 'erá', ('future', 'er', 'ustedes'): 'erán', ('future', 'er', 'nosotros'): 'eremos', ('future', 'er', 'vosotros'): 'eréis',
    ('future', 'ir', 'yo'): 'iré', ('future', 'ir', 'tu'): 'ás', ('future', 'ir', 'usted'): 'irá', ('future', 'ir', 'ustedes'): 'irán', ('future', 'ir', 'nosotros'): 'iremos', ('future', 'ir', 'vosotros'): 'iréis'
}