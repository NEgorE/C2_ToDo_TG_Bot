from operator import itemgetter
import datetime
import pandas as pd

RUN = True
HELP = '''
Available commands:
/show <date>    - show all tasks for date (first 10 if date is empty)
/add            - add new task
/del            - del task by ID
/clear <date>   - dell all tasks for 1 day (del all tasks if date is empty)
/HELP           - show all available commands
/exit           - stop programm\n
'''
#[(1,'2023-03-30','15:30','Test task n1','N','','ToDo/Done')]

#1,2023-03-30,15:30,Test task n1,N,,ToDo
#2,2023-03-31,08:30,Test task n2,N,,ToDo

list = []
f_list = open('s_list.txt', 'r')
for str in f_list :
    list.append(tuple(str.replace('\n','').split(',')))
f_list.close()
list.sort(key=itemgetter(0))
max_task_in_file = int(list[-1][0])


def check_date(t_date_in) :
    date_format = '%Y-%m-%d'
    try:
        dateObject = datetime.datetime.strptime(t_date_in, date_format)
        return True
    except ValueError:
        print('It\'s not correct date!')
        return False


def check_time(t_time_in) :
    ret = False
    try :
        hh = int(t_time_in[0:1])
        mm = int(t_time_in[3:4])
        if hh < 25 and mm < 60  and t_time_in[2] ==':':
            ret = True
    except ValueError:
        ret = False
    if not ret :
        print('It\'s not correct time!')
    return ret


def add_task() :
    global max_task_in_file
    max_task_in_file +=1
    t_id = max_task_in_file
    date_loop = True
    while date_loop :
        t_date = input('Input date (YYYY-MM-DD): ')
        if check_date(t_date) :
            date_loop = False
    time_loop = True
    while time_loop :
        t_time = input('Input time (HH:MM): ')
        if check_time(t_time) :
            time_loop = False
    t_text = input('Input Task: ')
    
        
def show() :
    global list
    print(list)


def save_list() :
    print('xxx')


while RUN :
    in_str = input('Input command pls:\n')
    p_point = in_str.find(' ')
    if p_point == -1 :
        cur_command = in_str
        p_date = ''
    else :
        cur_command=in_str[0:in_str.find(' ')]
        p_date = in_str[in_str.find(' ')+1:len(in_str)-1]

    if cur_command == '/exit' :
        save_list()
        RUN = False
    elif cur_command == '/show' :
        show()
    elif cur_command == '/HELP' :
        print(HELP)
    elif cur_command == '/add' :
        add_task()
    else :
        print('\nWrong command!!!\nUse /HELP for show list of available comands.\n')


print('\nBye!!!')