"""
sudo usermod -a -G dialout $USER
"""

import serial
import sys
import argparse
import time
import datetime
import os
from modbus_crc16 import crc16
from protocol import Mercury_230
from datetime import datetime as dt
from simple_term_menu import TerminalMenu


def count_def(func, count):
    for _ in range(3):
        if func or func[0]:
            break
    if count == 1:
        return func[1]
    elif count == 2:
        return func[1], func[2]
    else:
        pass


def testChannel():
    data = f'{m_id} 00'
    crc = crc16(bytearray.fromhex(data))
    data = f'{data} {crc}'
    count_def(m_class.testConnect(data), 0)


def openSession():
    data = f'{m_id} 01 {m_level} {m_pass}'
    crc = crc16(bytearray.fromhex(data))
    data = f'{data} {crc}'
    count_def(m_class.connect(data), 0)


def updateFirmware():
    file_path = "update/firmware.txt"
    if os.access(file_path, os.F_OK):
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('@'):
                    hexStr = line[1:].rstrip()
                    if len(hexStr) < 5:
                        addrHi = f'0{hexStr[:1]}'
                        addrLo = f'{hexStr[1:]}0' if len(hexStr[1:]) == 1 else f'{hexStr[1:]}'
                        k = '02'
                    else:
                        addrHi = f'{hexStr[:2]}'
                        addrLo = f'{hexStr[2:4]}'
                        k = '02'
                elif line.startswith('q'):
                    data = f'{m_id} 07 05 12 0F 3C 0F FC 10'
                    crc = crc16(bytearray.fromhex(data))
                    data = f'{data} {crc}'
                    result = count_def(m_class.firmwareEnd(data), 1)
                    print("Обновление выполнено успешно!\n"
                          if result == '00'
                          else "Обновление не выполнено...\n")
                else:
                    data = f'{m_id} 07 05 {k} {addrHi} {addrLo} {line.rstrip()}'
                    crc = crc16(bytearray.fromhex(data))
                    data = f'{data} {crc}'
                    count_def(m_class.firmware(data), 0)
                    if addrLo == 'FF':
                        addrHi = format(int(addrHi, 16) + 1, "02X")
                        addrLo = '00'
                        k = '00'
                    else:
                        k = '00'
                        addrLo = format(int(addrLo, 16) + 1, "02X")
    else:
        print("Файл прошивки не найден, обновление невозможно...\n")


def backToMenu():
    setMenu = input("Завершить?  (Yes/No) : ")
    return 1 if (setMenu == "yes" or setMenu == "y" or setMenu == "Yes" or setMenu == "") else backToMenu()


def printable(work, addr, serial_num, var_byte):
    setMenu = input("Сохранить в файл?  (Yes/No) : ")
    if setMenu == "yes" or setMenu == "y" or setMenu == "Yes" or setMenu == "":
        saveInfoFiles(work, addr, serial_num, var_byte)
        print(f'Информация сохранена в файл {work}_Info.txt')
        return 3
    return 1


