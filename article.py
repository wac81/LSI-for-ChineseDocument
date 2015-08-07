#coding=utf8


import os
# clear all html tags
def stripTags(s):
    ''' Strips HTML tags.
        Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440481
    '''
    intag = [False]

    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True

    return ''.join(c for c in s if chk(c))


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' 目录已存在'
        return False

# 定义要创建的目录
mkpath="ac"
# 调用函数
mkdir(mkpath)
fp = open('ac.txt','r')


# for line in fp:
#     c=str(line)
#
#     #打开一个新文件写
    # fnew=open(mkpath+'/'+c.split('<')[0]+'.txt','w')  //
#         fnew.write(stripTags(c))
#         fnew.close()
# fp.close()

cx=''

# def writefile(line):
#     c=str(line)
#     cx=cx+c
#     #打开一个新文件写
#     # fnew=open(mkpath+'/'+c.split('<')[0]+'.txt','w')  //
#     if len(c)>0 :
#         if c[len(c)-2]=='\\':
#             return
#
#         name = cx.split('	')[0]
#         name = os.path.normpath(name)
#         try:
#             fnew=open(mkpath+'/'+name.decode('utf8')+'.txt','w')
#         except:
#             cx=''
#             return cx
#         # fnew=open(mkpath+'/'+cx[0:20]+'.txt','w')
#         fnew.write(stripTags(cx))
#         fnew.close()
#         cx=''
#
# from multiprocessing.dummy import Pool as ThreadPool
# pool = ThreadPool(4)
# dictionary = pool.map(writefile,fp)
# pool.close()
# pool.join()

for line in fp:
    c=str(line)
    cx=cx+c
    #打开一个新文件写
    # fnew=open(mkpath+'/'+c.split('<')[0]+'.txt','w')  //
    if len(c)>0 :
        if c[len(c)-2]=='\\':
            continue

        name = cx.split('	')[0]
        name = os.path.normpath(name)
        try:
            fnew=open(mkpath+'/'+name.decode('utf8')+'.txt','w')
        except:
            cx=''
            continue
        # fnew=open(mkpath+'/'+cx[0:20]+'.txt','w')
        fnew.write(stripTags(cx))
        fnew.close()
        cx=''
fp.close()
