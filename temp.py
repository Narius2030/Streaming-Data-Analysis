import requests
import json

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMzE0OGE4OWJhZTczOGQ1ZDRiYzVkMGYwYzllODI3MyIsIm5iZiI6MTcxOTQ4NDczMy4wMDgxMDMsInN1YiI6IjY1ZDIxYzcxNmVlY2VlMDE4YTM5MmZkNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4rj8zbqb7WXWJXSMx0ByPVOwxelrxVM_uh2xGNiiOaU"
}

response = requests.get(url, headers=headers)
with open('./test.json', 'w') as file:
        json.dump(response.json(), file)

# print(response.text)