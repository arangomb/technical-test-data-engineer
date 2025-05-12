from datetime import datetime

from solution.src.config.logger import logger
from solution.src.resources.file_manager import FileManagerResource

class RawLoaderService():

    def __init__(self):
        self.file_manager = FileManagerResource()

    def load_raw_data(self, src_bucket_name:str, file_key:str):

        final_path = self._get_final_path(file_key)

        try:
            self.file_manager.copy_object(file_key, final_path, src_bucket_name)
            return "File loaded to energy bucket successfully"
        except Exception as e:
            logger.info(f"Error processing file in raw process: {e}")
            raise
    
    def _get_final_path(self, file_key:str):

        file_type = file_key.split('/')[0] if '/' in file_key else 'noType'
        filename = file_key.split('/')[-1]
        load_date = datetime.now().strftime('%Y-%m-%d')

        return f"raw/{file_type}/{load_date}/{filename}"