import time
from pyspark.sql import SparkSession, Window
import pyspark.sql.functions as func
from pyspark.ml.recommendation import ALS
from pyspark.ml.recommendation import ALSModel
from pyspark.ml.feature import StringIndexer
from pyspark.mllib.evaluation import RankingMetrics
import os 

def preprocess_data(spark, filter_thresh=100):
    train_raw = spark.read.parquet("hdfs:/user/jt4686_nyu_edu/listenbrainz/interactions_train_fixed.parquet").cache()
    val = spark.read.parquet(f"hdfs:/user/jt4686_nyu_edu/listenbrainz/interactions_val_fixed.parquet")

    start = time.time()
    print("Computing Unique Tracks...")
    unique_tracks = train_raw.groupBy(["cleaned_id"]).count(). \
        filter(func.col("count") > filter_thresh). \
        coalesce(5). \
        rdd.map(lambda x: x[0]). \
        collect()
    end = time.time()
    print(f'Time Elapsed: {end - start}')

    start = time.time()
    print("Filtering Training Data...")
    train = train_raw.filter(func.col("cleaned_id").isin(unique_tracks)). \
        groupBy(["user_id", "cleaned_id"]).count()
    end = time.time()
    print(f'Time Elapsed: {end - start}')

    # ALS requires track_ids to be INT, one hot encode hash values
    indexer = StringIndexer(inputCol='cleaned_id', outputCol='track_index', handleInvalid='keep')
    indexer_fit = indexer.fit(train)
    start = time.time()
    print("Encoding Train/Val Data...")
    train_indexed = indexer_fit.transform(train)
    val_indexed = indexer_fit.transform(val)
    end = time.time()
    print(f'Time Elapsed: {end - start}')

    return train_indexed, val_indexed


def als(train, rank=10, iter=10, reg=0.01):

    start = time.time()
    print("Training ALS Model...")
    als = ALS(rank=rank, maxIter=iter, regParam=reg, implicitPrefs=True, userCol='user_id',
              itemCol='track_index', ratingCol='count', nonnegative=True, coldStartStrategy='drop', seed=510)
    model = als.fit(train)
    end = time.time()
    print(f'Model Training Time: {end - start}')

    users = eval.dropDuplicates(['user_id'])
    start = time.time()
    print("Computing Recommendations...")
    recs = model.recommendForUserSubset(users, 100). \
        withColumn('track_recs', func.col("recommendations.track_index")). \
        select("user_id", "track_recs")
    end = time.time()
    print(f'Time Elapsed: {end - start}')

    # Ground truth: All actual user interactions
    ground_truth = eval.dropDuplicates(["user_id", "track_index"]).\
        groupBy("user_id"). \
        agg(func.collect_list("track_index"))

    print("Formatting Recommendation Results...")
    # Format data for RankingMetrics
    eval_df = recs.join(ground_truth, on="user_id"). \
        rdd.map(lambda x: (x[1], x[2]))

    print("Computing Evaluatiion Metrics...")
    metrics1 = "{:.3f}".format(RankingMetrics(eval_df).precisionAt(100))
    metrics2 = "{:.3f}".format(RankingMetrics(eval_df).meanAveragePrecisionAt(100))
    metrics3 = "{:.3f}".format(RankingMetrics(eval_df).ndcgAt(100))

    return metrics1, metrics2, metrics3


if __name__ == "__main__":
    path = "./save_model"
    print("-"*50)
    print(path)
    print("-"*50)
    rank=10
    iter=10
    reg=0.01

    spark = SparkSession.builder.appName("final_project").getOrCreate()
    model = ALS(rank=rank, maxIter=iter, regParam=reg, implicitPrefs=True, userCol='user_id',
              itemCol='track_index', ratingCol='count', nonnegative=True, coldStartStrategy='drop', seed=510)
    model.write().overwrite().save(path)
    #model.save(path)
    #ALSModel.load(path)
    print("done i guess")
    # train, eval = preprocess_data(spark, filter_thresh=500)
    # train.cache()
    # eval.cache()
    #metric_names = ['Precision@100', 'MAP', 'NDCG']
    #metrics = als(train, eval, rank=200, iter=12, reg=0.3)
    #for i, metric in enumerate(metrics):
    #    print(f"{metric_names[i]}: {metric}")