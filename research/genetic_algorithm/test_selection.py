def selection(performance_dict):

    sorted_dict = dict(sorted(performance_dict.items(), key=lambda x: x[1], reverse=True))
    # Eliminare gli ultimi 2 elementi del dizionario ordinato
    keys_to_remove = list(sorted_dict.keys())[-2:]
    for key in keys_to_remove:
        del sorted_dict[key]
    
    return sorted_dict