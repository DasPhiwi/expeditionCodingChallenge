import json
import requests

result = requests.get("https://rvj6rnbpxj.execute-api.eu-central-1.amazonaws.com/prod/building?interval=60&begin-timestamp=1635869520&end-timestamp=1635894000")

print(result)