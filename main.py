from runExe import Run
from datetime import datetime
import threading
    
def _testExe():
    
    path = "D:\\Projects\\Momentix\\octopus-ftx_futures\\TestApp\\bin\\Debug"
    exeToRun = "TestApp.exe"
    args = ["My name"]
    Run(exeToRun, path,args, 2)


def main(args):
    _testExe()
    return

if __name__ == '__main__':
   
    main(None)
  
