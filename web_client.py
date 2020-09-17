#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:12:52 2020

@author: jp
"""
import http.client
import pprint

connection = http.client.HTTPConnection('192.168.1.19', 80, timeout=10)
connection.request("GET", "/")
response = connection.getresponse()
headers = response.getheaders()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint("Headers: {}".format(headers))


#%%


from lxml import html
import requests

page = requests.get('http://192.168.1.19')
tree = html.fromstring(page.content)

sensor = tree.xpath('//arduino_due/sensor[@type=\'analog\']/text()')
reading = tree.xpath('//arduino_due/sensor[@reading]/text()')

values = {}

for i in range(len(sensor)):
    values['S{}'.format(sensor[i])] = int(reading[i])
    
print(values)