from configuration_backtest import ROOT_PATH

def save_performance(path_strategy):
    path_strategy = path_strategy.replace('./strategies/','').replace(ROOT_PATH*2,ROOT_PATH)
    performance = 0

    with open(path_strategy, "r") as file:
        contents = file.readlines()
        for i in range(len(contents)):
            if 'fitness' in contents[i]:
                fitness_raw = contents[i]
                if '[' in fitness_raw:
                    fitness_raw = fitness_raw.replace(']', '').replace('[', '')

                performance = fitness_raw.split('=')[1].replace(' ','')

    path_performance = path_strategy.replace(ROOT_PATH*2,ROOT_PATH).replace('strategies/s','strategies/p')
    with open(path_performance, "w+") as file:
        file.write(performance)


if __name__ == "__main__":
    save_performance('strategies/s0.py')