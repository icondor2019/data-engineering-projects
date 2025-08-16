from pyspark.sql import SparkSession

query = """

WITH deduped AS (
  SELECT
    g.game_date_est,
    g.season,
    g.home_team_id,
    g.visitor_team_id,
    gd.game_id,
    gd.team_id,
    gd.player_id,
    ROW_NUMBER() OVER (
      PARTITION BY gd.game_id, gd.team_id, gd.player_id
      ORDER BY g.game_date_est ASC
    ) AS row_num
  FROM game_details gd
  JOIN games g
    ON gd.game_id = g.game_id
)
SELECT
  game_id,
  team_id,
  player_id,
  game_date_est,
  season,
  home_team_id,
  visitor_team_id
FROM deduped
WHERE row_num = 1

"""


def do_game_details_transformation(spark, dataframe1, dataframe2):
    dataframe1.createOrReplaceTempView("games")
    dataframe2.createOrReplaceTempView("game_details")
    return spark.sql(query)


def main():
    spark = SparkSession.builder \
        .master("local") \
        .appName("game_details") \
        .getOrCreate()
    output_df = do_game_details_transformation(spark, spark.table("games"), spark.table("game_details"))
    output_df.write.mode("overwrite").insertInto("game_details")
