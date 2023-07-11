from time import sleep
from sys import stdout
import json
import numpy as np 
import threading
import logger

def thr(str = "file", lock = threading.Lock()):
    lock.acquire()
    try:
        try: 
            f = open(str, 'r')
        except FileNotFoundError:
            logger.test.warning(f"O arquivo {str} não existe")
        
        data = [json.loads(line) for line in f]
    except KeyboardInterrupt as ki:
        logger.test.info("Adm has manually stopped the process")
    finally:
        f.close()
        lock.release()


def loading(str):
    animations = [".::::", ":.:::", "::.::", ":::.:", "::::.", ":::: ", ":::  ", "::   ", ":    ", "    .", "   ..", "  ...", " ....", "....:", "...::", "..:::", ".::::", ":::::"]
    for animation in animations:
        stdout.write(f"loading {animation} \n")
        stdout.flush()
        sleep(0.1)

if __name__ == "__main__":

    s0 = "C:\\Users\\RHMSF\\Documents\\Python\\Projeto\\basic-proj\\Dados\\cz.muni.csirt."
    s1 = "Entry\\data.json"

    IPflow_d = s0 + "IPFlow" + s1
    Syslog_d = s0 + "Syslog" + s1
    Winlog_d = s0 + "Winlog" + s1

    Str = [IPflow_d]#, Syslog_d, Winlog_d]
    # Create multiple threads

    lock = threading.Lock()
    
    threads = []
    for s in Str:
        t = threading.Thread(target=thr, args=(s, lock,))
        threads.append(t)
        t.start()

    
    for s in Str:
        while t.is_alive:
            loading(s)

    # Wait for all threads to finish
    for t in threads:
        t.join()
