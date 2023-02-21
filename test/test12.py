import requests

files = {
    "file": open(r"E:\下载\1.png", "rb")
}
response = requests.post("http://localhost:11451/test", files=files)
print(response.text)
