import subprocess
import threading

def _RunExe(cmdLine, args : list, processID):
    try:
        #prepare the arguments list
        _args = [cmdLine]
    
        if (type(args) == list):
            # if arguments to process supplied
            _args.extend(args)
        
        #execute exe file
        subprocess.run(_args)

    except subprocess.CalledProcessError:
        pass        
    except subprocess.SubprocessError :
        pass
    except:
        pass
    finally:
        print ("Process {} done".format(str(processID)))
        pass

def Run(exeToRun: str, path: str, args: list, numberOfInstance=1):
    
    #verify terminates with back slash
    if (path[-1] != "\\"):
        path = path + "\\"

    fullPath = path + exeToRun

    threads = list()
    #start all threads 
    for i in range(numberOfInstance):
        #create thread
        x = threading.Thread(target=_RunExe, args=(fullPath, args, i))
        #store for later join
        threads.append(x)
        #start
        x.start()

    # wait all threads termination
    for index, thread in enumerate(threads):
        thread.join()
        print("Main    : thread {} done".format(str(index)) )

