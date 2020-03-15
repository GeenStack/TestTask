from config import tasks_url, users_url
import requests
from time import sleep


#Solved with ru.stackoverflow.com/questions/816815/
def get_data_from_api(api_url):
	while True:
		try:
			response = requests.get(api_url)
			if (response.status_code != 200):
				error_log = 'Failed to access ' + api_url
				error_log +=' Server response status code: ' + str(response.status_code)
				print(error_log)
				continue

			return response.json()

		except requests.ConnectionError:
			print('ConnectionError. Check your connection to internet')
			sleep(5)

