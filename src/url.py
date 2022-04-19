import requests

class URL:

    def __init__(self, url):
        self.url = url
        r = requests.get(url)
        self.status_code = r.status_code

    def __str__(self):
        return f"{self.url} with response {self.status_code}"
        