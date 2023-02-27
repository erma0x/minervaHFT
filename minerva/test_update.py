
import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from minerva.oracle import update_performance

update_performance(performance=21,performance_name='fitness',path='minerva/runs/experiment_136/generation_0/strategy_0.py')