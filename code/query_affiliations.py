import http.client, urllib.request, urllib.parse, urllib.error, base64
import json,ast
import os
from tqdm import tqdm

cur_path = os.getcwd()
file_path = os.path.relpath('..//data//', cur_path)

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '1f346730bfc94341b3ff286d4dbfa34f'
}

params = urllib.parse.urlencode({
    # Request parameters
    'count' : 1000000000,
    'attributes': 'AfN,CC,DAfN,Id,ECC,PC'
})

def get_data():
    
    file_name = 'MAG_Affiliation.json'
    try:
        conn = http.client.HTTPSConnection('api.labs.cognitive.microsoft.com')
        conn.request("GET", "/academic/v1.0/evaluate?expr=Id>0)&%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data_dict = json.loads(data)
        with open(file_name, 'w') as f:
            json.dump(data_dict, f, indent=4)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
get_data()
# expr=And(Composite(C.CN='"+conf+"'),Y>=2014,Pt='3')