import random

employee = {'employee1', 'employee2', 'employee3', 'employ4', 'employee5', 'employee6', 'employee7', 'employee8',
            'employee9', 'employee10', 'employee11', 'employee12'
            }

dic = {'三等奖': 5, '二等奖': 3, '一等奖': 1}


def lottery(employee, dic):
    for key in dic:
        num = dic[key]
        prize = random.sample(employee, num)
        # print(prize)
        print(f'{key}中奖人员:')
        for i in prize:
            print(i)
        employee = employee - set(prize)


lottery(employee, dic)
