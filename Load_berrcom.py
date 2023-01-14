#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os   
import requests
import json
import time
import logging                                                           


down_rele = os.system("/opt/RODOS4/RODOS4 --id 4798 --c8 0")

def measure():
    resault_post= ''
    url = 'http://localhost:3001/measure'
    body = {}
    headers = {'content-type': 'application/json'}
    try:
        measure_d = requests.post(url, data=json.dumps(body), headers=headers, timeout=7)
        os.system("/opt/RODOS4/RODOS4 --id 4798 --c9 128")
        time.sleep(1)
        os.system("/opt/RODOS4/RODOS4 --id 4798 --c9 0")        
        resault_post = measure_d.text
        file = open ('./clipboard.txt', 'w')
        file.write(resault_post)
        file.close()
        return
    
    except requests.exceptions.ReadTimeout:
        print ("Какие-то проблемы с прибором. Программа отменена.")
        resault_post = 'error'
        file = open ('./clipboard.txt', 'w')
        file.write(resault_post)
        file.close()
        return
        

def shutdown_rodos():
    for x in range(16):
        a = "/opt/RODOS4/RODOS4 --id 4798 --c" +str(x) + " 0"
        time.sleep(0.2)
        os.system(a)
    return "Усё"

#проверка подключения драйвер теста
status = requests.get("http://localhost:3001/status")
if status.text =="":
    down_rele
    print ("Не запущен тест-драйвер. Программа отменена.")
    exit()
elif status.text == '{"result":"ONLINE"}':
    requests.get("http://localhost:3001/start")
    time.sleep(1)
    status
    if status.text != '{"result":"READY"}':
        print("Что-то пошло не так, я выключаюсь")
        exit()

#включение "чайника"
os.system("/opt/RODOS4/RODOS4 --id 4798 --c8 128")
print ("нагрев включен, время ожинания около 3 мин")
time.sleep (180)


a = 0
while a != 50000:
    print("Запуск измерений.")
    measure()
    time.sleep(1)
    status
    if  status.text == '{"result":"READY"}':
        file = open ('./clipboard.txt', 'r')
        resault_measure = file.read()
        file.close()
        if resault_measure.find('sys"') != 21:
            print("Прибор не выдал требуемые результаты.")
            file = open ('./error.txt', 'a')
            resault_measure = file.read()
            file.close()
        elif resault_measure.find('sys"') == 21:
            file = open ('./result.txt', 'r')
            number = file.read()
            file.close()
            file = open ('./result.txt', 'w')
            number = int (number) + 1
            file.write(str (number))
            file.close()
            print("Кол-во измерений =", number)
    a += 1

exit()