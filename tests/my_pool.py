import time
from pymyorm.connection_pool import ConnectionPool
from config import db
from models.user import User
from threading import Thread


# 定义一个线程任务
class TaskThread(Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        from pymyorm.local import local
        from pymyorm.connection_pool import ConnectionPool
        pool = ConnectionPool()
        local.conn = pool.get()
        print(f"thread name={self.name} conn={local.conn}")
        time.sleep(3)
        count = User.find().count()
        print(count)
        pool.put(local.conn)


if __name__ == '__main__':

    pool = ConnectionPool()
    pool.size(size=3)
    pool.create(**db)
    stime = time.time()
    thread_list = []
    for i in range(2):
        thread = TaskThread(str(i))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    etime = time.time()
    print(f"time diff: {etime - stime}")
