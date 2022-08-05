import boto3 
import traceback


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

def upload(files: list, dest_folder: str, bucket_name: str) -> bool:
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