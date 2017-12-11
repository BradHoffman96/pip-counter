from multiprocessing import Queue

def testes(q):
    while(1):
        print(q.get())

   
