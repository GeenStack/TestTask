from config import tasks_url
import requests

def get_tasks_list():
	response = requests.get(tasks_url)
	if (response.status_code != 200):
		error_log = 'Failed to access ' + tasks_url 
		error_log += ' Server response status code: ' + str(response.status_code)
		print(error_log)
		get_tasks_list()
	task_list = response.json()
	return task_list

def get_users_list():
	response = requests.get(users_url)
	if (response.status_code != 200):
		error_log = 'Failed to access ' + users_url
		error_log +=' Server response status code: ' +str(response.status_code)
		print(error_log)
		get_users_list()
	users_list = response.json()
	return users_list