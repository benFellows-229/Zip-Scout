
import http.client

conn = http.client.HTTPSConnection("realty-mole-property-api.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "e375110e3cmshaf77ee007d8b4f6p1b083fjsn1e170d0c3e46",
    'X-RapidAPI-Host': "realty-mole-property-api.p.rapidapi.com"
    }

conn.request("GET", "/zipCodes/29611", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