def testUpdate():
    vector1, vector2, vector3, vector4 = '', '', '', ''
    tmpSend = ['06 04 1A 04 02', '06 04 F1 C0 10', '06 04 F1 D0 10', '06 04 F1 E0 10', '06 04 F1 F0 10']
    vector = [vector1, vector2, vector3, vector4]
    result_vector = []

    idHardware = {'81A3': 'MSP430F67771', '8190': 'MSP430F6768', '8191': 'MSP430F6769', '8195': 'MSP430F6778',
                  '8196': 'MSP430F6779',
                  '819F': 'MSP430F67681', '81A0': 'MSP430F67691', '81A4': 'MSP430F67781', '81A5': 'MSP430F67791',
                  '821E': 'MSP430F6768A',
                  '821F': 'MSP430F6769A', '8223': 'MSP430F6778A', '8224': 'MSP430F6779A', '822D': 'MSP430F67681A',
                  '822E': 'MSP430F67691A',
                  '8232': 'MSP430F67781A', '8233': 'MSP430F67791A', 'None': 'None'}

    data = f'{m_id} {tmpSend[0]}'
    crc = crc16(bytearray.fromhex(data))
    data = f'{data} {crc}'
    descriptor = count_def(m_class.updateTest(data), 1)
    try:
        hardware = idHardware[descriptor]
    except KeyError:
        hardware = None

    if hardware:
        for i in range(1, 5):
            data = f'{m_id} {tmpSend[i]}'
            crc = crc16(bytearray.fromhex(data))
            data = f'{data} {crc}'
            vector[i - 1] = count_def(m_class.getVectors(data), 1)
            result_vector.append(vector[i - 1])

        print(f'\n Дескриптор : {descriptor}\n',
              f'Микроконтроллер : {hardware}\n',
              f'Обновление доступно!\n\n',
              "================== Вектора прерываний ==================\n\n",
              f'0F1C0h : {result_vector[0]}\n',
              f'0F1D0h : {result_vector[1]}\n',
              f'0F1E0h : {result_vector[2]}\n',
              f'0F1F0h : {result_vector[3]}\n\n',
              f'Для дальнейшего обновления проверьте файл "firmware.txt" в папке update.\n',
              )
    else:
        print(f'Дескриптор : {descriptor}\n',
              f'Обновление не доступно....\n'
              )


def saveInfoFiles(tmp1, tmp2, tmp3, tmp4):
    dictInfo = [
                'Класс точности А+', 'Класс точности R+', 'Номинальное напряжение', 'Номинальный ток', 'Версия ПО',
                'CRC ПО', 'Вариант исполнения', 'Число направлений', 'Температурный диапазон',
                'Учет профиля средних мощностей',
                'Число фаз', 'Постоянная счетчика', 'Суммирование фаз', 'Тарификатор', 'Тип счетчика',
                'Номер варианта исполнения',
                'Память №3', 'Модем PLC', 'Модем GSM', 'Оптопорт', 'Интерфейс 1', 'Внешнее питание',
                'Эл.пломба верхней крышки',
                'Флаг наличия встроенного реле', 'Флаг наличия подсветки ЖКИ',
                'Флаг потарифного учета максимумов мощности',
                'Флаг наличия эл.пломбы защитной крышки', 'Интерфейс 2', 'Встроенное питание интерфейса 1',
                'Контроль ПКЭ', 'Пофазный учет энергии А+', 'Флаг измерения тока в нуле',
                'Флаг расширенного перечня массивов',
                'Флаг протокола IEC 61107', 'Модем PLC2', 'Флаг наличия профиля 2',
                'Флаг наличия пломбы модульного отсека',
                'Флаг переключения тарифов внешним напряжением', 'Реле управ-ния внешн.устр-ми откл. нагрузки',
                'Постоянная имп. и оптических выходов', 'Флаг измерения провалов и перенапряжений',
                'Флаг тарифного учета R1-R4',
                'Флаг КПК', 'Флаг массива профилей'
                ]
    info = dict(zip(dictInfo, tmp4))
    with open(f'{tmp1}_Info.txt', 'w+') as file:
        file.write(
            "============== Служебная информация ================\n\nСерийный номер : " + str(tmp1) +
            "\nДата выпуска : " + str(tmp2) + "\nСетевой адрес : " + str(tmp3) + "\n")
        for key, v in info.items():
            file.write(f'{key} : {v}\n')


def getInfo():
    tmpSend = ['08 05', '08 00', '08 01 00']

    data = f'{m_id} {tmpSend[0]}'
    crc = crc16(bytearray.fromhex(data))
    data = f'{data} {crc}'
    getSerial = count_def(m_class.getId(data), 1)

    data = f'{m_id} {tmpSend[1]}'
    crc = crc16(bytearray.fromhex(data))
    data = f'{data} {crc}'
    getNumber, getWork = count_def(m_class.getNumData(data), 2)

    data = f'{m_id} {tmpSend[2]}'
    crc = crc16(bytearray.fromhex(data))
    data = f'{data} {crc}'
    getByte = count_def(m_class.getVariant(data), 1)

    return list_info(getNumber, getSerial, getWork, getByte)


