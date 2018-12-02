import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext

object user_dict {

  def main(args: Array[String]) : Unit = {
    val spark_config = new SparkConf().setAppName("user_dict").setMaster("local[2]")
    val spark_context = new SparkContext(spark_config)
    val sqlContext = new SQLContext(spark_context)

    val review = sqlContext.read.json(args(0))
    val tips = sqlContext.read.json(args(1))
    val raw_business = spark_context.textFile(args(2))
    val business = raw_business.map(x => x.toString).collect().toSet

    val vegas_reviw = review.select("user_id", "business_id").repartition(1).rdd.map(x => (x(0).toString, x(1).toString)).filter(x => business.contains(x._2))
    val vegas_tip = review.select("user_id", "business_id").repartition(1).rdd.map(x => (x(0).toString, x(1).toString)).filter(x => business.contains(x._2))

    vegas_reviw.union(vegas_tip).map(x => (x._2, x._1)).distinct().groupByKey().map(x => (x._1, x._2.toSet)).map(x => x._1 + "," + x._2).repartition(1).saveAsTextFile("Strip_business_user_dict")
    vegas_reviw.union(vegas_tip).distinct().groupByKey().map(x => (x._1, x._2.toSet)).map(x => x._1 + "," + x._2).repartition(1).saveAsTextFile("Strip_user_business_dict")


  }
}