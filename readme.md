## battery_limiter.py
This is a python script to limit battery charging with a smart plug using http request or MQTT.

### Installing the script
Python 3 is required for this app.

After installing Python open a terminal/command prompt in the same directory of this app and install the dependencies using `pip install -U -r requirements.txt --user`

Rename `config.ini.template` to `config.ini`, modify settings at needed.

### Credits
##### Images
- Battery Icon - [Adrien Coquet](https://thenounproject.com/term/battery-indicator/1601217/) under Creative Commons License
##### Python Libraries
- [wxPython](https://pypi.org/project/wxPython/) under OSI Approved [wxWindows Library License](https://opensource.org/licenses/wxwindows.php)
- [PySimpleGUIWx](https://pypi.org/project/PySimpleGUIWx/) under LGPLv3+
- [psutil](https://pypi.org/project/psutil/) under  BSD License
- [requests](https://pypi.org/project/requests/) under Apache Software License (Apache 2.0)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) under OSI Approved (Eclipse Public License v1.0 / Eclipse Distribution License v1.0)
- [certifi](https://pypi.org/project/certifi/) under MPL-2.0