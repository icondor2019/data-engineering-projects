from pyspark.sql import SparkSession

query = """

WITH last_year AS (
    SELECT * FROM actors WHERE current_year = 1974
),
current_year AS (
    SELECT
        actorid,
        actor,
        year,
        COLLECT_LIST(NAMED_STRUCT('film', film, 'votes', votes, 'rating', rating, 'filmid', filmid)) AS films,
        AVG(rating) AS year_rating
    FROM actor_films
    WHERE year = 1975
    GROUP BY actorid, actor, year
)
SELECT
    COALESCE(cy.actorid, ly.actorid) AS actorid,
    COALESCE(cy.actor, ly.actor) AS actor,
    CASE
        WHEN ly.films IS NULL THEN cy.films
        WHEN cy.films IS NULL THEN ly.films
        ELSE CONCAT(ly.films, cy.films)
    END AS films,
    CASE
        WHEN cy.year IS NOT NULL THEN (
            CASE
                WHEN cy.year_rating > 8 THEN 'star'
                WHEN cy.year_rating > 7 THEN 'good'
                WHEN cy.year_rating > 6 THEN 'average'
                ELSE 'bad'
            END
        )
        ELSE ly.quality_class
    END AS quality_class,
    cy.year IS NOT NULL AS is_active,
    1975 AS current_year
FROM last_year ly
FULL OUTER JOIN current_year cy
    ON cy.actorid = ly.actorid

"""


def do_actors_transformation(spark, dataframe1, dataframe2):
    dataframe1.createOrReplaceTempView("actors")
    dataframe2.createOrReplaceTempView("actor_films")
    return spark.sql(query)


def main():
    spark = SparkSession.builder \
        .master("local") \
        .appName("actors") \
        .getOrCreate()
    output_df = do_actors_transformation(spark, spark.table("actors"), spark.table("actor_films"))
    output_df.write.mode("overwrite").insertInto("actors")
