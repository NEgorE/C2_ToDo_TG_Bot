import telebot
from operator import itemgetter
import datetime
import csv
import os.path
import time

from token_str import token
bot = telebot.TeleBot(token)

FILE = 's_list.txt'
HELP = '''
Available commands:
/show <date>    - show all tasks for date (first 10 if date is empty)
/add            - add new task
/del            - del task by ID
/clear <date>   - dell all tasks for 1 day (del all tasks if date is empty)
/help           - show all available commands
/exit           - stop programm\n
'''

input_str = ''
list_tasks = []
add_task_list = []
if os.path.isfile(FILE) :
    f_list_tasks = open(FILE, 'r')
    for str in f_list_tasks :
        list_tasks.append(tuple(str.replace('\n','').split(',')))
    f_list_tasks.close()
    list_tasks.sort(key=itemgetter(0))
    if len(list_tasks) > 0 :
        max_task_in_file = int(list_tasks[-1][0])
    changed = False


@bot.message_handler(commands=["help"])
def help(msg) :
    print(msg.text)
    bot.send_message(msg.chat.id, HELP)


@bot.message_handler(commands=["show"])
def show(msg) :
    global add_task_list
    print(add_task_list)
    msg_id = msg.chat.id
    msg_text = msg.text
    print(msg_text)
    global list_tasks
    if msg_text == '/show' :
        print_list(list_tasks, msg_id)
    else :
        p_date_in = msg_text[msg_text.find(' ')+1:len(msg_text)]
        list_tasks_filtred = filter(lambda t: (t[1] == p_date_in) , list_tasks)
        print_list(list(list_tasks_filtred), msg_id)


@bot.message_handler(commands=["add"])
def add_init(msg) :
    msg_id = msg.chat.id
    msg_text = msg.text
    print(msg_text)
    bot.send_message(msg_id, 'start add mode')
    add(msg,'INIT')
    bot.send_message(msg_id, 'Input date pls (YYYY-MM-DD)')
    bot.register_next_step_handler(msg, add, 'INPUT_DATE')


def add(msg, com):
    global max_task_in_file, add_task_list
    if com == 'INIT' :
        max_task_in_file += 1
        add_task_list.append(max_task_in_file)
    elif com == 'INPUT_DATE' :
        in_date = check_date(msg)
        print(in_date)
        if in_date == '' :
            bot.register_next_step_handler(msg, add, 'INPUT_DATE')
        else :
            add_task_list.append(in_date)
            bot.register_next_step_handler(msg, add, 'INPUT_TIME')       
    elif com == 'INPUT_TIME' :
        #in_time = check_time(msg)
        in_time = msg.text
        print(in_time)


def check_time(msg) :
    time_loop = True
    while time_loop :
        t_time_in = input(msg)
        try :
            hh = int(t_time_in[0:2])
            mm = int(t_time_in[3:5])
            if hh < 25 and mm < 60  and t_time_in[2] ==':':
                time_loop = False
            else :
                print('It\'s not correct time!')
        except ValueError:
            print('It\'s not correct time!')
    return t_time_in

def check_date(msg) :
    date_format = '%Y-%m-%d'
    return_str = ''
    try:
        dateObject = datetime.datetime.strptime(msg.text, date_format)
        return_str = msg.text
    except ValueError:
        bot.send_message(msg.chat.id, 'It\'s not correct date!')
        bot.send_message(msg.chat.id, 'Input date pls (YYYY-MM-DD)')
    return return_str
        

def print_list(lfp, msg_id) :
    answ = ''
    lfp_ord = lfp
    lfp_ord.sort(key=itemgetter(1))
    cur_date = ''
    pref_date = ''
    for task in lfp :
        cur_date = task[1]
        if cur_date != pref_date : 
            answ += f'\n{cur_date}:'
        answ += f'\n    - {task[2]} : {task[3]}'
        pref_date = cur_date
    answ += ''
    if len(answ.strip()) > 0 :
        bot.send_message(msg_id, answ)
    else :
        bot.send_message(msg_id, 'List is empty :(')


bot.polling(none_stop = True)