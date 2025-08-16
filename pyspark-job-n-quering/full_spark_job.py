import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.storage.StorageLevel

val spark = SparkSession.builder()
  .appName("Iceberg Notebook")
  .config("spark.driver.memory", "8g") 
  .config("spark.executor.memory", "8g")       
  .config("spark.sql.shuffle.partitions", "4") 
  .config("spark.sql.autoBroadcastJoinThreshold", "-1") 
  .config("spark.sql.analyzer.failAmbiguousSelfJoin", "false")
  .getOrCreate()

// MEDALS
val medals = spark.read.option("header", "true")
                        .option("inferSchema", "true")
                        .csv("/home/iceberg/data/medals.csv")

// MAPS
val maps = spark.read.option("header", "true")
                        .option("inferSchema", "true")
                        .csv("/home/iceberg/data/maps.csv")

// MATCHES BUCKETED
val matchesBucketed = spark.read.option("header", "true")
                        .option("inferSchema", "true")
                        .csv("/home/iceberg/data/matches.csv")

//MATCH DETAILS BUCKETED
val matchDetailsBucketed =  spark.read.option("header", "true")
                        .option("inferSchema", "true")
                        .csv("/home/iceberg/data/match_details.csv")

// MEDALS MATCHES BUCKETED
val medalsMatchesPlayersBucketed = spark.read.option("header", "true")
                        .option("inferSchema", "true")
                        .csv("/home/iceberg/data/medals_matches_players.csv")

medals.createOrReplaceTempView("medals")
maps.createOrReplaceTempView("maps")
medals_matches_players.createOrReplaceTempView("medals_matches_players")


spark.sql("""DROP TABLE IF EXISTS bootcamp.matches_bucketed""")

val bucketedMatchDDL = """
CREATE TABLE IF NOT EXISTS bootcamp.matches_bucketed (
     match_id STRING,
     is_team_game BOOLEAN,
     playlist_id STRING,
     mapid STRING,
     completion_date TIMESTAMP
 )
 USING iceberg
 PARTITIONED BY (completion_date, bucket(16, match_id)); 
 """
spark.sql(bucketedMatchDDL)

matchesBucketed
  .select(
    $"match_id",
    $"is_team_game",
    $"playlist_id",
    $"mapid",
    $"completion_date"
  )
  .writeTo("bootcamp.matches_bucketed")
  .append()

spark.sql("DESCRIBE TABLE bootcamp.matches_bucketed").show(false)

val bucketedDetailsDDL = """
CREATE TABLE IF NOT EXISTS bootcamp.match_details_bucketed (
     match_id STRING,
     player_gamertag STRING,
     player_total_kills INTEGER,
     player_total_deaths INTEGER
 )
 USING iceberg
 PARTITIONED BY (bucket(16, match_id));
"""
spark.sql(bucketedDetailsDDL)

matchDetailsBucketed
  .select(
    $"match_id",
    $"player_gamertag",
    $"player_total_kills",
    $"player_total_deaths"
  )
  .writeTo("bootcamp.match_details_bucketed")
  .append()

spark.sql("""DROP TABLE IF EXISTS bootcamp.medal_players_bucketed""")

val bucketedMedalPlayersDDL = """
CREATE TABLE IF NOT EXISTS bootcamp.medal_players_bucketed (
     match_id STRING,
     player_gamertag STRING,
     medal_id BIGINT,
     count INTEGER
 )
 USING iceberg
 PARTITIONED BY (bucket(16, match_id));
"""
spark.sql(bucketedMedalPlayersDDL)

medalsMatchesPlayersBucketed
  .select(
    $"match_id",
    $"player_gamertag",
    $"medal_id",
    $"count"
  )
  .writeTo("bootcamp.medal_players_bucketed")
  .append()

val medalPlayers = spark.table("bootcamp.medal_players_bucketed")
val matchDetails = spark.table("bootcamp.match_details_bucketed")
val matches = spark.table("bootcamp.matches_bucketed")

val medalsFiltered = medals
  .select($"medal_id", $"name".as("medal_name"))

val mapsFiltered = maps
  .select($"mapid", $"name".as("map_name"))

