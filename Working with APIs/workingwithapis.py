import requests

response = requests.get("https://randomfox.ca/floof")

#print(response.status_code)
#print(response.text)
#print(response.json())

fox = response.json()

print(fox)
print(fox['image'])
print(fox['link'])