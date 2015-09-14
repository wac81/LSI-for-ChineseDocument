__author__ = 'wuanc'

def solution(A):
    # write your code in Python 2.7
    units=[]
    for i in A:
        if len(units)==0:
            units.append(i)
            continue
        for k in units:
            if k!=i:units.append(k)






    pass


print solution([5,4,4,5,0,12])