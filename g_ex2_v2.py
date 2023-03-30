from operator import itemgetter

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

list = []
f_list = open('s_list.txt', 'r')
for str in f_list :
    list.append(tuple(str.replace('\n','').split(',')))
f_list.close()
list.sort(key=itemgetter(0))
max_task_in_file = list[-1][0]

def add_task() :
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
        RUN = False
    elif cur_command == '/show' :
        print('\nThis command is not relized yet.\n')
    elif cur_command == '/HELP' :
        print(HELP)
    elif cur_command == '/add' :
        add_task()
    else :
        print('\nWrong command!!!\nUse /HELP for show list of available comands.\n')


print('\nBye!!!')