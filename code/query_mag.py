import http.client, urllib.request, urllib.parse, urllib.error, base64
import json,ast
import os
from tqdm import tqdm

cur_path = os.getcwd()
file_path = os.path.relpath('..//data//paper_data_mag//', cur_path)

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '1f346730bfc94341b3ff286d4dbfa34f'
}

params = urllib.parse.urlencode({
    # Request parameters
    'count' : 1000000000,
    'attributes': 'AA.AfId,AA.AfN,AA.AuId,AA.AuN,AA.S,AW,BT,BV,C.CId,C.CN,CC,CitCon,D,DN,DOI,ECC,F.FId,F.FN,FP,Id,Pt,RId,Ti,Y'
})

def get_data(conf):
    
    file_name = 'MAG_' + conf.upper() + '.json'
    try:
        conn = http.client.HTTPSConnection('api.labs.cognitive.microsoft.com')
        conn.request("GET", "/academic/v1.0/evaluate?expr=And(Composite(C.CN='"+conf+"'),Y>2017,Pt='3')&%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data_dict = json.loads(data)
        with open(file_path+"//"+file_name, 'w') as f:
            json.dump(data_dict, f, indent=4)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
conf_list = ['acl','emnlp','iccv','icml','iclr','cvpr','naacl','neurips']
for conf in tqdm(conf_list):
    get_data(conf)