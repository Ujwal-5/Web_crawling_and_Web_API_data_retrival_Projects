import requests
import json

def hit_moniter_api(file_name):
    conf = open(file_name) 
    conFile = json.load(conf)   
    try:
        requests.get('http://3.254.232.204/DEV2.0/Configrator/monitor.php?Browser='+conFile['Browser']+'&Service='+conFile['Service']+'&Machine_Name='+conFile['Machine_Name'])    
    except: pass