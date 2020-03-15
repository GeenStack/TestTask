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


def users_list_created(users_list_returned_by_api):
	users_list = []
	for i in users_list_returned_by_api:
		new_user = {}
		new_user.update({"user_id":i["id"], "name":i["name"], "email":i["email"], 
						"completed_tasks":[], "lost_task":[]})
		
		users_list.append(new_user)
	return users_list

'''
def tasks_list_created(tasks_list_returned_by_api):
	tasks_list = []
	for i in tasks_list_returned_by_api:
'''

test_users_list = users_list_created(get_data_from_api(users_url))
for i in test_users_list:
	print(i)
	print('\n\n')
#TO DO
#Describe users
#  1. Form users_list, use some data from requests(users_url)
#  2. Put tasks to users 

#users model as JSON: {users:[{user1},{user2},{userN}]}?
#Maybe use Class?
#From users need data name, id and email
#From tasks need useerId, completed, title
#Is there really a need for additional processing 
#of the task list that the API returns to me?