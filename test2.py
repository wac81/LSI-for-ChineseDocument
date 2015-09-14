__author__ = 'wuanc'

def solutions(S):
    dec = int(S, 2)
    numsteps = 0
    while 1:
        x = dec%2
        dec = dec // 2
        if dec == 0 and x == 1:
            numsteps =numsteps+1
            break
        if x == 1:numsteps=numsteps+2
        if x == 0:numsteps=numsteps+1
        # if dec == 0: break
    return numsteps

print solutions('10')
