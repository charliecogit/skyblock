import requests
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 10_000)
from copy import deepcopy
import time

params = {'from': int(time.time()-24*20*3600)*1000}
items = requests.get("https://api.slothpixel.me/api/skyblock/items").json()
auctions = requests.get("https://api.slothpixel.me/api/skyblock/auctions/PIGMAN_SWORD",
                        params=params).json()


def flatten(data, indices, res, index_in):
    index = deepcopy(index_in)
    for k, v in data.items():
        if isinstance(v, dict):
            flatten(v, indices, res, index + [k])
        else:
            indices.append(tuple(index + [k]))
            res.append(v)


res = []
indices = []
flatten(auctions, indices, res, [])

index = pd.MultiIndex.from_tuples(indices)

df = pd.DataFrame(res, index=index, columns=['enchantment'])
idx = pd.IndexSlice
df2 = df.xs('enchantments', level=4, drop_level=False)
df3 = df2.droplevel((0, 2, 3, 4))
df4 = df3.unstack(level=-1)
df4.fillna(value=0, inplace=True)
df4.index = pd.to_datetime(df4.index, unit='ms', utc=True)
df4.index = df4.index.tz_convert('US/Eastern')
df4['time'] = df4.index.strftime('%b %d %y %r')
df4 = df4.set_index('time')
df4 = df4.drop(0, level=1, axis=1)
print(df4)
