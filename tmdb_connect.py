import datetime
import json
import requests
import socket
import pandas as pd
# from tqdm import tqdm

# Replace with your actual Twitter API credentials (keep these secret)
with open('./config.json', mode='r') as f:
    json_obj = json.loads(f.read())
    api_key = json_obj['API_KEY']
    bearer_token = json_obj['BEARER_TOKEN']

def create_url(url, params, verbose:bool=True) -> str:
    """params: [(include_adult, false),
                (include_video, false),
                (language, en-US),
                (page, 1),
                (sort_by, popularity.desc)]
    """
    query_url = url + '?' + '&'.join([str(k) + '=' + str(v) for k, v in params.items()])
    if verbose:
        print('Query String: ', query_url)
    return query_url

def get_response(url, params, headers, data, verbose:bool=True) -> dict:
    search_url = create_url(url, params)
    resp = requests.get(search_url, headers=headers, stream=True)
    if verbose:
        print(f"---> Endpoint Response Code: {str(resp.status_code)}")
    
    if resp.status_code != 200:
        raise Exception(resp.status_code, resp.text)

    resp_json = resp.json()
    data.update({'page': resp_json['page'], 
                'total_pages':resp_json['total_pages'], 
                'total_results':resp_json['total_results']})
    for res in resp_json['results']:
        data['results'].append(res)
        
    return data
    
def get_movies_data(data:dict, save:bool=False, path:str=None):
    results = data['results']
    columns = [k for k in results[0].keys()]
    content = []
    
    for res in results:
        temp = [v for _, v in res.items()]
        content.append(temp)
        
    df = pd.DataFrame(columns=columns, data=content)
    if save:
        df.to_csv(path)
    return df
        
if __name__ == "__main__":
    TCP_IP = "localhost"
    TCP_PORT = 9009
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection...")
    conn, addr = s.accept()
    print("Connected... Starting getting movies.")
    
    
    url = "https://api.themoviedb.org/3/discover/movie?"
    resp = {'results': []}
    for page in range(1, 11):
        params = {
            'include_adult': 'false',
            'include_video': 'false',
            'language': 'en-US',
            'page': page,
            'sort_by': 'popularity.desc'
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }
        resp = get_response(url, params, headers, resp)
    
    with open('./data/tmdb.json', 'w') as f:
        json.dump(resp, f)
    with open('./data/tmdb.json', 'r') as f:
        data = json.load(f)
        get_movies_data(data, save=True, path="./data/tmdb.csv")
