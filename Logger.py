#region IMPORTS
from datetime import datetime
import inspect
import os
#endregion

#region CLASS
class Logger:

    #region LOCALS
    _log_full_file_name = ""
    _log_short_file_name = ""
    _logs_dir_archive = ""
    _logs_dir = ""
    # _max_file_zize_bytes = 1024 * 1024 * 1024 #1Gb
    _max_file_zize_bytes = 1024 * 1024  #1Mb
    #endregion

    #region API
    
    def __init__(self):

        #region LOGS FOLDERS
        folder = os.path.dirname(os.path.realpath(__file__)) + "/Log Files/"

        self._logs_dir = folder
        self._logs_dir_archive = folder + "Archived/"

        os.makedirs(self._logs_dir, exist_ok=True)
        os.makedirs(self._logs_dir_archive, exist_ok=True)
        #endregion

        self._create_new_log_file()

    def write_to_log(self, log, log_to_console = True):

        self._check_file_size()

        file = open(self._log_full_file_name, 'a')

        #region EXTRACT CALLING FUNCTION DETAILS 
        
        #call function
        curframe = inspect.currentframe()
        calling_frame = inspect.getouterframes(curframe, 2)
        calling_function =  calling_frame[1][3]

        # calling object
        calling_obj = ""
        f2 = inspect.currentframe().f_back
        if "self" in f2.f_locals:
            #calling object is a class - get class name
            calling_obj = type(f2.f_locals["self"]).__name__
        else:
            #not a class - module name
            calling_obj = inspect.stack()[-1].filename

        del curframe, calling_frame
        #endregion

        #region WRITE TO FILE
        time_now = datetime.utcnow().strftime("%d/%m/%y %H:%M:%S.%f")
        log_to_write = f"{time_now} {calling_obj}.{calling_function}: {log} \n"

        file.write(f"{log_to_write}\n")
        file.close()
        #endregion

        #region WRITE TO CONSOLE
        if log_to_console:
            print(f"{calling_function}:{log}")
        #endregion

    def get_log_file_name(self) -> str:
        return self._log_full_file_name
    
    
    #endregion

    #region HELPERS
    def _check_file_size(self):
        bytes = os.stat(self._log_full_file_name).st_size
        if bytes > self._max_file_zize_bytes:
            self._create_new_log_file()

    def _create_new_log_file(self) -> str:

        #archive old file
        self._archive_old_log(self._log_full_file_name)

        #create new file
        time_now = datetime.utcnow().strftime("%d%m%y-%H%M%S")
        file_name = "worker_log_" + str(time_now) + '.txt'
        full_file_name = self._logs_dir + file_name
        file = open(full_file_name, 'w')
        file.close()

        # CACHE
        self._log_short_file_name = file_name   
        self._log_full_file_name = full_file_name   
    
    def _archive_old_log(self, full_file_name: str):

        import gzip
        import shutil
                
        if full_file_name is not None and os.path.exists(full_file_name):

            #region ARCHIVE CURRENT LOG FILE
            with open(full_file_name, 'rb') as f_in:
            
                full_target_zip_name = f"{full_file_name}.gz"

                #region COMPRESS
                with gzip.open(full_target_zip_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                #endregion
                
                #region MOVE COMPRESS FILE TO ARCHIVE FOLDER
                if self._logs_dir_archive != self._logs_dir:
                    shutil.move(full_target_zip_name, self._logs_dir_archive)
                #endregion
            
            #endregion

            #region DELETE UNCOMRESSED FILE
            os.remove(full_file_name)
            #endregion

    #endregion

#endregion


#region API
logger2 = Logger()
#endregion