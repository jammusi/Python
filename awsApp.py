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

def delete(bucket_name: str, aws_folder: str, file_name: str) -> bool:

    result = False

    try:

        pamas_valid = _is_valid_param("file_name", file_name)
        pamas_valid = pamas_valid and _is_valid_param("aws_folder", aws_folder)
        pamas_valid = pamas_valid and _is_valid_param("bucket_name", bucket_name)

        if pamas_valid:
            
            valid_aws_folder = _validate_aws_folder_name(aws_folder)

            full_file_name = f'{valid_aws_folder}{file_name}'
            
            result = _delete_all_versions_of_object(bucket_name, full_file_name)
    
    except botocore.exceptions.ClientError as e:
        print(traceback.format_exc())
        result = False
        
    except Exception as e:
        print(traceback.format_exc())
        result = False

    return result

def _is_valid_param(param_name: str, param_val) -> bool:

    is_valid = param_val is not None and len(param_val) > 0

    if not is_valid:
        print(f"Error {param_name} value is: {param_val}")

    return is_valid

def _delete_all_versions_of_object(bucket_name, full_file_name) -> bool:

    is_success = True

    s3_client = boto3.client("s3")
    
    get_obj_ver_response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=full_file_name)
    
    print(f"AWS Get versions response: {get_obj_ver_response}")

    objects_to_delete = []
    
    for version in get_obj_ver_response.get("Versions",[]):
        objects_to_delete.append({"Key": full_file_name, "VersionId": version["VersionId"]})
    
    for delete_marker in get_obj_ver_response.get("DeleteMarkers", []):
        objects_to_delete.append({"Key": full_file_name, "VersionId": delete_marker["VersionId"]})

    # delete objects in batches of 1000
    del_per_call = 1000

    if len(objects_to_delete) > 0:
        for i in range(0, len(objects_to_delete), del_per_call):

            cur_objects_to_del = objects_to_delete[i: i + del_per_call]

            # response = s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects_to_delete[i:i+1000]})
            response = s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": cur_objects_to_del})

            cur_result = _handle_delete_response(response)

            # update finla result
            is_success = is_success and cur_result

            if not is_success:
                break
    else:
        
        print(f"File: {full_file_name} not found")
        is_success = False

    return is_success

def _handle_delete_response(response: dict) -> bool:

    deleted_key = "Deleted"
    error_key = "Error"
    is_deleted = False

    # print (f"Current response: {response}")
    
    if response.__contains__(error_key):
        # error occured
        is_deleted = False
    elif response.__contains__(deleted_key):
        is_deleted = len(response[deleted_key]) > 0

    return is_deleted
