import socket
import threading
import time


from logs import logger

data = {}


def update_data(port: int, state: str) -> None:
    """Добавление результата проверки порта в словарь data"""
    data[port] = state


def port_scanner(ip, port) -> None:
    """Проверка одного порта"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    try:
        connect = sock.connect((ip, port))
        update_data(port, 'open')
        sock.close()
    except Exception:
        update_data(port, 'close')


def port_scanner_loop(ip: str, start_port: int, end_port: int) -> dict:
    """Цикл для проверки всех портов в заданном диапазоне"""
    for i in range(start_port, end_port + 1):
        thread = threading.Thread(target=port_scanner, args=(ip, i))
        thread.start()
    time.sleep(0.1)
    try:
        logger.info('Ports are checked')
        return data
    except Exception:
        logger.error('Check error')
        return {'Error': 'Check process error'}


def get_data(request):
    """Обработка запроса"""
    try:
        ip = request.match_info['ip']
        port_start, port_end = int(request.match_info['port_start']), int(request.match_info['port_end'])
        if port_start > port_end:
            logger.warning('End port is less then start port. Automatically switched values.')
            port_start, port_end = port_end, port_start
        logger.info(f'Checking ports by ip: {ip}')
        return port_scanner_loop(ip, port_start, port_end)
    except TypeError('post_start, port_end must be int'):
        return {'Error': 'post_start, port_end must be int'}
    except ValueError('Incorrect Values'):
        return {'Error': 'Incorrect Values'}