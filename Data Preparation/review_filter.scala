import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext

object review_filter {

  def main(args: Array[String]) : Unit = {
    val spark_config = new SparkConf().setAppName("review_filter").setMaster("local[2]")
    val spark_context = new SparkContext(spark_config)
    val sqlContext = new SQLContext(spark_context)

    val review = sqlContext.read.json(args(0))
    val raw_business = spark_context.textFile(args(1))
    //println("count: " + raw_business.count())

    val business = raw_business.map(x => x.toString).collect().toSet

    val vegas = review.select( "review_id","user_id", "business_id", "stars", "date", "useful", "text").repartition(1)

    var vegas_reviews = vegas.select("user_id", "business_id", "stars").rdd.map(x => (x(0), x(1).toString, x(2))).filter(x => business.contains(x._2))
      .map(x => x._1 + "," + x._2 + "," + x._3).repartition(1)

    if(args(2) == "ratings") {
      spark_context.parallelize(Seq("user_id,business_id,rating")).union(vegas_reviews).repartition(1).saveAsTextFile("ratings")
    }

    if(args(2) == "reviews") {
      vegas_reviews = vegas.select("user_id", "business_id", "stars", "text").rdd
        .map(x => (x(0), x(1).toString, x(2), x(3))).filter(x => business.contains(x._2))
        .map(x => (x._1, x._2, x._3, x._4.toString.toLowerCase()
        .replaceAll("""([\p{Punct}&&[^.]]|\b\p{IsLetter}{1,2}\b)""", "").replaceAll("""([\p{Cntrl}])""", " ")
        .replaceAll("[.]", "").replaceAll("[ ]{2,}", " ").trim))
        .map(x => x._1 + "," + x._2 + "," + x._3 + "," + x._4).repartition(1)
      spark_context.parallelize(Seq("user_id,business_id,rating,review")).union(vegas_reviews).repartition(1).saveAsTextFile("reviews")
    }

  }
}