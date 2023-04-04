import telebot
from operator import itemgetter
import datetime
import csv
import os.path

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

list_tasks = []
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
def help(msg) :
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