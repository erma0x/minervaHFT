import subprocess
p = subprocess.Popen(['python3', 'minerva/oracle.py','-s minerva/runs/experiment_157/generation_0/strategy_1.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = subprocess.Popen(['python3', 'minerva/oracle.py','-s minerva/runs/experiment_157/generation_0/strategy_2.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = subprocess.Popen(['python3', 'minerva/oracle.py','-s minerva/runs/experiment_157/generation_0/strategy_3.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = subprocess.Popen(['python3', 'minerva/oracle.py','-s minerva/runs/experiment_157/generation_0/strategy_0.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = p.communicate()
# print('-'*100)
# print('out', out)
# print('-'*100)
# print('err', err)
# print('-'*100)
# print('EXIT')