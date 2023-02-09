# from runExe import Run
from datetime import datetime
from pivots import pivot
from awsApp import upload
from awsApp import download

def _testExe():

    lbRight = 2    
    lbLeft = 2
    data = [1,2,15,10,11,12,11,10,20,9,11,13,12,8]
    res = pivot(data,lbLeft,lbRight,"high")

    print ("Pivot res:", res)
    return res

def _testUploadAWS():
    files = []
    files.append("D:\\kraken balance\\test.json")
    files.append("D:\\kraken balance\\testsnapshots.json")
    files.append("D:\\kraken balance\\test.log")

    destFolder = "Folder3/NewFolderToGet/"
    bucket_name="ojbucket-2"
    res = upload(files, destFolder, bucket_name)

def _testDownloadFromAWS():
    files = []
    files.append("D:\\kraken balance\\test.json")
    files.append("D:\\kraken balance\\testsnapshots.json")
    files.append("D:\\kraken balance\\test.log")

    aws_folder = "Folder3/NewFolderToGet/"
    donwload_folder = "c:\\Temp\\"
    donwload_folder = ""
    bucket_name="ojbucket-2"
    suffix = "json"
    download(bucket_name, aws_folder, suffix, donwload_folder) 

def main(args):
    _testDownloadFromAWS()
    
    # _testExe()

    return

if __name__ == '__main__':
   
    main(None)
  
