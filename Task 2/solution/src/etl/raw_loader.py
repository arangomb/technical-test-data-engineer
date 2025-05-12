from urllib.parse import unquote_plus

from solution.src.config.logger import logger
from solution.src.services.raw_loader import RawLoaderService

def raw_loader_handler(event, context):

    records = event.get('Records', [])

    for record in records:
        src_bucket = record['s3']['bucket']['name']
        file_key = unquote_plus(record['s3']['object']['key'])

        if not file_key.lower().endswith('.csv'):
            logger.info("Omitting non-CSV file")
            continue

        return RawLoaderService().load_raw_data(src_bucket, file_key)