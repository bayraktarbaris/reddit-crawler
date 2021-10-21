from pyspark.shell import spark
from pyspark.shell import sqlContext
from pyspark.sql.functions import from_unixtime, col, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, FloatType

from src.utils.singleton import Singleton


class SubmissionService(metaclass=Singleton):
    def __init__(self):
        self.schema = StructType([
            StructField("title", StringType(), True),
            StructField("selftext", StringType(), True),
            StructField("id", StringType(), True),
            StructField("upvote_ratio", FloatType(), True),
            StructField("num_comments", IntegerType(), True),
            StructField("link_flair_text", StringType(), True),
            StructField("score", IntegerType(), True),
            StructField("created_utc", LongType(), True),
            StructField("author", StringType(), True),
            StructField("author_fullname", StringType(), True),
            StructField("retrieved_on", LongType(), True),
        ])
        self.file_name = "../data/submissions.json"
        self.save_path = "../data/submissions"

    def write(self):
        # if "author": "[deleted]", we can clean data, but i didn't clean it
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
