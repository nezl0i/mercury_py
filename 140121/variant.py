class Variant:

    # =============== 1-й байт варианта исполнения ==============
    @staticmethod
    def get_VarByte1_1(tmp):
        return {
            tmp == "00": "0,2S",
            tmp == "01": "0,5S",
            tmp == "10": "1,0",
            tmp == "11": "2,0",
        }[True]

    @staticmethod
    def get_VarByte1_2(tmp):
        return {
            tmp == "00": "0,2",
            tmp == "01": "0,5",
            tmp == "10": "1,0",
            tmp == "11": "2,0",
        }[True]

    @staticmethod
    def get_VarByte1_3(tmp):
        return {
            tmp == "00": "57,7В",
            tmp == "01": "230В",
        }[True]

    @staticmethod
    def get_VarByte1_4(tmp):
        return {
            tmp == "00": "5А",
            tmp == "01": "1А",
            tmp == "10": "10А"
        }[True]

    # =============== 2-й байт варианта исполнения ==============
    @staticmethod
    def get_VarByte2_1(tmp):
        return {
            tmp == "0": "2",
            tmp == "1": "1"
        }[True]

    @staticmethod
    def get_VarByte2_2(tmp):
        return {
            tmp == "0": "-20 C",
            tmp == "1": "-40 C"
        }[True]

    @staticmethod
    def get_VarByte2_3(tmp):
        return {
            tmp == "0": "Нет",
            tmp == "1": "Есть"
        }[True]

    @staticmethod
    def get_VarByte2_4(tmp):
        return {
            tmp == "0": "3",
            tmp == "1": "1"
        }[True]

    @staticmethod
    def get_VarByte2_5(tmp):
        return {
            tmp == "0000": "5000 имп/кВт∙ч",
            tmp == "0001": "2500 имп/кВт∙ч",
            tmp == "0010": "1250 имп/кВт∙ч",
            tmp == "0011": "500 имп/кВт∙ч",
            tmp == "0100": "1000 имп/кВт∙ч",
            tmp == "0101": "250 имп/кВт∙ч"
        }[True]

    # =============== 3-й байт варианта исполнения ==============
    @staticmethod
    def get_VarByte3_1(tmp):
        return {
            tmp == "0": "С учетом знака",
            tmp == "1": "По модулю"
        }[True]

    @staticmethod
    def get_VarByte3_2(tmp):
        return {
            tmp == "0": "Внешний",
            tmp == "1": "Внутренний"
        }[True]

    @staticmethod
    def get_VarByte3_3(tmp):
        return {
            tmp == "00": "A+R+",
            tmp == "01": "A+"
        }[True]

    @staticmethod
    def get_VarByte3_4(tmp):
        return {
            tmp == "0001": "Вариант 1",
            tmp == "0010": "Вариант 2",
            tmp == "0011": "Вариант 3",
            tmp == "0100": "Вариант 4",
        }[True]

    # =============== 4-й байт варианта исполнения ==============
    @staticmethod
    def get_VarByte4_1(tmp):
        return {
            tmp == "0": "65,5x8",
            tmp == "1": "131x8"
        }[True]

    @staticmethod
    def get_VarByte4_2(tmp):
        return {
            tmp == "0": "Нет",
            tmp == "1": "Есть"
        }[True]

    @staticmethod
    def get_VarByte4_3(tmp):
        return {
            tmp == "0": "Нет",
            tmp == "1": "Есть"
        }[True]

    @staticmethod
    def get_VarByte4_4(tmp):
        return {
            tmp == "0": "Нет",
            tmp == "1": "Есть"
        }[True]

    @staticmethod
    def get_VarByte4_5(tmp):
        return {
            tmp == "00": "CAN",
            tmp == "01": "RS-485",
            tmp == "10": "Резерв",
            tmp == "11": "Нет",
        }[True]

    @staticmethod
    def get_VarByte4_6(tmp):
        return {
            tmp == "0": "Нет",
            tmp == "1": "Есть"
        }[True]

    @staticmethod
    def get_VarByte4_7(tmp):
        return {
            tmp == "0": "Нет",
            tmp == "1": "Есть"
        }[True]

    # =============== 7-й байт варианта исполнения ==============
    @staticmethod
    def get_VarByte7_1(tmp):
        return {
            tmp == "0000": "Не используется",
            tmp == "0001": "5000 имп/кВт∙ч",
            tmp == "0010": "2500 имп/кВт∙ч",
            tmp == "0011": "1250 имп/кВт∙ч",
            tmp == "0100": "500 имп/кВт∙ч",
            tmp == "0101": "1000 имп/кВт∙ч",
            tmp == "0110": "250 имп/кВт∙ч"
        }[True]
