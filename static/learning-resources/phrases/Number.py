

from random import randint
from math import floor


class Number :

    '''
    To say 2,345,678 in Spanish, you would say:
    Dos millones trescientos cuarenta y cinco mil seiscientos setenta y ocho.
    2,000,000: Dos millones
    345,000: Trescientos cuarenta y cinco mil
    678: Seiscientos setenta y ocho 
    '''

    # Irregular numbers (10-29)
    teens = {10: "diez", 11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince", 16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve",
        20: "veinte", 21: "veintiuno", 22: "veintidós", 23: "veintitrés", 24: "veinticuatro", 25: "veinticinco", 26: "veintiséis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve"

    }
    ones = {1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve"}
    tens = {10: "diez", 20: "veinte", 30: "treinte", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa"
    }
    hundreds = {100: "cien", 200: "doscientos", 300: "trescientos", 400: "cuatrocientos", 500: "quinientos", 600: "seiscientos", 700: "setecientos", 800: "ochocientos", 900: "novecientos"
    }

    def __init__(self, integer=None, min=0, max=999) : #range=range(0,999999999)) :

        self._int = 0

        if None is integer :
            self._int = randint(min, max)
        else :
            self._int = integer

        self.MakeString()

    @staticmethod
    def GetHundredsString(integer) :

        if 0 == integer :
            return "cero"

        string = ""
        place_hundreds = 0
        place_tens = 0
        place_ones = 0

        if 100 <= integer :
            place_hundreds = floor(integer / 100) * 100
            string += f"{Number.hundreds[place_hundreds]} "
            integer = integer - place_hundreds

        if 30 <= integer :
            place_tens = floor(integer / 10) * 10
            string += f"{Number.tens[place_tens]} y "
            integer = integer - place_tens
        elif 10 <= integer :
            string += f"{Number.teens[integer]}"
            integer = 0

        if integer != 0 :
            string += f"{Number.ones[integer]}"

        return string

    def MakeString(self) :

        self._str = Number.GetHundredsString(self._int)

    def __str__(self) :
        return self._str

