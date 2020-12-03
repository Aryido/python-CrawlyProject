import time
import pandas as pd
import json
import requests

token = "xq_a_token=b2f87b997a1558e1023f18af36cab23af8d202ea"
finance_indicator_url = "https://stock.xueqiu.com/v5/stock/finance/cn/indicator.json?symbol="

finance_indicator_url_us = "https://stock.xueqiu.com/v5/stock/finance/us/indicator.json?symbol="

f10_indicator_url = "https://stock.xueqiu.com/v5/stock/f10/cn/indicator.json?symbol="
f10_indicator_url_us = "https://stock.xueqiu.com/v5/stock/f10/us/indicator.json?symbol="


def fetch(url):
    HEADERS = {'Host': 'stock.xueqiu.com',
               'Accept': 'application/json',
               'Cookie': token,
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)


def indicator(symbol, count, country):
    if country == 'us':
        url = finance_indicator_url_us + symbol
    else:
        url = finance_indicator_url + symbol

    url = url + '&type=Q4' + '&count=' + str(count)
    return fetch(url)


def f10_indicator(symbol, count, country):
    if country == 'us':
        url = f10_indicator_url_us + symbol
    else:
        url = f10_indicator_url + symbol

    url = url + '&count=' + str(count)
    return fetch(url)


a_country = 'cn'
#a_country = 'us'

annal_count = 5
file_name = '{0}_stock_list.txt'.format(a_country)

all_df = None

with open(file_name) as f:
    lines = f.readlines()
    for line in lines[1:]:
        try:
            stock = line.split(',')[1].strip(' \n')
            res1 = indicator(stock, 5, country=a_country)
            res2 = f10_indicator(stock, 5, country=a_country)

            name = res1['data']['quote_name']
            cols = ['stock', 'name']
            roe_list = []
            for i in range(annal_count):
                if a_country == 'us':
                    roe = res1['data']['list'][i]['roe_avg'][0]
                else:
                    roe = res1['data']['list'][i]['avg_roe'][0]
                roe_list.append(roe)
                cols.append(res1['data']['list'][i]['report_name'])
            pe = res2['data']['items'][0]['pe_ttm']
            pb = res2['data']['items'][0]['pb']
            cols += ['pe_ttm', 'pb']

            row = [stock] + [name] + roe_list + [pe] + [pb]
            df = pd.DataFrame([row], columns=cols)

            if all_df is None:
                all_df = pd.DataFrame(columns=cols)
            all_df = all_df.append(df)
            print(all_df.tail())
            time.sleep(1)
        except:
            pass
    all_df.to_csv('{0}_roe_pe_pb_900.csv'.format(a_country))
