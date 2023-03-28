i = 0
dict = {}
GLOBAL_TASK_ID = 0

while i == 0 :
    in_date = input('Input date: ')
    
    if in_date in dict :
        dict_day = dict[in_date]
    else :
        dict_day = {}

    in_task = input('Input task: ')
    GLOBAL_TASK_ID += 1

    dict_day[GLOBAL_TASK_ID] = in_task

    dict[in_date] = dict_day

    print(dict)

    y = input('Vihodim? (Y/N)')

    if y == 'Y' :
        i = 1

print('Bye!!!')