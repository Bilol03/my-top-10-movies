
import requests

title = "matrix"
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjgxZWMyYzQzODIwZWZlMDlhZDgxZmEwM2JjMmVlYiIsInN1YiI6IjY2MThjNjg0NmYzMWFmMDE0OTlhNWU0NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eJg4Kab1x0ynsUpteIZ1mxAclWc9rUWG1defHDL-5ts"  # Replace this with your actual API key from TMDb
url = f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}"

headers = {
    "accept": "application/json",
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print("Error:", e)
