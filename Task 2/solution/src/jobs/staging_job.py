import sys
import pandas as pd
from datetime import datetime
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col

from solution.src.config.logger import logger
from solution.src.resources.file_manager import FileManagerResource

def main():
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'ENERGY_BUCKET', 'PREFIX'])

    spark_context = SparkContext.getOrCreate()
    glue_context = GlueContext(spark_context)
    spark = glue_context.spark_session
    file_manager = FileManagerResource()

    raw_files = file_manager.list_objects(bucket=args['ENERGY_BUCKET'], prefix=args['PREFIX'])

    if 'Contents' not in raw_files or not raw_files['Contents']:
        logger.info("There are no files to process")
        return
    
    load_date = datetime.now().strftime('%Y-%m-%d')

    for file in raw_files['Contents']:
        key = file['Key']
        if key.endswith('.csv'):
            file_name = key.split('/')[-1]
            local_path = f"temp/{file_name}"

            file_manager.download_object(key, local_path)

            df = pd.read_csv(local_path)

            for column in df.select_dtypes(include="object").columns:
                df[column] = df[column].str.strip().str.lower()
            
            if 'email' in df.columns:
                df['email'] = df['email'].str.lower()

            spark_df = spark.createDataFrame(df)

            new_cols = [c.strip().lower().replace(' ', '_') for c in spark_df.columns]
            spark_df = spark_df.toDF(*new_cols)

            if 'precio' in spark_df.columns:
                spark_df = spark_df.filter(col('precio').isNotNull() & (col('precio') > 0))

            if 'cantidad' in spark_df.columns:
                spark_df = spark_df.filter(col('cantidad').isNotNull() & (col('cantidad') > 0))

            output_path = f"s3://{args['ENERGY_BUCKET']}/staging/{load_date}/{file_name.replace('.csv', '')}"
            spark_df.write.mode("overwrite").parquet(output_path)

            logger.info("File processed and saved")
  
if __name__ == "__main__":
    main()