from enum import Enum

class TipoOpciones(Enum):
    AMERICANO = "Americano"
    MOZZARELLA = "Mozzarella"
    LITE_LINE = "Lite Line"


class PresentacionOpciones(Enum):
    REBANADAS_25 = "25 Rebanadas"
    REBANADAS_50 = "50 Rebanadas"
    REBANADAS_75 = "75 Rebanadas"
    KILOGRAMOS_2 = "2 kg."


class CuartoOpciones(Enum):
    CUARTO_1 = 1
    CUARTO_2 = 2
    CUARTO_3 = 3


class LadoOpciones(Enum):
    LADO_A = "A"
    LADO_B = "B"



class RackOpciones(Enum):
    RACK_1 = 1
    RACK_2 = 2
    RACK_3 = 3
    RACK_4 = 4
    RACK_5 = 5
    RACK_6 = 6
    RACK_7 = 7



class NivelOpciones(Enum):
    NIVEL_1 = 1
    NIVEL_2 = 2
    NIVEL_3 = 3



class PosicionOpciones(Enum):
    POSICION_1 = 1
    POSICION_2 = 2
    POSICION_3 = 3
    POSICION_4 = 4
    POSICION_5 = 5
    POSICION_6 = 6
    POSICION_7 = 7