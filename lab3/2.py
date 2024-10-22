import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts')

posts = response.json()
