# Description: This program will calculate the median value of house listings from a zillow api call
import http.client
import json

conn = http.client.HTTPSConnection("zillow56.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "e375110e3cmshaf77ee007d8b4f6p1b083fjsn1e170d0c3e46",
    'X-RapidAPI-Host': "zillow56.p.rapidapi.com"
    }

conn.request("GET", "/search?location=houston%2C%20tx", headers=headers)
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
