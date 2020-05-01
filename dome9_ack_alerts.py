import requests
import json

API_ID = "" # API ID from Dome9
API_SECRET = "" #API Secret from Dome9
API_ENDPOINT = "https://api.dome9.com/v2"
ACK_COMMENT = "[BATCH ACKNOWLEDGED]"

headers = {
    "Content-type": "application/json",
    "Accept": "application/json"
}
# We only want to find un-acknowledged alerts

search_params = {
    "pageSize": 100,
    "filter": {
        "fields": [
            {
                "name": "acknowledged",
                "value": "false"
            }
        ]
    }
}

# Search without ID for first page, use searchAfter for subsequent
# then if len findings < 100 - don't request another page


r = requests.post(API_ENDPOINT + "/Compliance/Finding/search", 
    params={}, data=json.dumps(search_params), headers = headers, auth=(API_ID, API_SECRET))

res = json.loads(r.text)
print("[INFO] - Found a total of " + str(res['totalFindingsCount']))

ack = {
    "acknowledged": "true",
    "comment": ACK_COMMENT
}

while 'searchAfter' in res.keys() and res['searchAfter'] != None:
    for f in res['findings']:
        print("[INFO] - ACKing event ID" + f['id'])
        r = requests.put(API_ENDPOINT + "/Compliance/Finding/" + f['id'] + "/acknowledge",
            headers=headers, auth=(API_ID, API_SECRET), data=json.dumps(ack))
        if r.status_code != 200:
            print("[ERROR] - Request failed. Error received: [" + str(r.status_code) + "] " + r.reason)
            exit()
    search_params['searchAfter'] = res['searchAfter']
    
    r = requests.post(API_ENDPOINT + "/Compliance/Finding/search", 
        params={}, data=json.dumps(search_params), headers = headers, auth=(API_ID, API_SECRET))
    res = json.loads(r.text)

print("[INFO] Finished!")
         
    




#r = requests.put(API_ENDPOINT + "/Compliance/Finding/" + res['findings'][0]['id'] + "/acknowledge",
#headers=headers, auth=(API_ID, API_SECRET), data=json.dumps(ack))
#print(r.text)