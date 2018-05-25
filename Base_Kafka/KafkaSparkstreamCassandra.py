import os
import threading, logging, time
import multiprocessing

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from kafka import KafkaConsumer, KafkaProducer

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
    def stop(self):
        self.stop_event.set()
    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',api_version= (0,10))
        while not self.stop_event.is_set():
            message = time.strftime("%Y-%m-%d %H:%M:%S")
            producer.send('test', message)
            time.sleep(1)
        producer.close()

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
    def stop(self):
        self.stop_event.set()
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000,
                                 api_version = (0, 10))
        consumer.subscribe(['test'])
        while not self.stop_event.is_set():
            for message in consumer:
                data = sc.parallelize(message.value.split(","))
                rows = data.map(lambda x: Row(time_sent=x, time_received=time.strftime("%Y-%m-%d %H:%M:%S")))
                rows.foreach(g)
                # rows.saveAsTextFile("/home/guest/jsb")
                # rows.foreach(saveToCassandra)
                if self.stop_event.is_set():
                    break
        consumer.close()

def g(x):
    print(x)

def saveToCassandra(rows):
    if not rows.isEmpty():
        sqlContext.createDataFrame(rows).write \
            .format("org.apache.spark.sql.cassandra") \
            .mode('append') \
            .options(table="sent_received", keyspace="test_time") \
            .save()

def main():
    tasks = [
        Producer(),
        Consumer()
    ]
    for t in tasks:
        t.start()
    time.sleep(10)
    for task in tasks:
        task.stop()
    for task in tasks:
        task.join()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    conf = SparkConf() \
        .setAppName("Streaming test") \
        .setMaster("local[2]") \
        .set("spark.cassandra.connection.host", "localhost")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 5)
    main()