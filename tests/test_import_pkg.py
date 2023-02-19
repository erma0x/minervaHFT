#from ..runs.experiment_0.generation_0.strategy_0 import MARKET
# progetto/
# ├── config/
# │   ├── config.ini
# └── test/
#     ├── test_file.py
import sys
sys.path.append(sys.path[0].replace("tests/","minerva/"))

from ..configuration_backtest import MARKET
print(MARKET)
