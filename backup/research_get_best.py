import os

def get_performance_dict(filepath_strategies='./strategies/'):
    obj = os.scandir(filepath_strategies)
    list_of_files = []
    
    for entry in obj :
        if entry.is_file() and entry.name not in ("__init__.py","__pycache__") :
            list_of_files.append(entry.name)
    
    print(list_of_files)
    
    file_paths = ['./strategies/'+str(i) for i in list_of_files]
    performance_dict = {}
    # for file_path in file_paths:
    #     with open(file_path, "r") as file:
    #         for line in file:
    #             if "fitness" in line:
    #                 key, value = line.strip().split("=")
    #                 key_dict = int(file_path.replace("./strategies/s","").replace(".py",''))
    #                 value = float(value.replace(" ", ""))
    #                 performance_dict[key_dict] = value

    #return  performance_dict

get_performance_dict()
