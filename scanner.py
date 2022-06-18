import re
import socket
import threading
import time

from logs import logger


class Data:
    """
    Класс для хранения полученных данных
    """
    def __init__(self):
        self.__data = {}

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, result):
        self.__data[result[0]] = result[1]


def port_scanner(ip: str, port: int, data_obj: Data) -> None:
    """Проверка одного порта"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    try:
        connect = sock.connect((ip, port))
        data_obj.data = port, 'open'
        sock.close()
    except Exception:
        data_obj.data = port, 'close'
        sock.close()


def port_scanner_loop(request, ip: str, start_port: int, end_port: int, data_obj: Data) -> dict:
    """Цикл для проверки всех портов в заданном диапазоне"""
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=port_scanner, args=(ip, port, data_obj))
        thread.start()
    time.sleep(0.5)
    try:
        logger.info(f'Ports are checked. request: {request} Result: {data_obj.data}')
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
                logger.warning(f'End port is less then start port. Automatically switched values. request: {request}')
                port_start, port_end = port_end, port_start
            logger.info(f'Checking ports by ip: {ip}, request: {request}')
            data_obj = Data()
            return port_scanner_loop(request, ip, port_start, port_end, data_obj)
        else:
            raise ValueError
    except ValueError:
        return {'Error': f'Incorrect Values'}


