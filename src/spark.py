import sys
import time

from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json
from pyspark.sql.types import StringType

import sparkutils


class EventsCount:
    TABLE = "events_count"

    def __init__(self, topic: str):
        self.topic = topic
        self.spark = sparkutils.get_spark_session()
        self.start_time = time.time()

    def foreach_batch_function(self, dataframe: DataFrame, epoch_id: int):
        start_time = time.time()
        dataframe.show()
        print("Processing Time:", time.time() - start_time)
        dataframe.write \
            .format("org.apache.spark.sql.cassandra") \
            .mode("append") \
            .options(table=EventsCount.TABLE, keyspace=self.topic + "_keyspace") \
            .save()

    def start_streaming(self):
        df = sparkutils.get_streaming_dataframe(self.spark, self.topic)
        df.printSchema()

        schema = sparkutils.get_event_schema(StringType)

        df = df.select(from_json(col="value", schema=schema).alias("event")).select("event.*")

        count = df.groupby("event_name").count()

        sparkutils.write_stream(count, self.foreach_batch_function).awaitTermination()


if __name__ == '__main__':
    topic = sys.argv[1]
    print("Running spark streaming for", topic)
    EventsCount(topic).start_streaming()
