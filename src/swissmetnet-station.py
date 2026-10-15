from pystac_client import Client
import pandas as pd

cat = Client.open("https://data.geo.admin.ch/api/stac/v1/")

# Collection = automatic weather stations; item = station code in lowercase
item = cat.get_collection("ch.meteoschweiz.ogd-smn").get_item("sma")
for k in item.assets:          # look at what's available
    print(k)

# d = daily, historical = long series (alternatives: recent, now)
hrefs = [a.href for k, a in item.assets.items() if "_d_historical" in k]

df = pd.concat(
    pd.read_csv(h, sep=";", encoding="cp1252",
                parse_dates=["reference_timestamp"], dayfirst=True)
    for h in hrefs
).set_index("reference_timestamp")

# tre200d0 = daily mean air temperature at 2 m, rre150d0 = daily precipitation
annual = df["tre200d0"].resample("YE").mean()
annual.plot(title="Zürich-Fluntern: annual mean temperature (°C)")
