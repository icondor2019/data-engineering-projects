from chispa.dataframe_comparer import assert_df_equality
from ..jobs.local_actors_job import do_actors_transformation

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType, BooleanType

def test_actors_transformation(spark):
    film_struct = StructType([
        StructField("film", StringType(), True),
        StructField("votes", IntegerType(), True),
        StructField("rating", DoubleType(), True),
        StructField("filmid", IntegerType(), True)
    ])

    actors_schema = StructType([
        StructField("actorid", IntegerType(), True),
        StructField("actor", StringType(), True),
        StructField("films", ArrayType(film_struct), True),
        StructField("quality_class", StringType(), True),
        StructField("is_active", BooleanType(), True),
        StructField("current_year", IntegerType(), True),
    ])

    input_data1 = [
        {
            "actorid": 1,
            "actor": "Actor 1",
            "films": None,
            "quality_class": "star",
            "is_active": True,
            "current_year": 1974
        }
    ]

    input_data2 = [
        {
            "actorid": 1,
            "actor": "Actor 1",
            "year": 1975,
            "film": "Film B",
            "votes": 1000,
            "rating": 10.0,
            "filmid": 101
        }
    ]

    actor_films_schema = StructType([
        StructField("actorid", IntegerType(), True),
        StructField("actor", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("film", StringType(), True),
        StructField("votes", IntegerType(), True),
        StructField("rating", DoubleType(), True),
        StructField("filmid", IntegerType(), True),
    ])

    source_df1 = spark.createDataFrame(input_data1, schema=actors_schema)
    source_df2 = spark.createDataFrame(input_data2, schema=actor_films_schema)

    actual_df = do_actors_transformation(spark, source_df1, source_df2)

    expected_data = [
        {
            "actorid": 1,
            "actor": "Actor 1",
            "films": [
                {"film": "Film B", "votes": 1000, "rating": 10.0, "filmid": 101}
            ],
            "quality_class": "star",
            "is_active": True,
            "current_year": 1975
        }
    ]

    expected_df = spark.createDataFrame(expected_data, schema=actors_schema)

    assert_df_equality(actual_df, expected_df, ignore_nullable=True)


