import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext

object splitter {

  def main(args: Array[String]) : Unit = {
    val spark_config = new SparkConf().setAppName("splitter").setMaster("local[2]")
    val spark_context = new SparkContext(spark_config)
    val sqlContext = new SQLContext(spark_context)

    val review = sqlContext.read.json(args(0))
    val raw_business = spark_context.textFile(args(1))
    val business = raw_business.map(x => x.toString).collect().toSet

    val vegas = review.select( "review_id","user_id", "business_id", "stars", "date", "useful", "text").repartition(1)

    var vegas_reviews = vegas.select("user_id", "business_id", "stars").rdd.map(x => (x(0), x(1).toString, x(2))).filter(x => business.contains(x._2))
      .map(x => x._1 + "," + x._2 + "," + x._3).repartition(1)

    val vegas_reviews_date = vegas.select("user_id", "business_id", "stars", "date").rdd.map(x => (x(0), x(1).toString, x(2), (x(3).toString.slice(0, 4) + x(3).toString.slice(5, 7) + x(3).toString.slice(8, 10)).toInt)).filter(x => business.contains(x._2))
      .sortBy(x => x._4)

    if(args(2) == "U") {
      val input_user = args(4)
      val percentage = args(3).toFloat

      val user_history = vegas_reviews_date.filter(x => x._1 == input_user).zipWithIndex()
      val filter_pos = (user_history.count() * percentage).toInt
      val filter_date = user_history.filter(x => x._2 == filter_pos).map(x => x._1._4).first()
      val train_set = vegas_reviews_date.filter(x => x._4 <= filter_date).map(x => x._1 + "," + x._2 + "," + x._3)
      val test_set = vegas_reviews_date.filter(x => x._4 > filter_date).map(x => x._1 + "," + x._2 + "," + x._3)
      spark_context.parallelize(Seq("user_id,business_id,rating")).union(train_set).repartition(1).saveAsTextFile("train_set")
      println("training data/total data = " + (train_set.count().toFloat/vegas_reviews.count().toFloat) * 100 + "%")
    }

    if(args(2) == "D") {
      val percentage = args(3).toFloat
      val history = vegas_reviews_date.zipWithIndex()
      val filter_pos = (history.count() * percentage).toInt
      val filter_date = history.filter(x => x._2 == filter_pos).map(x => x._1._4).first()

      val train_set = vegas_reviews_date.filter(x => x._4 <= filter_date).map(x => x._1 + "," + x._2 + "," + x._3)
      val test_set = vegas_reviews_date.filter(x => x._4 > filter_date).map(x => x._1 + "," + x._2 + "," + x._3)
      spark_context.parallelize(Seq("user_id,business_id,rating")).union(train_set).repartition(1).saveAsTextFile("train_set")
      println("training data/total data = " + (train_set.count().toFloat/vegas_reviews.count().toFloat) * 100 + "%")
    }

  }
}