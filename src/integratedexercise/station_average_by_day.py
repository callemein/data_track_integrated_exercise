from pyspark.sql import SparkSession
from pyspark.sql.functions import date_format, to_date, col, avg

spark = (
    SparkSession.builder.config(
        "spark.jars.packages",
        ",".join(
            [
                "org.apache.hadoop:hadoop-aws:3.3.1",
            ]
        ),
    )
    .config(
        "fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
    )
    .getOrCreate()
)

s3_bucket = "data-track-integrated-exercise"
s3_prefix = "timothy-data"

s3_table_stations = f"s3a://{s3_bucket}/{s3_prefix}/stations.csv"
s3_table_timeseries = f"s3a://{s3_bucket}/{s3_prefix}/timeseries.csv"
s3_table_categories = f"s3a://{s3_bucket}/{s3_prefix}/categories.csv"

s3_table_data_points = f"s3a://{s3_bucket}/{s3_prefix}/data/*/data.parquet"
s3_table_clean_data_points = (
    f"s3a://{s3_bucket}/{s3_prefix}/clean/aggregate_station_by_day/"
)

df_stations = (
    spark.read.format("csv")
    .options(header="true", inferSchema="true")
    .load(s3_table_stations)
)
df_timeseries = (
    spark.read.format("csv")
    .options(header="true", inferSchema="true")
    .load(s3_table_timeseries)
)
df_categories = (
    spark.read.format("csv")
    .options(header="true", inferSchema="true")
    .load(s3_table_categories)
)

df = spark.read.parquet(s3_table_data_points)

# - add a datetime column that converts the epoch millis to a datatime (string representation)
df = df.withColumn("DATETIME", date_format("TIME", "yyyy-MM-dd HH:mm"))
df = df.withColumn("DATE", to_date("TIME"))

# - Calculate the average of the measurements for a specific station by day

# Prepare timeseries
df_timeseries = df_timeseries.drop(
    "PROCEDURE_ID",
    "UOM",
    "FIRST_VALUE",
    "FIRST_VALUE_TIME",
    "LAST_VALUE",
    "LAST_VALUE_TIME",
)

df_stations = df_stations.drop(
    "LONGITUDE",
    "LATITUDE",
)

# Join the timeseries and the data_points
df = df.join(df_timeseries, ["TIMESERIES_ID"])

df = df.withColumn('DATE', to_date('TIME'))

df = df.groupBy("DATE", "TIMESERIES_ID", "STATION_ID", "CATEGORY_ID").agg(avg("VALUE").alias("AVG_VALUE"))
df = df.join(df_stations, ["STATION_ID"])
df = df.join(df_categories, ["CATEGORY_ID"])

df.show(5)
df.printSchema()

# TODO: How can I partitionBy by date without saving the date along with the timestamp?
df.write.option("header", True).partitionBy("DATE").mode("overwrite").parquet(s3_table_clean_data_points)


