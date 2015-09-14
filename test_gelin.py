
# coding=utf-8

def gen_list(expression):
    '''将输入的字符串表达式转换为列表'''
    units = []#保存包含操作符和操作数的列表
    start = 0#标记数字起点
    # expression = (expression if expression[len(expression) - 1] == "=" else expression + "=")
    for i in range(len(expression)):
        # units.append(float(expression[start:i]))
        units.append(expression[i])
        start = i + 1
    return units

def base_calculate(expression, isFirst = True):
    units = []#保存包含操作符和操作数的列表
    for i in range(len(expression)):
        units.append(expression[i])
    units = gen_list(expression)
    num=[]
    result = -1
    try:
        for u in units:
            if (u != '+') and (u !='*'):
                num.append(int(u))
            elif u == '+':
                #get num[] last one and the last second
                a = num[len(num)-1]
                b = num[len(num)-2]
                num.remove(a)
                num.remove(b)
                num.append(a+b)
            elif u == '*':
                #get num[] last one and the last second
                a = num[len(num)-1]
                b = num[len(num)-2]
                num.remove(a)
                num.remove(b)
                num.append(a*b)
    except:
        return result

    result = num[len(num)-1]

    return result#返回结果



print base_calculate('13+62*7+*+')