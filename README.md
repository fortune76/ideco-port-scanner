# ideco-port-scanner
Simple application for check tcp ports by ip.
# Задание

Требуется разработать web-приложение для сканирования открытых TCP портов удаленного хоста.
Приложение должно реализовать следующее REST API:

    * GET /scan/<ip>/<begin_port>/<end_port>

    Параметры:
        # ip - хост, который необходимо просканировать
        # begin_port - начала диапозона портов для сканирования
        # end_port - конец диапозона портов для сканирования

    Формат ответа:  [{"port": "integer", "state": "(open|close)"}]


Обработчик данного урла - запускает сканирование указанного хоста, и отдает информацию клиенту. В формате JSON (можно частями).
    


Требования к программе:

* Aiohttp, Python3.9 или выше;
* наличие логов работы приложения - входящие запросы, ошибки и т.д. Логирование необходимо производить в syslog.

Будет плюсом:

* наличие тестов (AioHTTPTestCase), не обязательно но желательно;
* готовый spec-файл для сборки RPM-пакета с программой.

Предпочтительные средства реализации:

* образ системы Fedora 35.

Результат:

* код, расположенный на git-репозитории (например, github).

### Installing:
First install venv.
```
sudo pip3 install virtualenv 
```
Next create venv in project directory
```
virtualenv venv 
```
Activate venv.
```
source venv/bin/activate
```
Install requirements
```
pip3 install -r requirements.txt
```
### How to use
Start application using command
```
python3 main.py
```
Logs are automatically stream to your terminal
Type HTTP GET /scan/<ip>/<begin_port>/<end_port>/ to your browser or Postman.
You will receive JSON response with port's status.  
