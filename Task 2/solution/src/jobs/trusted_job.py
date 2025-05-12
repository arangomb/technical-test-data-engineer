import sys
from datetime import datetime
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, to_date, round

from solution.src.config.logger import logger

def main():
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "ENERGY_BUCKET", "STAGING_PREFIX", "TRUSTED_PREFIX"])

    spark_context = SparkContext.getOrCreate()
    glue_context = GlueContext(spark_context)
    spark = glue_context.spark_session

    load_date = datetime.now().strftime('%Y-%m-%d')

    staging_path = f"s3://{args['ENERGY_BUCKET']}/{args['STAGING_PREFIX']}/*/*.parquet"
    df = spark.read.parquet(staging_path)

    df = (
        df
        .withColumn("fecha_transaccion",to_date(col("fecha_transaccion"), "yyyy-MM-dd"))
        .withColumn("precio", col("precio").cast("double"))
        .withColumn("cantidad", col("cantidad").cast("double"))
    )

    df = (
        df
        .withColumn("monto_total", round(col("precio") * col("cantidad"), 2))
    )

    window_cols = ["id_cliente", "id_transaccion"]
    df = df.dropDuplicates(window_cols)

    output_path = f"s3://{args['ENERGY_BUCKET']}/{args['TRUSTED_PREFIX']}/{load_date}"
    df.write.mode("overwrite").parquet(output_path)

    logger.info(f"Trusted data saved")

if __name__ == "__main__":
    main()