def list_info(serial_num, addr, work, var_byte):
    print('\n========= Служебная информация ===============\n')
    print(f'Серийный номер : {serial_num}')
    print(f'Дата выпуска : {work}')
    print(f'Сетевой адрес : {addr}')
    print(f'Версия ПО : {var_byte[4]}')
    print(f'CRC ПО : {var_byte[5]}')
    print(f'Вариант исполнения : {var_byte[6]}')
    print(f'Класс точности А+ : {var_byte[0]}')
    print(f'Класс точности R+ : {var_byte[1]}')
    print(f'Номинальное напряжение : {var_byte[2]}')
    print(f'Номинальный ток : {var_byte[3]}')
    print(f'Число направлений : {var_byte[7]}')
    print(f'Температурный диапазон : {var_byte[8]}')
    print(f'Учет профиля средних мощностей : {var_byte[9]}')
    print(f'Число фаз : {var_byte[10]}')
    print(f'Постоянная счетчика : {var_byte[11]}')
    print(f'Суммирование фаз : {var_byte[12]}')
    print(f'Тарификатор : {var_byte[13]}')
    print(f'Тип счетчика : {var_byte[14]}')
    print(f'Номер варианта исполнения : {var_byte[15]}')
    print(f'Память №3 : {var_byte[16]}')
    print(f'Модем PLC : {var_byte[17]}')
    print(f'Модем GSM : {var_byte[18]}')
    print(f'Оптопорт : {var_byte[19]}')
    print(f'Интерфейс 1: {var_byte[20]}')
    print(f'Внешнее питание : {var_byte[21]}')
    print(f'Эл.пломба верхней крышки : {var_byte[22]}')
    print(f'Флаг наличия встроенного реле : {var_byte[23]}')
    print(f'Флаг наличия подсветки ЖКИ : {var_byte[24]}')
    print(f'Флаг потарифного учета максимумов мощности : {var_byte[25]}')
    print(f'Флаг наличия эл.пломбы защитной крышки : {var_byte[26]}')
    print(f'Интерфейс 2 : {var_byte[27]}')
    print(f'Встроенное питание интерфейса 1 : {var_byte[28]}')
    print(f'Контроль ПКЭ : {var_byte[29]}')
    print(f'Пофазный учет энергии А+ : {var_byte[30]}')
    print(f'Флаг измерения тока в нуле : {var_byte[31]}')
    print(f'Флаг расширенного перечня массивов : {var_byte[32]}')
    print(f'Флаг протокола IEC 61107 : {var_byte[33]}')
    print(f'Модем PLC2 : {var_byte[34]}')
    print(f'Флаг наличия профиля 2 : {var_byte[35]}')
    print(f'Флаг наличия пломбы модульного отсека : {var_byte[36]}')
    print(f'Флаг переключения тарифов внешним напряжением : {var_byte[37]}')
    print(f'Реле управ-ния внешн.устр-ми откл. нагрузки : {var_byte[38]}')
    print(f'Постоянная имп. и оптических выходов : {var_byte[39]}')
    print(f'Флаг измерения провалов и перенапряжений : {var_byte[40]}')
    print(f'Флаг тарифного учета R1-R4 : {var_byte[41]}')
    print(f'Флаг КПК : {var_byte[42]}')
    print(f'Флаг массива профилей : {var_byte[43]}')
    print()
    return printable(serial_num, work, addr, var_byte)


