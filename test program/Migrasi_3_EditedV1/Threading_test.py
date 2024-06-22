from concurrent.futures import thread
import threading
import time


start = time.perf_counter()


class CPUPainter:
    def paintwall(self):
        time.sleep(2)
        print('Wall Painted')

    def __init__(self):
        self.t = threading.Thread(target=self.paintwall)
        self.t.start()

        # self.paintwall()
    def finishing(self):
        self.t.join()


a = CPUPainter()
b = CPUPainter()
c = CPUPainter()
d = CPUPainter()
a.finishing()
b.finishing()
c.finishing()
d.finishing()
finish = time.perf_counter()

print(round(finish-start, 2))
