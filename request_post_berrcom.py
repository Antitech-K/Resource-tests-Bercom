#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import time
import json

resault_post= ''

url = 'http://localhost:3001/measure'
body = {}
headers = {'content-type': 'application/json'}
try:
    measure = requests.post(url, data=json.dumps(body), headers=headers, timeout=7)
    resault_post = measure.text
    file = open ('./clipboard.txt', 'w')
    file.write(resault_post)
    file.close()
    
except requests.exceptions.ReadTimeout:
    print ("Какие-то проблемы с прибором. Программа отменена.")
    resault_post = 'error'
    pass

time.sleep(2)
exit()