def createParser():
    param = argparse.ArgumentParser()
    param.add_argument('-p', '--port')  # СОМ порт
    param.add_argument('-t', '--timeout', type=float, default=5)  # Время ожидания ответа
    param.add_argument('-i', '--number', type=int, default=0)  # Идентификатор счетчика
    param.add_argument('-s', '--systimeout', type=float, default=.5)  # Системный таймаут
    param.add_argument('-l', '--level', type=int, default=2)  # Уровень доступа (1-USER,2-ADMIN)
    param.add_argument('-pass', '--password', type=int, default=222222)  # Пароль пользователя
    return param


def passToArray(tmp):
    listIn = list(map(int, str(tmp)))
    listOut = ' '.join((format(listIn[i], '02X')) for i in listIn)
    return listOut


def get_time():
    now = datetime.datetime.now()
    comp_time = now.strftime('%d.%m.%y %H:%M:%S')
    comp_zone = now.strftime('%W')
    zone = 'Зима' if comp_zone == '01' else 'Лето'
    print(f'Время компьютера:  {comp_time} {zone}')
    print(f'Время счетчика:  ')


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    m_port = namespace.port
    m_timeout = namespace.timeout
    m_id = format(namespace.number, '02X')
    m_stimeout = namespace.systimeout
    m_level = format(namespace.level, '02X')
    m_pass = passToArray(namespace.password)

    try:
        ser = serial.Serial(
            port=m_port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=m_timeout
        )

        pOpen = f' Port {ser.port} opened ( {dt.now()} )' if ser.isOpen else f' Error to open port {ser.port}'

    except Exception as e:
        print(f'Port {m_port} no avilable... {e}')
        sys.exit()

    m_class = Mercury_230(m_id, ser, m_stimeout)

    main_menu_title = "=" * 48 + "\n"
    main_menu_title += "=               Конфигуратор 2.0               =\n"
    main_menu_title += "=" * 48 + "\n"
    main_menu_title += "-" * 48 + "\n"
    main_menu_title += pOpen + "\n"
    main_menu_title += "-" * 48 + "\n"
    main_menu_items = ["Служебная информация", "Обновление ПО", "Дата/Время", "Выход"]
    main_menu_cursor = "* "
    main_menu_cursor_style = ("fg_red", "bold")
    # main_menu_style = ("bg_black", "fg_blue")
    main_menu_exit = False

    main_menu = TerminalMenu(menu_entries=main_menu_items,
                             title=main_menu_title,
                             menu_cursor=main_menu_cursor,
                             menu_cursor_style=main_menu_cursor_style,
                             # menu_highlight_style=main_menu_style,
                             cycle_cursor=True,
                             clear_screen=True)

    edit_menu_title = "  Обновление ПО счетчика\n"
    edit_menu_items = ["Проверить возможность обновления", "Обновить", "Назад"]
    edit_menu_back = False
    edit_menu = TerminalMenu(edit_menu_items,
                             edit_menu_title,
                             main_menu_cursor,
                             main_menu_cursor_style,
                             # main_menu_style,
                             cycle_cursor=True,
                             clear_screen=True)

    while not main_menu_exit:
        main_sel = main_menu.show()
        if main_sel == 1:  # Обновление ПО
            while not edit_menu_back:
                edit_sel = edit_menu.show()
                if edit_sel == 0:  # Проверить возможность обновления
                    testUpdate()
                    t = backToMenu()
                    time.sleep(t)
                elif edit_sel == 1:  # Обновить ПО счетчика
                    updateFirmware()
                    t = backToMenu()
                    time.sleep(t)

                elif edit_sel == 2:  # Назад (из меню "Обновление ПО")
                    edit_menu_back = True
                    print("Back Selected")
            edit_menu_back = False

        elif main_sel == 0:  # Служебная информация
            testChannel()
            openSession()
            t = getInfo()
            time.sleep(t)

        elif main_sel == 2:  # Профиль мощности
            get_time()
            time.sleep(15)

        elif main_sel == 3:  # Выход
            ser.close()
            main_menu_exit = True
    raise SystemExit
