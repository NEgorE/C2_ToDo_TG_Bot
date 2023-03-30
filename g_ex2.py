import json

dict = {}
f_dict = open('s_dict.txt', 'r')
s_dict = f_dict.read()
if len(s_dict)!=0 :
    dict = json.loads(s_dict)
f_dict.close()

GLOBAL_TASK_ID = 0
if dict != {} :
    GLOBAL_TASK_ID = dict['MAX_TASK_ID']

RUN = True
cur_command = ''
HELP = '''
Available commands:
/show <date>    - show all tasks for date (first 10 if date is empty)
/add            - add new task
/del            - del task by ID
/clear <date>   - dell all tasks for 1 day (del all tasks if date is empty)
/HELP           - show all available commands
/exit           - stop programm\n
'''


def add_task() :
    global GLOBAL_TASK_ID
    in_date = input('Input date: ')
    
    if in_date in dict :
        dict_day = dict[in_date]
    else :
        dict_day = {}

    in_task = input('Input task: ')
    GLOBAL_TASK_ID += 1

    dict_day[str(GLOBAL_TASK_ID)] = in_task

    dict[in_date] = dict_day
    dict["MAX_TASK_ID"] = GLOBAL_TASK_ID


def help() :
    print(HELP)


def show(p_date) :
    global dict
    if p_date == '' :
        print(dict)
    else :
        if p_date in dict :
            print(dict[p_date])
        else :
            print('Date not found!')


def d_save() :
    global dict
    new_f_dict = open('s_dict.txt', 'w')
    new_f_dict.write(str(dict).replace('\'','\"'))
    new_f_dict.close()

while RUN :
    in_str = input('Input command pls:\n')
    p_point = in_str.find(' ')
    if p_point == -1 :
        cur_command = in_str
        p_date = ''
    else :
        cur_command=in_str[0:in_str.find(' ')]
        print(cur_command)
        p_date = in_str[in_str.find(' ')+1:len(in_str)-1]
    

    if cur_command == '/exit' :
        d_save()
        RUN = False

    elif cur_command == '/show' :
        show(p_date)

    elif cur_command == '/HELP' :
        print(HELP)
    
    elif cur_command == '/add' :
        add_task()
    else :
        print('\nWrong command!!!\nUse /HELP for show list of available comands.\n')


print('\nBye!!!')