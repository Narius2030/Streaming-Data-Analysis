from typing import Any
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType 
from pyspark.sql.functions import *
from pyspark.ml.feature import StringIndexer, HashingTF, IDF,Tokenizer, VectorIndexer

class TransformText():
    def __init__(self, spark:SparkSession, data_path:str) -> None:
        schema = StructType() \
                .add("tweet_id", IntegerType(), False) \
                .add("entity", StringType(), True) \
                .add("sentiment", StringType(), True)  \
                .add("content", StringType(), True)
        
        self.tweets = spark.read.option("header", True) \
                .schema(schema) \
                .csv(data_path)
    
    def fit(self):
        tweets = self.clean_data(self.tweets, 'content')
        tweets = self.clean_data(tweets, 'sentiment')
        encoded_tweets = self.label_encoder(tweets, 'sentiment', 'sentiment_label')
        tfidf_tweets = self.tfidf_transform(encoded_tweets, 'content', 20)
        vectorized_tweets = self.vectorindex_transform(tfidf_tweets, 'features', 4)
        return vectorized_tweets
    
    def label_encoder(self, tweets, inputCol:str, outputCol:str) -> DataFrame:
        # .setHandleInvalid('skip')
        encoder = StringIndexer(inputCol=inputCol, outputCol=outputCol).fit(tweets)
        encoded_tweets = encoder.transform(tweets)
        print(encoded_tweets.groupBy(outputCol).count().show())
        return encoded_tweets
    
    def clean_data(self, tweets, feature:str) -> DataFrame:
        cleaned_tweets = tweets.withColumn(feature, when(isnull(col(feature)), "") \
                        .otherwise(col(feature)))
        return cleaned_tweets
    
    def tfidf_transform(self, tweets, inputCol:str, numFeatures:int=20) -> DataFrame:
        tokenizer = Tokenizer(inputCol=inputCol, outputCol='words')
        tokenized_tweets = tokenizer.transform(tweets)

        hashingTF = HashingTF(inputCol="words", 
                              outputCol="raw_features", 
                              numFeatures=numFeatures)
        featurized_data = hashingTF.transform(tokenized_tweets)

        idf = IDF(inputCol="raw_features", outputCol="features")
        tfidf_tweets = idf.fit(featurized_data).transform(featurized_data)
        return tfidf_tweets
    
    def vectorindex_transform(self, tweets, inputCol:str, maxCategories:int=4) -> DataFrame:
        featureIndexer = VectorIndexer(inputCol=inputCol, 
                                       outputCol="indexedFeatures", 
                                       maxCategories=maxCategories).fit(tweets)
        vectorized_tweets = featureIndexer.transform(tweets)
        return vectorized_tweets