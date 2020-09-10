#!/usr/bin/env python3
import pandas as pd
import pickle
from os import path
import math
print(pd.__version__)
router = '00:04:4b:e4:08:c5'

result = {}

def process(f, r):
  r[f] = {}
  df=pd.read_csv(f)
  for index, row in df.iterrows():
    d=row.to_dict()
    #print(d)
    size = 0.0
    if not math.isnan(float(d['UDP.Length'])):
       size = float(d['UDP.Length'])
    elif not math.isnan(float(d['Payload.Length'])):
       size = float(d['Payload.Length'])
    if d['Ethernet.SrcMAC'] == router: #download
       addr = 'IPv4.SrcIP'
       direction = 'dw'
       mac = d['Ethernet.DstMAC']
       ip = d['IPv4.DstIP']
    else:
       addr = 'IPv4.DstIP'
       direction = 'up'
       mac = d['Ethernet.SrcMAC']
       ip = d['IPv4.SrcIP']
    if mac not in r[f]:
        r[f][mac] = {'ip': ip, 'destination': {}, 'count_destination': 0}
    if d[addr] not in r[f][mac]['destination']:
        r[f][mac]['destination'][d[addr]] = {'dw' : 0.0, 'up' : 0.0}
    r[f][mac]['destination'][d[addr]][direction] =\
            r[f][mac]['destination'][d[addr]][direction] + size
  for k in r[f].keys():
     r[f][k]['count_destination'] = len(r[f][k]['destination'].keys())

if path.exists("traces.pickle"):
  with open('traces.pickle', 'rb') as handle:
    result = pickle.load(handle)
else:
  #process('test.csv', result)
  process('trace-20200802081606.pcap.csv', result)
  process('trace-20200802081606.pcap.csv', result)
  process('trace-20200805081601.pcap.csv', result)
  process('trace-20200806080026.pcap.csv', result)
  process('trace-20200807080028.pcap.csv', result)
  process('trace-20200808080027.pcap.csv', result)
  process('trace-20200809080034.pcap.csv', result)
  process('trace-20200810080027.pcap.csv', result)
  process('trace-20200811080039.pcap.csv', result)

  with open('traces.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(result)
for f in result.keys():
  for d in result[f].keys():
    print("{0} {1} {2}".format(f,d,result[f][d]['count_destination']))
