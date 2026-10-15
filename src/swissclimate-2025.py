from pystac_client import Client
import pandas as pd

cat = Client.open("https://data.geo.admin.ch/api/stac/v1/")

item = cat.get_collection("ch.meteoschweiz.ogd-climate-scenarios-ch2025").get_item("sma")
for k in item.assets:
    print(k)   # e.g. ..._sma_tas_ref91-20.csv, ..._sma_tas_GWL2.0.csv

def load(level):
    href = next(a.href for k, a in item.assets.items() if f"_tas_{level}" in k)
    return pd.read_csv(href, sep=";", encoding="cp1252")

ref, gwl2 = load("ref91-20"), load("GWL2.0")
