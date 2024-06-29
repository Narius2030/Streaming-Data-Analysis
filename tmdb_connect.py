import datetime
import json
import sys
import requests
import socket
import pandas as pd
from tqdm import tqdm


# params = {
#     'include_adult': 'false',
#     'include_video': 'false',
#     'language': 'en-US',
#     'page': page,
#     'sort_by': 'popularity.desc'
# }
# headers = {
#     "accept": "application/json",
#     "Authorization": f"Bearer {bearer_token}"
# }

# Replace with your actual Twitter API credentials (keep these secret)
with open('./config.json', mode='r') as f:
    json_obj = json.loads(f.read())
    api_key = json_obj['API_KEY']
    bearer_token = json_obj['BEARER_TOKEN']
    params = json_obj['params']
    headers = json_obj['headers']

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

def get_response_json(url, params, headers, data, verbose:bool=True) -> dict:
    search_url = create_url(url, params, verbose)
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
    
def get_response_csv(data:dict, save:bool=False, path:str=None):
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

def get_movies(url, params, headers, resp) -> dict:
    for page in tqdm(range(1, 6)):
        params['page'] = page
        resp = get_response_json(url, params, headers, resp, verbose=False)
    return resp
        
if __name__ == "__main__":
    TCP_IP = "localhost"
    TCP_PORT = 65432
    conn = None
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        print("Waiting for TCP connection...")
        conn, addr = s.accept()

        with conn:
            print("Connected... Starting getting movies.")
            while True:
                recieve_data = conn.recv(4096)
                if not recieve_data:
                    break
                print(recieve_data.decode('utf-8'))
                url = "https://api.themoviedb.org/3/discover/movie?"
                resp = {'results': []}
                movies_data = get_movies(url, params, headers, resp)
                encoded_movies_data = json.dumps(movies_data).encode()
                conn.send(encoded_movies_data)
                print("Number of bytes: ", sys.getsizeof(encoded_movies_data))
            print("Connected... got movies successfully.")
    
    # with open('./data/tmdb.json', 'w') as f:
    #     json.dump(resp, f)
    # with open('./data/tmdb.json', 'r') as f:
    #     data = json.load(f)
    #     get_response_csv(data, save=True, path="./data/tmdb.csv")
