import subprocess
#import os
import threading


def _RunExe(cmdLine,processID):
    try:
        subprocess.run(cmdLine, check=False)
    except subprocess.CalledProcessError:
        pass        
    except subprocess.SubprocessError :
        pass
    except:
        pass
    finally:
        print ("Process {} done".format(str(processID)))
        pass

def Run(exeToRun, path, numberOfInstance=1):
    
    #verify terminates with back slash
    if (path[-1] != "\\"):
        path = path + "\\"

    fullPath = path + exeToRun

    threads = list()
    #start all threads 
    for i in range(numberOfInstance):

        x = threading.Thread(target=_RunExe, args=(fullPath,i))
        threads.append(x)
        x.start()

    # wait all treada termination
    for index, thread in enumerate(threads):
        thread.join()
        print("Main    : thread {} done".format(str(index)) )

