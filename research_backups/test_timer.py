from utils.mytimer import Timer
import time


my_timer = Timer()

my_timer.start()

time.sleep(2)

my_timer.stop()

print(my_timer.elapsed)