val joinedDF = matches.as("m").where($"m.match_id".isNotNull)
  .join(matchDetails.as("md"), Seq("match_id"), "inner")
  .join(medalPlayers.as("mp"), Seq("match_id"), "inner")
  .join(broadcast(medalsFiltered).as("me"), $"mp.medal_id" === $"me.medal_id")
  .join(broadcast(mapsFiltered).as("ma"), $"m.mapid" === $"ma.mapid")
  .select(
    $"m.match_id",
    $"m.is_team_game",
    $"m.playlist_id",
    $"m.mapid",
    $"ma.map_name",
    to_date($"m.completion_date").as("ds"),
    $"md.player_gamertag",
    $"md.player_total_kills",
    $"md.player_total_deaths",
    $"mp.medal_id",
    $"mp.count".as("medal_count"),
    $"me.medal_name"
  )
  //.show(50)

// Joined DataFrame temporal View
joinedDF.createOrReplaceTempView("joinedDfView")

// Which player averages the most kills per game?
val AggKillsGame = spark.sql("""
WITH unique_matches AS (
    SELECT DISTINCT
        match_id,
        player_gamertag,
        playlist_id,
        mapid,
        player_total_kills
    FROM joinedDfView
)
SELECT 
    player_gamertag,
    playlist_id,
    mapid,
    COUNT(match_id) AS match_count,
    COUNT(DISTINCT match_id) AS unique_matches,
    SUM(player_total_kills) AS total_kills,
    SUM(player_total_kills) / COUNT(DISTINCT match_id) AS avg_kills_per_game
FROM unique_matches
GROUP BY player_gamertag, playlist_id, mapid
""")
AggKillsGame.show(5)

// Which playlist gets played the most?
val AggPlaylist = spark.sql("""
with unique_matches as (
    select
        distinct
        match_id,
        playlist_id,
        mapid
    from joinedDfView
)
  SELECT 
      playlist_id,
      count(match_id) as total_played_playlist
  FROM unique_matches 
  GROUP BY playlist_id
""")


// Which map gets played the most?
val AggMapPlayed = spark.sql("""
with unique_matches as (
    select
        distinct
        match_id,
        mapid,
        map_name
    from joinedDfView
)
  SELECT 
      mapid,
      map_name,
      count(match_id) as total_matches
  FROM unique_matches 
  GROUP BY mapid, map_name
""")
AggMapPlayed.show(5)

// Which map do players get the most Killing Spree medals on?
val AggMedals = spark.sql("""
SELECT
    mapid,
    medal_name,
    sum(medal_count) as total_medals
  FROM joinedDfView
  WHERE medal_name = 'Killing Spree'
  GROUP BY mapid, medal_name
""")
AggMedals.show(5)

val sortedA = AggKillsGame
  .repartition($"playlist_id")
  .sortWithinPartitions($"playlist_id", $"player_gamertag")

val sortedB = AggKillsGame
  .repartition($"mapid")
  .sortWithinPartitions($"mapid", $"player_gamertag")

val sortedC = AggKillsGame
  .repartition($"playlist_id", $"mapid")
  .sortWithinPartitions($"playlist_id", $"mapid", $"player_gamertag")

sortedA.write.mode("overwrite").saveAsTable("bootcamp.events_sortedA")
sortedB.write.mode("overwrite").saveAsTable("bootcamp.events_sortedB")
sortedC.write.mode("overwrite").saveAsTable("bootcamp.events_sortedC")

val fileSizes = spark.sql("""
SELECT SUM(file_size_in_bytes) AS size, COUNT(1) AS num_files, 'sortedA' AS table_name
FROM bootcamp.events_sortedA.files

UNION ALL

SELECT SUM(file_size_in_bytes) AS size, COUNT(1) AS num_files, 'sortedB' AS table_name
FROM bootcamp.events_sortedB.files

UNION ALL

SELECT SUM(file_size_in_bytes) AS size, COUNT(1) AS num_files, 'sortedC' AS table_name
FROM bootcamp.events_sortedC.files
""")


fileSizes.show(truncate = false)

// best scenario is sortedB, which shows the best performance, and has the lowest file size and number of files.