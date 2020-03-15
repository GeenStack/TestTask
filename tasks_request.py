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
        new_user.update({"userId":i["id"], "name":i["name"], "email":i["email"], 
                        "company":i["company"]["name"],"completed_tasks":[], "lost_task":[]})
        
        users_list.append(new_user)
    return users_list


def parsing_tasks_list_and_add_to_users(tasks_list, users_list):
    for task in tasks_list:
        #Now need find user
        for user in users_list:
            if (task["userId"] == user["userId"]):
                if(task["completed"]):
                    user["completed_tasks"].append(task["title"])
                else:
                    user["lost_task"].append(task["title"])
                break




def print_user(user):#THIS FUNCTION ONLY FOR DEBUG
    print("ID "+str(user["userId"]))
    print("name "+str(user["name"]))
    print("email "+str(user["email"]))
    print("company "+str(user["company"]))
    print("COMPLETED TASKS LIST")
    print(user["completed_tasks"])
    print("LOST TASKS LIST")
    print(user['lost_task'])
    print('\n\n')

#So, need describe the report model
#report include:
# 1. name, url, creating_time
# 2. user_company
def report_preparing(user):
    pass

test_users_list = users_list_created(get_data_from_api(users_url))
parsing_tasks_list_and_add_to_users(get_data_from_api(tasks_url), test_users_list)
for i in test_users_list:
    print_user(i)
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