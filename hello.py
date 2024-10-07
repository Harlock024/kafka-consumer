from pyspark.sql import SparkSession
#uri = "mongodb+srv://adsoft:adsoft-sito@cluster0.kzghgph.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://adsoft:adsoft-sito@cluster0.kzghgph.mongodb.net/memes?retryWrites=true&w=majority"
uri_out = "mongodb+srv://adsoft:adsoft-sito@cluster0.kzghgph.mongodb.net/memes.memes_summary?retryWrites=true&w=majority"

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("hello_spark")\
        .config("spark.mongodb.read.connection.uri", uri)\
        .config("spark.mongodb.write.connection.uri", uri_out)\
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2_12-10.1.1:3.3.2')\
        .config('spark.jars.packages', 'org.mongodb.spark:bson-3.8.1:3.3.2')\
        .getOrCreate()
                                                        #mongo-spark-connector_2.12-2.4.2
        

#        config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0").\

    print("Hello spark world, welcome adsoft ... ")
#    df = spark.read.format("mongodb").load()
#com.mongodb.spark.sql.DefaultSource
    df_memes_info = spark.read\
    .format("mongodb")\
    .option("uri", uri)\
    .option("database","memes")\
    .option("collection", "memes_info")\
    .load()


    df_memes_info.printSchema()
    df_memes_info.createOrReplaceTempView("memes_info")

    group_query = 'SELECT name, COUNT(name) as n FROM memes_info GROUP BY name';
    #group_query ='SELECT name FROM memes_info';

    df_memes_sum = spark.sql(group_query)
    df_memes_sum.printSchema();
    print(df_memes_sum.columns);
#    print(df_memes_sum.show());

    #df_group_name.createOrReplaceTempView("group_name")
    
    #df_group_name.foreach(lambda x: 
    #    print (x[0])
    #) 

#    for item in df_memes_info:
#      print (item)
    #df_memes_summary = spark.read\
    #.format("mongodb")\
    #.option("uri", uri)\
    #.option("database","memes")\
    #.option("collection", "memes_summary")\
    #.load()

    #created a data frame of two records

    
    columns = ["name","n"]
    data = [("Java", 20000)]

#    df = spark.createDataFrame([
#      Row(name = 'adsoft', n = 10),
#      Row(name = 'adsoftsito',  n = 9)
#    ])


    df = spark.createDataFrame(data).toDF(*columns)
    df.printSchema();
#    df.show();
    #writing to the database
    df.write\
    .format("mongodb")\
    .mode("append")\
    .option("uri", uri_out)\
    .option("database","memes")\
    .option("collection", "memes_summary")\
    .save()
  

    #  people.write.format("mongodb").mode("append").option("database",
    # "people").option("collection", "contacts").save()


#    df.write.format("mongodb").mode("append").option("uri", uri).save()

    spark.stop()
