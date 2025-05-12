from pyspark.sql import SparkSession

from solution.src.config.env import ENERGY_BUCKET_NAME

def main():

    spark = SparkSession.builder.appName("TrustedDataSQLQueries").getOrCreate()
    trusted_path = f"s3://{ENERGY_BUCKET_NAME}/trusted/*/*.parquet"
    df = spark.read.parquet(trusted_path)

    df.createOrReplaceTempView("trusted_data")

    spending_per_customer = spark.sql("""
        SELECT
            cliente_id,
            SUM(monto_total) AS monto_total_facturado
        FROM trusted_data
        GROUP BY cliente_id
        ORDER BY monto_total_facturado DESC
    """)
    spending_per_customer.show()

    capital_clients = spark.sql("""
        SELECT *
        FROM trusted_data
        WHERE ciudad = 'bogota'
    """)
    capital_clients.show()

    specific_transactions = spark.sql("""
        SELECT *
        FROM trusted_data
        WHERE fecha_transaccion = '2025-04-29'
    """)
    specific_transactions.show()

    processed_transactions = spark.sql("""
        SELECT *
        FROM trusted_data
        WHERE estado = 'procesada' AND tipo_energia = 'eolica'
    """)
    processed_transactions.show()

if __name__ == "__main__":
    main()