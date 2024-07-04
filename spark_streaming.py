from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Streaming Socket movie data") \
    .master("local[*]") \
    .getOrCreate()

print(spark)

streaming_df = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", "9999") \
    .load()
    
# Check the schema
print(streaming_df.printSchema())

# Write the output to console sink to check the output
writing_df = streaming_df.writeStream \
    .format("console") \
    .outputMode("update") \
    .start()

# Start the streaming application to run until the following happens
# 1. Exception in the running program
# 2. Manual Interruption
writing_df.awaitTermination()