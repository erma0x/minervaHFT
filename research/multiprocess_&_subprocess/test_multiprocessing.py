import multiprocessing
import subprocess

def start_oracle(file):
    #oracle_file = file.split('/minervaHFT/')[1]
    process = subprocess.Popen(['python3','minerva/oracle.py',f'-s {file}'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'pid {process.pid} python3 minerva/oracle.py -s {file}')

def start_streamer():
    process = subprocess.Popen(['python3', f'minerva/streamer.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f'pid {process.pid} python3 minerva/streamer.py')


file_strategy = 'minerva/runs/experiment_157/generation_0/strategy_2.py'
process = multiprocessing.Process(target=start_oracle, args=(file_strategy,))
process.start()
process.join()

p = multiprocessing.Pool(multiprocessing.cpu_count())
p.map(func, range(1, 100))
