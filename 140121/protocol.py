import time
from datetime import datetime as dt
from variant import Variant


def _get_answer(tmp):
    return {
        tmp == "00": "OK",
        tmp == "01": "Недопустимая команда или параметр",
        tmp == "02": "Внутренняя ошибка счетчика",
        tmp == "03": "Недостаточен уровень доступа",
        tmp == "04": "Внутренние часы счетчика уже корректировались",
        tmp == "05": "Не открыт канал связи"
    }[True]


class Mercury_230(Variant):
    def __init__(self, ids, ser, sleeping):
        self.id = ids
        self.ser = ser
        self.sleep = sleeping

    def __printStr(self, byte):
        outResult = byte.hex(' ', -1)
        print(f'({dt.now()}): << {outResult}\n')
        time.sleep(self.sleep)
        return False, 'None'

# =================== Тест канала связи ===================

    def testConnect(self, tmp):
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(4)
            if len(outbytes) == 4:
                res = _get_answer(format(outbytes[1], '02X'))
                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ({res})\n')
                return True
            elif 0 < len(outbytes) < 4:
                return self.__printStr(outbytes)
            else:
                return False

# ========================== Авторизация ==================================

    def connect(self, tmp):
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(4)
            if len(outbytes) == 4:
                res = _get_answer(format(outbytes[1], '02X'))
                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ({res})\n')
                return True
            elif 0 < len(outbytes) < 4:
                return self.__printStr(outbytes)
            else:
                return False

# =============================== Чтение сетевого адреса =======================================

    def getId(self, tmp):
        outIdent = ''
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(5)
            if len(outbytes) == 5:
                outIdent = int(format(outbytes[2], '02X'), 16)
                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ( OK )\n')
                return True, outIdent
            elif 0 < len(outbytes) < 5:
                return self.__printStr(outbytes), outIdent
            else:
                return False, outIdent

# ======================= Чтение серийного номера и даты выпуска ======================

    def getNumData(self, tmp):
        outSerialNumber = ''
        outDataWork = ''
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(10)
            if len(outbytes) == 10:
                outSerialNumber = "{0:0=2d}".format(int(format(outbytes[1], '02X'), 16)) \
                                  + "{0:0=2d}".format(int(format(outbytes[2], '02X'), 16)) \
                                  + "{0:0=2d}".format(int(format(outbytes[3], '02X'), 16)) \
                                  + "{0:0=2d}".format(int(format(outbytes[4], '02X'), 16))

                outDataWork = "{0:0=2d}".format(int(format(outbytes[5], '02X'), 16)) + "." \
                              + "{0:0=2d}".format(int(format(outbytes[6], '02X'), 16)) + ".20" \
                              + "{0:0=2d}".format(int(format(outbytes[7], '02X'), 16))

                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ( OK )\n')
                return True, outSerialNumber, outDataWork
            elif 0 < len(outbytes) < 10:
                return self.__printStr(outbytes), outSerialNumber, outDataWork
            else:
                return False, outSerialNumber, outDataWork

