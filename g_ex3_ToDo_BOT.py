import telebot
from operator import itemgetter
import datetime
import csv
import os.path
import time

#3,2020-01-20,15:15,add_task1,N,,ToDo
#4,2020-01-20,16:00,add_task2,Y,15:30,ToDo
#1,2023-03-30,15:30,Test task n1,N,,ToDo
#2,2023-03-31,08:30,Test task n2,N,,ToDo
#5,2024-01-01,08:00,HNY,Y,07:45,ToDo
#6,2024-02-01,15:52,fghfjh,N,,ToDo


from token_str import token
bot = telebot.TeleBot(token)

FILE = 's_list.txt'
HELP = '''
Available commands:
/show <param>    - show all tasks for date(first 5 tasks if param is empty)
/add                    - add new task
/del  <param>   - del task by ID or all tasks for date
/help                   - show all available commands\n
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
        list_tasks.sort(key=itemgetter(1,2))
        print_list(list_tasks[:5], msg_id)
    else :
        p_date_in = msg_text[msg_text.find(' ')+1:len(msg_text)]
        if p_date_in == 'all' :
            print_list(list_tasks[:100], msg_id)
        else :
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

@bot.message_handler(commands=["del"])
def del_by_id(msg) :
    bot.send_message(msg.chat.id, 'Del mod')


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
            bot.send_message(msg.chat.id, 'Input task time (HH:MM): ')
            bot.register_next_step_handler(msg, add, 'INPUT_TIME')       
    elif com in ['INPUT_TIME','INPUT_NOTIF_TIME'] :
        in_time = check_time(msg)
        print(in_time)
        if in_time == '' :
            if com == 'INPUT_TIME' :
                bot.register_next_step_handler(msg, add, 'INPUT_TIME')
            else :
                bot.register_next_step_handler(msg, add, 'INPUT_NOTIF_TIME')
        else :
            add_task_list.append(in_time)
            if com == 'INPUT_TIME' :
                bot.send_message(msg.chat.id, 'Task task text:')
                bot.register_next_step_handler(msg, add, 'TASK_TEXT')
            else :
                add_task_list.append('ToDo')
                list_tasks.append(tuple(add_task_list))
                save_file(list_tasks)
    elif com == 'NOTIF_NEED' :
        in_notif_need = msg.text
        print(in_notif_need)
        if in_notif_need == 'Y' :
            add_task_list.append(in_notif_need)
            bot.send_message(msg.chat.id, 'Input notif time (HH:MM): ')
            bot.register_next_step_handler(msg, add, 'INPUT_NOTIF_TIME')
        elif in_notif_need == 'N' :
            add_task_list.append(in_notif_need)
            add_task_list.append('')
            add_task_list.append('ToDo')
            list_tasks.append(tuple(add_task_list))
            save_file(list_tasks)
        else :
            bot.send_message(msg.chat.id, 'Wrong input!!!')
            bot.send_message(msg.chat.id, 'Need notification? (input Y or N): ')
            bot.register_next_step_handler(msg, add, 'NOTIF_NEED')
    elif com == 'TASK_TEXT' :
        in_task_text = msg.text
        if in_task_text == '' :
            bot.send_message(msg.chat.id, 'Task text cant be empty!!!')
            bot.send_message(msg.chat.id, 'Task task text:')
            bot.register_next_step_handler(msg, add, 'TASK_TEXT')
        else :
            add_task_list.append(in_task_text)
            bot.send_message(msg.chat.id, 'Need notification? (input Y or N): ')
            bot.register_next_step_handler(msg, add, 'NOTIF_NEED')


def save_file (t_list) :
    t_list.sort(key=itemgetter(0))
    with open(FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(t_list)


def check_time(msg) :
    t_time_in = ''
    try :
        hh = int(msg.text[0:2])
        mm = int(msg.text[3:5])
        if hh < 25 and mm < 60  and msg.text[2] ==':':
            t_time_in = msg.text
        else :
            t_time_in = ''
    except ValueError:
        t_time_in = ''
    if t_time_in == '' :
        bot.send_message(msg.chat.id, 'It\'s not correct time!')
        bot.send_message(msg.chat.id, 'Input task time (HH:MM): ')
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
    lfp_ord.sort(key=itemgetter(1,2))
    cur_date = ''
    pref_date = ''
    for task in lfp :
        cur_date = task[1]
        if cur_date != pref_date : 
            answ += f'\n{cur_date}:'
        answ += f'\n    - {task[2]} : {task[3]} (taskId: {task[0]})'
        pref_date = cur_date
    answ += ''
    if len(answ.strip()) > 0 :
        bot.send_message(msg_id, answ)
    else :
        bot.send_message(msg_id, 'List is empty :(')


bot.polling(none_stop = True)