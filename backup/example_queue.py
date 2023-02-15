import time
import random as rnd


from collections import deque
my_buffer = deque(maxlen=3)

while True:

    data = rnd.randint(0, 10)
    my_buffer.append(data)

    print(my_buffer)
    print(my_buffer[-1])
    time.sleep(1)


#In questo esempio, la struttura dati inizialmente conterrà solo 2 elementi [1,2,3] e [4,5,6]. Se si tenta di aggiungere un nuovo elemento, l'elemento più vecchio verrà automaticamente rimosso.
#Nota che collections.deque non è pensato per essere utilizzato con thread multipli, per farlo si può usare il modulo queue.




