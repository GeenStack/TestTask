#coding: utf-8
import os
from time import gmtime, strftime, sleep
import requests
from config import tasks_url, users_url


def get_json(api_url):
    """Функция возвращает данные от API в виде списка"""
    while True:
        try:
            r = requests.get(api_url)
            if (r.status_code != 200):
                error_log = "Ошибка доступа к " + api_url
                error_log +=" Код ответа сервера: " + str(r.status_code)
                print(error_log)
                continue

            return r.json()

        except requests.ConnectionError:
            print("Ошибка соединения. Проверьте подключение к интернету")
            sleep(5)


def create_user_list(user_list_from_api):
    """Создание списка пользователей по данным от API. 
    
    Изначально API дает слишком много данных о пользователе,
    поэтому из список, возвращаемого функцией get_json(api_url),
    нужно обработать и вернуть новый, где каждый пользователь
    представлен в виде словаря, содержащего данные по ключам id,
    name, email, company. В новом представлении каждый пользователь
    имеет два списка для завершенных и оставшихся задач.
    
    """
    user_list = []
    for i in user_list_from_api:
        new_user = {}
        new_user.update({"user_id":i["id"], "name":i["name"],
                        "email":i["email"], "company":i["company"]["name"],
                        "completed":[], "remaining":[]})
        
        user_list.append(new_user)
    return user_list


def add_tasks_to_users(task_list_from_api, user_list):
    """Наполнение списков задач пользователей данными от API."""
    for task in task_list_from_api:
        for user in user_list:
            if(task["userId"] == user["user_id"]):
                if(task["completed"]):
                    user["completed"].append(task["title"])
                else:
                    user["remaining"].append(task["title"])
                break


def create_report_body(header, task_list):
    """Создание тела отчета по заголовку.
    
    В функцию передаются заголовки заершенные/оставшиеся задачи
    и список задач пользователя. Каждая задача отображается 
    на новой строке. Если название задачи соержит
    более 50 символов, то она отображается как 
    первые_50_символов_названия_задачи_...
    Если список задач пуст - это отржается в теле отчета.
    Сформированное тело отчета присваивается
    принятому заголовку, который в итоге возвращается.

    """
    if(len(task_list) == 0):
        return "Пользователь не имеет задач"
    for i in task_list:
        if (len(i) > 50):
            i = i[0:49:] + '...'
        header += "{}\n".format(i)
    return header


def report_preparing(user):
    """Формирует полный текст отчета по пользователю.

    Полный текст отчета состоит из имени пользователя, его адреса
    электронной почты, даты создания отчета.
    Списки задач представлены как два разных тела отчета
    по заголовкам завершенные задачи и отсавшиеся задачи.
    Функция возвращает полный текст отчета.

    """
    date = strftime("%d.%m.%Y %H:%M", gmtime())
    report = "{} <{}> {}\n".format(user["name"], user["email"], date)
    report += "{}\n\n".format(user["company"])
    report += create_report_body("Завершенные задачи:\n",user["completed"])
    report += create_report_body("\nОставшиеся задачи:\n", user["remaining"])
    return report

    
def write_report_to_file(user, report):
    """Запись отчета о пользователе

    Функция принимает пользователя, использует его имя
    для создания пути к файлу отчета. Если пользователь уже существует,
    файл отчета переименовывается по формату имя_дата_последнего_отчета.
    Дата последнего отчета извлекается парсингом (можно было использовать
    регулярное выражение).
    Также функция прнимает сам текст отчета.
    """
    try:
        file_path = "tasks/{}.txt".format(user["name"])
        if(os.path.exists(file_path)):
            f = open(file_path, "r")
            data = f.read()
            f.close()
            data = data.split("\n")
            report_date = data[0][-16::]
            report_date = report_date.replace(" ","T")
            report_date = report_date.replace(".","-")
            os.system("mv \"{}\" tasks/\"{}_{}.txt\"".format(file_path,
                                                             user["name"], 
                                                             report_date)) 

        f = open(file_path, "w")
        f.write(report)
        f.close()

    except IOError:
        print("Ошибка чтения/записи на диск")

    except OSError:
        print("Недостаточно прав для работы с файлами отчетов")


def main():
    if(os.path.exists('/tasks') == False):
        os.system("mkdir tasks")
    user_list = create_user_list(get_json(users_url))
    add_tasks_to_users(get_json(tasks_url), user_list)
    for i in user_list:
        write_report_to_file(i, report_preparing(i))


if __name__ == "__main__":
    main()
