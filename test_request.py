import requests
import json

url = 'http://127.0.0.1:8000/webhook'
# heroku_url = "https://blooming-thicket-47680.herokuapp.com/signals" # webhook
sample_data = {
            'ACTION': 'OPEN LONG',
            'AMOUNT_COIN' : '100.00',
            'LEV' : '20',
            'SYMBOL' : 'ADABUSD'
            }

sample_data = json.dumps(sample_data)

#x = requests.post(url, data = ข้อมูลตัวอย่าง)
x = requests.post(url, data = sample_data)

print(x.text)