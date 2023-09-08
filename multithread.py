from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
import time

lock = Lock()

temp = []
array = []
num_list = list(range(13))


# def worker(i):
#     print(i)
#     print(f"{i} sleeping")
#     time.sleep(5)
#     print(f"{i} end")

def worker_lock(i):
    try:
        print('start ', i)
        with lock:
            print(i)
            array.append(i)
        time.sleep(5)
        print('endddddd')
    except Exception as e:
        print("loi ", e)
        # time.sleep(5)
        # print(f"{i} end")


# for i in range(13):
#     t = Thread(target=worker, args=(i,))
#     temp.append(t)
#     if len(temp) == 5:
#         for j in temp:
#             j.start()
#             # j.join()
#         for j in temp:
#             j.join()
#         temp.clear()
# print(f"con {len(temp)} luong")
# for j in temp:
#     j.start()

# with ThreadPoolExecutor(max_workers=5) as thr:
#     for i in range(13):
#         thr.submit(worker, i)

with ThreadPoolExecutor(max_workers=5) as thr:
    while True:
        # print("len(num_list): ", len(num_list))
        try:
            num = num_list.pop()
        except IndexError:
            break
        thr.submit(worker_lock, num)