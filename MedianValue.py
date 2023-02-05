# Description: This program will calculate the median value of house listings from a zillow api call
import http.client
import json

conn = http.client.HTTPSConnection("zillow56.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "1d5c1f2561msh0af3408496e2673p1a6e6ajsnc23c8c34bca3",
    'X-RapidAPI-Host': "zillow56.p.rapidapi.com"
    }

conn.request("GET", "/search?location=Houston", headers=headers)
j = 0
res = conn.getresponse()
data = res.read()
foo = json.loads(data)
bar = foo.get("results")
price = 0
for i in range (len(bar)):
    price = price + bar[i].get("price")
    j += 1
average = price/j
print(average)
