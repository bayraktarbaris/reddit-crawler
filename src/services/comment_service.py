from pyspark.shell import sqlContext, spark
from pyspark.sql.functions import from_unixtime, col, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType

from src.utils.singleton import Singleton


class CommentService(metaclass=Singleton):
    def __init__(self):
        self.schema = StructType([
            StructField("body", StringType(), True),
            StructField("id", StringType(), True),
            StructField("score", IntegerType(), True),
            StructField("author", StringType(), True),
            StructField("author_fullname", StringType(), True),
            StructField("parent_id", StringType(), True),
            StructField("created_utc", LongType(), True),
        ])
        self.file_name = "../data/comments.json"
        self.save_path = "../data/comments"

    def write(self):
        # if "author": "[deleted]" or "body": "[removed]", we can clean data, but i didn't clean it
        df = sqlContext.read.json(self.file_name, self.schema)
        df_with_date = df.withColumn("date", from_unixtime(col("created_utc")))
        df_with_date \
            .withColumn("year", year(col("date"))) \
            .withColumn("month", month(col("date"))) \
            .withColumn("day", dayofmonth(col("date"))) \
            .drop("date") \
            .write \
            .partitionBy("year", "month", "day") \
            .mode("overwrite") \
            .format("parquet") \
            .save(self.save_path)

    def read(self):
        df_submissions = spark.read.parquet(self.save_path)
        df_submissions.show()
