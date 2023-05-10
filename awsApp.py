import boto3 
import traceback
import botocore

def _validate_aws_folder_name(folder_name) -> str:
     #last char must be "/". 
     # append if not
    result = folder_name
    if folder_name.rfind("/") < len(folder_name) - 1:
        result = folder_name + "/"
    
    return result

def _extract_fname_from_path(path: str) -> str:
    #last backslash index
    i = path.rindex("\\")
    #slice from index to end
    fname = path[i+1::]

    return fname

def _upload(files, dest_folder, bucket) -> list:

    failed = []

    client = boto3.client("s3")

    for file in files:

        try:
            if isinstance(file, tuple):

                # expected ex 2 items tuple: 
                #  ("c:\\temp\fname.pdf" , "newName.pdf")
                if len(file) == 2:
                    tname = file[1]
                else:
                    #use first entry as target name
                    tname = _extract_fname_from_path(file[0])

                #when tuple supplied - soruce name is the first entry
                sname = file[0]

            elif(isinstance(file,str)):
                tname = _extract_fname_from_path(file)
                sname = file
                
            else:
                sname = ""
                failed.append(file)
                print("unsupported file name format. file ignored. expected 2 items tuple or string got:", file)

            #upload
            if (sname):
                client.upload_file(sname, bucket, dest_folder + tname)

        except Exception as e:
            print(traceback.format_exc())
            failed.append(file)

    #return failed list
    return failed

def upload(files: list, dest_folder: str, bucket_name: str) -> list:
    failed = None
    try:
        #last char must be "/". 
        # append if not
        if dest_folder.rfind("/") < len(dest_folder) - 1:
            dest_folder += "/"

        failed = _upload(files, dest_folder, bucket_name)

    except Exception as e:
        print("upload AWS failed", e)
        print(traceback.format_exc())

    finally:

        return failed if failed and len(failed) > 0 else None

def download(bucket_name, aws_folder, suffix="", download_folder=""):
    try:
        valid_aws_folder = _validate_aws_folder_name(aws_folder)
        resource = boto3.resource("s3")
        bucket = resource.Bucket(bucket_name)
        all_objects = bucket.objects
        
        #get all file names in aws folder
        filterred = all_objects.filter(Prefix=valid_aws_folder)

        #iterate files
        for object_summary in filterred:

            print(f' current file/folder: {object_summary.key} ')
            #extract file name suffix
            aws_file_name = object_summary.key
            suffix_index = aws_file_name.rindex(".")
            cur_suffix = aws_file_name[suffix_index + 1::]
            
            #only if suffix matched
            if (suffix == "" or cur_suffix == suffix):
                # print("matched: " + aws_file_name)

                #extract file name without folder
                last_folder_index = aws_file_name.rindex("/")
                file_name = aws_file_name[last_folder_index + 1::]

                #calc local name
                local_full_file_name = download_folder + file_name

                #download
                bucket.download_file(aws_file_name, local_full_file_name)
                print(f'{local_full_file_name} downloaded')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print(traceback.format_exc())
    except Exception as e:
        print(traceback.format_exc())

# def donwload(bucket_name: str, aws_folder: str, suffix: str, download_folder="" ) -> list:
#     try:
#         _download(bucket_name, aws_folder, suffix, download_folder) 

#     except Exception as e:
#         print("download from AWS failed", e)