# ======================= Чтение варианта исполнения ======================

    def getVariant(self, tmp):
        outByte = ''
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(27)
            if len(outbytes) == 27:
                outPotmp1 = "{0:0=2d}".format(int(format(outbytes[8], '02X'), 16))
                outPotmp2 = "{0:0=2d}".format(int(format(outbytes[9], '02X'), 16))
                outPotmp3 = "{0:0=2d}".format(int(format(outbytes[10], '02X'), 16))

                outBytetmp1 = format(int(format(outbytes[11], '02X'), 16), "08b")
                outByte1_1 = self.get_VarByte1_1(outBytetmp1[0] + outBytetmp1[1])
                outByte1_2 = self.get_VarByte1_2(outBytetmp1[2] + outBytetmp1[3])
                outByte1_3 = self.get_VarByte1_3(outBytetmp1[4] + outBytetmp1[5])
                outByte1_4 = self.get_VarByte1_4(outBytetmp1[6] + outBytetmp1[7])

                outBytetmp2 = format(int(format(outbytes[12], '02X'), 16), "08b")
                outByte2_1 = self.get_VarByte2_1(outBytetmp2[0])
                outByte2_2 = self.get_VarByte2_2(outBytetmp2[1])
                outByte2_3 = self.get_VarByte2_3(outBytetmp2[2])
                outByte2_4 = self.get_VarByte2_4(outBytetmp2[3])
                outByte2_5 = self.get_VarByte2_5(outBytetmp2[4] + outBytetmp2[5] + outBytetmp2[6] + outBytetmp2[7])

                outBytetmp3 = format(int(format(outbytes[13], '02X'), 16), "08b")
                outByte3_1 = self.get_VarByte3_1(outBytetmp3[0])
                outByte3_2 = self.get_VarByte3_2(outBytetmp3[1])
                outByte3_3 = self.get_VarByte3_3(outBytetmp3[2] + outBytetmp3[3])
                outByte3_4 = self.get_VarByte3_4(outBytetmp3[4] + outBytetmp3[5] + outBytetmp3[6] + outBytetmp3[7])

                outBytetmp4 = format(int(format(outbytes[14], '02X'), 16), "08b")
                outByte4_1 = self.get_VarByte4_1(outBytetmp4[0])
                outByte4_2 = self.get_VarByte4_2(outBytetmp4[1])
                outByte4_3 = self.get_VarByte4_3(outBytetmp4[2])
                outByte4_4 = self.get_VarByte4_4(outBytetmp4[3])
                outByte4_5 = self.get_VarByte4_5(outBytetmp4[4] + outBytetmp4[5])
                outByte4_6 = self.get_VarByte4_6(outBytetmp4[6])
                outByte4_7 = self.get_VarByte4_7(outBytetmp4[7])

                outBytetmp5 = format(int(format(outbytes[15], '02X'), 16), "08b")
                outByte5_1 = self.get_VarByte4_7(outBytetmp5[0])
                outByte5_2 = self.get_VarByte4_7(outBytetmp5[1])
                outByte5_3 = self.get_VarByte4_7(outBytetmp5[2])
                outByte5_4 = self.get_VarByte4_7(outBytetmp5[3])
                outByte5_5 = self.get_VarByte4_7(outBytetmp5[4])
                outByte5_6 = self.get_VarByte4_7(outBytetmp5[5])
                outByte5_7 = self.get_VarByte4_7(outBytetmp5[6])
                outByte5_8 = self.get_VarByte4_7(outBytetmp5[7])

                outBytetmp6 = format(int(format(outbytes[16], '02X'), 16), "08b")
                outByte6_1 = self.get_VarByte4_7(outBytetmp6[0])
                outByte6_2 = self.get_VarByte4_7(outBytetmp6[1])
                outByte6_3 = self.get_VarByte4_7(outBytetmp6[2])
                outByte6_4 = self.get_VarByte4_7(outBytetmp6[3])
                outByte6_5 = self.get_VarByte4_7(outBytetmp6[4])
                outByte6_6 = self.get_VarByte4_7(outBytetmp6[5])
                outByte6_7 = self.get_VarByte4_7(outBytetmp6[6])
                outByte6_8 = self.get_VarByte4_7(outBytetmp6[7])

                outBytetmp7 = format(int(format(outbytes[21], '02X'), 16), "08b")
                outByte7_1 = self.get_VarByte7_1(outBytetmp7[0] + outBytetmp7[1] + outBytetmp7[2] + outBytetmp7[3])
                outByte7_2 = self.get_VarByte4_7(outBytetmp7[4])
                outByte7_3 = self.get_VarByte4_7(outBytetmp7[5])
                outByte7_4 = self.get_VarByte4_7(outBytetmp7[6])
                outByte7_5 = self.get_VarByte4_7(outBytetmp7[7])

                outCrcPotmp1 = format(outbytes[17], '02X')
                outCrcPotmp2 = format(outbytes[18], '02X')

                outVartmp1 = "{0:0=2d}".format(int(format(outbytes[19], '02X'), 16))
                outVartmp2 = "{0:0=2d}".format(int(format(outbytes[20], '02X'), 16))

                outPo = outPotmp1 + "." + outPotmp2 + "." + outPotmp3
                outCrcPo = outCrcPotmp1 + outCrcPotmp2
                outVar = outVartmp1 + "." + outVartmp2

                outByte = [outByte1_1, outByte1_2, outByte1_3, outByte1_4, outPo, outCrcPo, outVar, outByte2_1,
                           outByte2_2, outByte2_3, outByte2_4, outByte2_5, outByte3_1, outByte3_2, outByte3_3,
                           outByte3_4, outByte4_1, outByte4_2, outByte4_3, outByte4_4, outByte4_5, outByte4_6,
                           outByte4_7, outByte5_1, outByte5_2, outByte5_3, outByte5_4, outByte5_5, outByte5_6,
                           outByte5_7, outByte5_8, outByte6_1, outByte6_2, outByte6_3, outByte6_4, outByte6_5,
                           outByte6_6, outByte6_7, outByte6_8, outByte7_1, outByte7_2, outByte7_3, outByte7_4,
                           outByte7_5]

                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ( OK )\n')
                return True, outByte
            elif 0 < len(outbytes) < 27:
                return self.__printStr(outbytes), outByte
            else:
                return False, outByte

# ============== Вектора прерываний =======================

    def getVectors(self, tmp):
        lst = ''
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(19)
            if len(outbytes) == 19:
                outResult = outbytes.hex(' ', -1)
                lst = outResult[3:50]
                print(f'({dt.now()}): << {outResult}\n')
                return True, lst
            elif 0 < len(outbytes) < 19:
                return self.__printStr(outbytes), lst
            else:
                return False, lst

# ============== Проверка обновления ПО ===================

    def updateTest(self, tmp):
        tmpIdentPo = None
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(5)
            if len(outbytes) == 5:
                tmpByte1 = format(outbytes[1], '02X')
                tmpByte2 = format(outbytes[2], '02X')
                tmpIdentPo = f'{tmpByte2}{tmpByte1}'
                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult}\n')
                return True, tmpIdentPo
            elif 0 < len(outbytes) < 5:
                return self.__printStr(outbytes)
            else:
                return False, tmpIdentPo

# ========================= Прошивка ======================================

    def firmware(self, tmp):
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(4)
            if len(outbytes) == 4:
                answers = format(outbytes[1], '02X')
                res = _get_answer(answers)
                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ({res})\n')
                return True
            elif 0 < len(outbytes) < 4:
                return self.__printStr(outbytes)
            else:
                return False

# ========================= Завершение прошивка ======================================

    def firmwareEnd(self, tmp):
        answers = None
        self.sleep = None
        print(f'({dt.now()}): >> {tmp}')
        data = bytearray.fromhex(tmp)
        self.ser.write(data)
        while True:
            outbytes = self.ser.read(4)
            if len(outbytes) == 4:
                answers = format(outbytes[1], '02X')
                res = _get_answer(answers)
                outResult = outbytes.hex(' ', -1)
                print(f'({dt.now()}): << {outResult} ({res})\n')
                return True, answers
            elif 0 < len(outbytes) < 4:
                return self.__printStr(outbytes)
            else:
                return False, answers
