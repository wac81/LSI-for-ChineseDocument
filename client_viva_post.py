# coding=utf8

import requests
import threading
import time

payload = {'text': '韦小宝最看重的不是妹子，不是钱。他想要这些，不过是因为他所处的环境里认这些，所以他也要。就如同你我身边不少人豁出命去考个什么公务员，怎么，他们的理想是当公务员？真有多热爱这个职业？当他遇到生命危险时，钱是可以扔的，妹子是可以不要的。七个老婆，你觉得他真心喜欢过谁？他追妹子的方式，全是把她们当战利品，这和他的妓院出身有关系，和金庸笔下其他男性半点不像。他见着漂亮的就要，越多越好，因为他打小就觉得这是成功的标志。'}
# payload = {'text': '韦小宝最看重的不是妹子，不是钱。他想要这些，不过是因为他所处的环境里认这些'}
def test_run():
    # time.sleep(4)
    r = requests.post("http://115.28.254.33:8088/similar/post",data=payload)
    # r = requests.post("http://192.168.11.128:3000/similar/s",data=payload)
    print r


#单线程顺序测试
for index in range(1000):
    test_run()

#多线程并发
# for index in range(100):
#     t=threading.Thread(target=test_run)
#     # t.daemon = True
#     t.start()

# threads = []
# for num in range(0, 10):
#     thread = test_run()
#     thread.start()
#     threads.append(thread)
# for thread in threads:
#     thread.join()