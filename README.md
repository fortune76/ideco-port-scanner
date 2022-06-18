# ideco-port-scanner
Simple application for check tcp ports by ip.
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
