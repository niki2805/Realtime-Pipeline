from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType


def write_stream(df: DataFrame, foreach_batch_function) -> StreamingQuery:
    return df.writeStream \
        .foreachBatch(foreach_batch_function) \
        .outputMode("update") \
        .start()


def get_spark_session():
    spark = SparkSession.builder.master("local[1]") \
        .appName('DataPipeline') \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    return spark


def get_streaming_dataframe(spark, topic: str) -> DataFrame:
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .load() \
        .selectExpr("CAST(value AS STRING)")

    return df


def get_event_schema(attributes_type) -> StructType:
    return StructType().add("event_name", StringType()).add("attributes", attributes_type())


def get_add_to_list_attributes() -> StructType:
    attributes_type = StructType() \
        .add("video_id", IntegerType()) \
        .add("user_id", IntegerType()) \
        .add("row", StringType()) \
        .add("ip", StringType()) \
        .add("timestamp", TimestampType())

    return get_event_schema(attributes_type)
