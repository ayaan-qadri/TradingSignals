import requests as rq
import json
import tkinter as tk
from tkinter import filedialog
import webbrowser


def req():

    header = {

        'Accept': "'text/html','application/xhtml+xml','application/xml;q=0.9','image/avif','image/webp','*/*;q=0.8'",
        'Accept-Encoding': "'gzip', 'deflate', 'br'",
        'Accept-Language': "'en-US','en;q=0.5'",
        'Connection': 'keep-alive',
        'Host': 'www.nseindia.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}

    r = rq.get(
        'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY', headers=header)
    print(r.ok)

    if r.ok:
        return r.json()
    else:
        return 'failed'


data = req()


def data_write():

    count = 0
    file_data = open('pcr_data.txt', 'w')
    dates = data['records']['expiryDates']

    for k in data['records']['data']:
        if k['expiryDate'] == dates[0]:
            CEio = k['CE']['openInterest']
            PEio = k['PE']['openInterest']
            pcr = 0
            IO_is = 1

            if CEio > 0:
                pcr = PEio/CEio
            else:
                IO_is = 0

            file_data.write(
                f"Expiry date: {k['expiryDate']}\nstrike price: {k['strikePrice']}\nCE OI: {CEio}\nPE OI: {PEio}\nSignle: ")
            if pcr >= 1 and IO_is:
                file_data.write(
                    f"***Buy***({pcr})\n\n------------------\n")
            else:
                file_data.write(
                f"\\\Sell\\\({pcr})\n\n------------------\n")
    file_data.close()


if data == 'failed':
    print('Try again')
else:
    data_write()
    webbrowser.open('pcr_data.txt', new=2)


