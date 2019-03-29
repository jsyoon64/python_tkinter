import sys, time
from threading import Thread

def testexit():
    time.sleep(1)
    sys.exit()
    print("post thread exit")

t = Thread(target = testexit)
t.start()
t.join()
print("pre main exit, post thread exit")
sys.exit()
print("post main exit")