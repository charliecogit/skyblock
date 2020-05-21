from selenium import webdriver
import requests
import re
import pandas as pd
import plotly.express as px
import plotly.io as pio
import itertools as it
import numpy as np

pio.renderers.default = 'png'

class WebDriver:
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

df = None
items = requests.get("https://api.slothpixel.me/api/skyblock/items").json()
bazaar_items = []
for k, v in items.items():
    if v.get('bazaar'):
        bazaar_items.append(k)

for item in it.islice(bazaar_items,1):
    print(item)
# item = 'SPIDER_EYE'
    with WebDriver(webdriver.Safari()) as wd:
        wd.get(f"https://skyblock-tool.xyz/product.php?name={item}")
        data = wd.page_source



    dataloc = list(re.finditer('name: .*?,', data))
    start = dataloc[-1].start()
    length = data[dataloc[-1].end():].find('</script>')
    data_iter = re.finditer('"x":(.*?),"y":(.*?)}', data[start:start + length])
    time = []
    price = []
    for m in data_iter:
        time.append(m.group(1))
        price.append(m.group(2))

    if df is not None:
        df= df.append(pd.DataFrame({'item': item, 'type': 'sell', 'time': pd.to_datetime(time, utc=True, unit='ms'),
                       'price': price}))
    else:
        df = pd.DataFrame({'item': item, 'type': 'sell', 'time': pd.to_datetime(time, utc=True, unit='ms'),
                           'price': price})

    start = dataloc[-1].start()
    length = data[dataloc[-1].end():].find('</script>')
    data_iter = re.finditer('"x":(.*?),"y":(.*?)}', data[start:start + length])

    data_iter = re.finditer('"x":(.*?),"y":(.*?)}', data[dataloc[-2].end():dataloc[-1].start()])
    time = []
    price = []
    for m in data_iter:
        time.append(m.group(1))
        price.append(m.group(2))
    df = df.append(pd.DataFrame({'item': item, 'type': 'buy', 'time': pd.to_datetime(time, utc=True, unit='ms'),
                       'price': price}))

fig = px.line(df, x='time',y='price', color='type')
fig.show()
