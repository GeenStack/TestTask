#coding: utf-8

from config import tasks_url, users_url
import requests
from time import sleep
from time import gmtime, strftime
import os


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
        for user in users_list:
            if (task["userId"] == user["userId"]):
                if(task["completed"]):
                    user["completed_tasks"].append(task["title"])
                else:
                    user["lost_task"].append(task["title"])
                break


def format_tasks_report(preview, task_list):
    if(len(task_list) == 0):
        return "User is not have tasks"
    for i in task_list:
        if (len(i) > 50):
            i = i[0:49:]+'...'
        preview +='{}\n'.format(i)
    return preview

def report_preparing(user):
    report_creating_date = strftime("%d.%m.%Y %H:%M", gmtime())
    report = '{} <{}> {}\n'.format(user["name"], user["email"], report_creating_date)
    report += '{}\n\n'.format(user["company"])
    report += format_tasks_report('completed_tasks:\n',user['completed_tasks'])
    report += format_tasks_report('\nLost_tasks:\n', user['lost_task'])
    print(report)
    return report
    
def write_report_to_file(user, report):
    try:
        file_path = "tasks/{}.txt".format(user["name"])
        if(os.path.exists(file_path)):
            f = open(file_path, 'r')
            data = f.read()
            f.close()
            data = data.split('\n')
            report_date = data[0][-16::]
            report_date = report_date.replace(' ','T')
            report_date = report_date.replace('.','-')
            os.system('mv \"{}\" tasks/\"{}_{}.txt\"'.format(file_path,user["name"], report_date)) 

        f = open(file_path, 'w')
        f.write(report)
        f.close()
    except (IOError, OSError) as e:
        print("Вызвана ошибка ")
        print(e)




test_users_list = users_list_created(get_data_from_api(users_url))
parsing_tasks_list_and_add_to_users(get_data_from_api(tasks_url), test_users_list)
for i in test_users_list:
    write_report_to_file(i, report_preparing(i))
