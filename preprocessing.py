from typing import Any
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType 
from pyspark.sql.functions import *
from pyspark.ml.feature import StringIndexer, HashingTF, IDF,Tokenizer, VectorIndexer, StopWordsRemover

class TransformText():
    def __init__(self, label:str, context_col:str) -> None:
        self.label = label
        self.context_col = context_col
                
    def data_loader(self, schema, spark:SparkSession, data_path:str):
        tweets = spark.read.option("header", True) \
                .schema(schema) \
                .csv(data_path)
        return tweets
    
    def transform(self, tweets):
        tweets = self.clean_data(tweets, self.context_col)
        tweets = self.clean_data(tweets, self.label)
        encoded_tweets = self.label_encoder(tweets, self.label, f'{self.label}_label')
        tfidf_tweets = self.tfidf_transform(encoded_tweets, self.context_col, 20)
        return tfidf_tweets
    
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



class CleanText():
    def __init__(self, outputCol:list|str, target:str=None) -> None:
        self.outputCol = outputCol
        self.target = target
    
    def transform(self, tweets):
        stopwords = self.get_stopwords('./data/stopword_en.txt')
        temp = self.remove_stopwords(tweets, stopwords, 'content')
        result = self.remove_redudance(temp, 'content')
        return result
    
    def get_stopwords(self, path:str) -> list:
        stopwords = []
        with open(file=path, mode='r') as file:
            try:
                stopwords = file.readlines()
                for idx, word in enumerate(stopwords):
                    stopwords[idx] = word[:len(word)-1:]
            except Exception as ex:
                print(ex)
        return stopwords
    
    def remove_stopwords(self, tweets, stopwords:list, inputCol:str) -> DataFrame:
        temp = tweets.withColumn('tokens', split(inputCol, ' '))
        remover = StopWordsRemover(stopWords=stopwords, inputCol='tokens', outputCol="stop")
        temp = remover.transform(temp).select(*self.outputCol, array_join("stop", " ").alias(inputCol))
        return temp
    
    def remove_redudance(self, tweets, inputCol:str):
        temp = tweets.withColumn(
            f'cleaned_{inputCol}', 
            translate(inputCol, '!"#$%&\'()*+,-./:;<=>?@[\\]^_{|}~', '')
        )
        temp = temp.withColumn(
            f'cleaned_{inputCol}',
            regexp_replace(regexp_replace(f'cleaned_{inputCol}', "[^\x00-\x7F]+", ""), '""', '')
        )
        temp = temp.withColumn(
            f'cleaned_{inputCol}',
            lower("cleaned_content")
        )
        return temp