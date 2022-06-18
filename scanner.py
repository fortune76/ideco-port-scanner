import re
import socket
import threading
import time

from logs import logger


class Data:
    def __init__(self):
        self.__data = {}

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, result):
        self.__data[result[0]] = result[1]


def update_data(data_obj: Data, port: int, state: str) -> None:
    """Добавление результата проверки порта в словарь data"""
    data_obj.data = (port, state)


def port_scanner(ip: str, port: int, data_obj: Data) -> None:
    """Проверка одного порта"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    try:
        connect = sock.connect((ip, port))
        update_data(data_obj, port, 'open')
        sock.close()
    except Exception:
        update_data(data_obj, port, 'close')
        sock.close()


def port_scanner_loop(ip: str, start_port: int, end_port: int, data_obj: Data) -> dict:
    """Цикл для проверки всех портов в заданном диапазоне"""
    for i in range(start_port, end_port + 1):
        thread = threading.Thread(target=port_scanner, args=(ip, i, data_obj))
        thread.start()
    time.sleep(0.5)
    try:
        logger.info(f'Ports are checked. Result: {data_obj.data}')
        return data_obj.data
    except Exception:
        logger.error('Check error')
        return {'Error': 'Check process error'}


def get_data(request):
    """Обработка запроса"""
    try:
        ip = request.match_info['ip']
        ip_check = re.match("([0-9]{1,3}[\.]){3}[0-9]{1,3}", ip)
        if ip_check:
            port_start, port_end = int(request.match_info['port_start']), int(request.match_info['port_end'])
            if port_start > port_end:
                logger.warning('End port is less then start port. Automatically switched values.')
                port_start, port_end = port_end, port_start
            logger.info(f'Checking ports by ip: {ip}')
            data_obj = Data()
            return port_scanner_loop(ip, port_start, port_end, data_obj)
        else:
            raise ValueError
    except ValueError:
        return {'Error': 'Incorrect Values'}
