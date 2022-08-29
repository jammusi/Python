from runExe import RunExe
from datetime import datetime
import threading
    
def _testExe():
    
    path = "C:\\Windows\\System32\\"
    exeToRun = "notepad.exe"

    fullPath = path + exeToRun

    numOfTime = 10
    for i in range(numOfTime):

        now = datetime.now()
        start_time = now.strftime("%H:%M:%S")


        RunExe(fullPath)

        now = datetime.now()
        end_time = now.strftime("%H:%M:%S")
        print ("Process started: {} and terminated: {}".format(start_time,end_time) )

def _testExe2():
    
    path = "C:\\Windows\\System32\\"
    exeToRun = "notepad.exe"

    # path = r'{"D:\Projects\VS Projects\Tests\ConsoleApp1\ConsoleApp1\bin\Debug"}' 
    # exeToRun = "ConsoleApp1.exe"

    # path = r'{"C:\Program Files (x86)\Microsoft Office\Office15\"}'
    # exeToRun = "winword.exe"

    # path = ""
    # exeToRun = r'{"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"}'
    
    path = "D:\\Projects\\Momentix\\octopus-ftx_futures\\TestApp\\bin\\Debug\\"
    exeToRun = "TestApp.exe"
    fullPath = path + exeToRun


    numOfTime = 2
    
    threads = list()
    #start all threads 
    for i in range(numOfTime):

        x = threading.Thread(target=RunExe, args=(fullPath,i))
        threads.append(x)
        x.start()

    # wait all treada termination
    for index, thread in enumerate(threads):
        thread.join()
        print("Main    : thread {} done".format(str(index)) )


def main(args):
    _testExe2()
    return

if __name__ == '__main__':
   
    main(None)
  
