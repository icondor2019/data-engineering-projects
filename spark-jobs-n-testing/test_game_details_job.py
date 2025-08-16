from chispa.dataframe_comparer import *

from ..jobs.local_game_details_job import do_game_details_transformation
from collections import namedtuple

Game = namedtuple("GameDetail", "game_id game_date_est season home_team_id visitor_team_id")
GameDetails = namedtuple("Games", "game_id team_id player_id")
GameDetailDeduped = namedtuple("GameDetailDeduped", "game_id team_id player_id game_date_est season home_team_id visitor_team_id")


def test_game_details_job(spark):
    input_data1 = [
                Game(
                    game_id=1001,
                    game_date_est="2023-03-01",
                    season="2022",
                    home_team_id=1,
                    visitor_team_id=2)
    ]

    input_data2 = [
        GameDetails(
                    game_id=1001,
                    team_id=1,
                    player_id=101),
        GameDetails(
                    game_id=1001,
                    team_id=1,
                    player_id=101),
    ]

    source_df1 = spark.createDataFrame(input_data1)
    source_df2 = spark.createDataFrame(input_data2)

    actual_df = do_game_details_transformation(spark, source_df1, source_df2)

    expected_values = [
        GameDetailDeduped(
            game_id=1001,
            team_id=1,
            player_id=101,
            game_date_est="2023-03-01",
            season="2022",
            home_team_id=1,
            visitor_team_id=2
            )
    ]
    
    expected_df = spark.createDataFrame(expected_values)
    assert_df_equality(actual_df, expected_df)
