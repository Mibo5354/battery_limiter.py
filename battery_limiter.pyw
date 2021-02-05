import PySimpleGUIWx as sg
import psutil, time
import threading

#Import config
from configparser import ConfigParser
config = ConfigParser(interpolation=None)
config.read('config.ini')

if config.get('main', 'protocol')=="http":
    #Use unsecured web requests
    import requests
elif config.get('main', 'protocol')=="mqtt":
    #Use TLS secured MQTT
    import paho.mqtt.publish as publish
    import certifi

limiter = True

def monitor():
    while True:
        global limiter
        while limiter:
            print("Limiter running")
            global percent
            battery = psutil.sensors_battery()
            plugged = battery.power_plugged
            percent = int(battery.percent)
            
            topic = config.get('main', 'topic')
            onVal = config.get('main', 'onValue')
            offVal = config.get('main', 'offValue')
            host = config.get('main', 'hostname')
            mport = config.getint('main', 'port')
            uname = config.get('main', 'username')
            passwd = config.get('main', 'password')
            min = config.getint('main', 'startCharge')
            max = config.getint('main', 'stopCharge')
            cert = config.get('main', 'tls')
            if config.get('main', 'protocol')=="mqtt":
                if cert == "certifi":
                    cert = {'ca_certs':certifi.where()}
                elif cert != "none":
                    cert = {'ca_certs':cert}
            
            if percent < min:
              if plugged == False:
                #run turn on switch
                if config.get('main', 'protocol')=="http":
                    requests.get(config.get('main', 'httpOn'))
                elif config.get('main', 'protocol')=="mqtt":
                    publish.single(topic, onVal, hostname=host, port=mport, auth = {'username':uname, 'password':passwd}, tls = cert)
                print("turn on charger")
            elif percent > max:
              if plugged == True:
                #run turn off switch
                if config.get('main', 'protocol')=="http":
                    requests.get(config.get('main', 'httpOff'))
                elif config.get('main', 'protocol')=="mqtt":
                    publish.single(topic, offVal, hostname=host, port=mport, auth = {'username':uname, 'password':passwd}, tls = cert)
                print("turn off charger")
            time.sleep(10)
def tray():
    menu_def = ['UNUSED', ['Disable Limiter', 'Exit']]

    tray = sg.SystemTray(menu=menu_def, filename=r'battery.png')

    tray.ShowMessage('Starting', 'Now Starting the Battery Limiter')

    while True:
        global limiter
        event = tray.Read()
        if event == 'Exit':
            break
        elif event == 'Disable Limiter':
            limiter = False
            tray.ShowMessage('Battery Limiter', 'Disabled')
            menu_def = ['UNUSED', ['Enable Limiter', 'Exit']]
            tray.Update(menu=menu_def, filename=r'battery.png')
        elif event == 'Enable Limiter':
            limiter = True
            tray.ShowMessage('Battery Limiter', 'Enabled')
            menu_def = ['UNUSED', ['Disable Limiter', 'Exit']]
            tray.Update(menu=menu_def, filename=r'battery.png')
        #tray.ShowMessage('Event', '{}'.format(event))
        print("Battery is at " + str(percent))
        print("Limiter="+str(limiter))
if __name__ == "__main__":   
    x = threading.Thread(target=monitor,daemon=True)
    x.start()   
    y = threading.Thread(target=tray)
    y.start()


