# Dimensional Data Modeling Example

This project demonstrates the implementation of Slowly Changing Dimensions (SCD) Type 2 in a data warehouse environment, specifically focusing on tracking historical changes in actor data over time.

## Project Structure

The project consists of three main SQL files that build up the dimensional model:

1. [1_create_bases.sql](1_create_bases.sql) - Creates the base tables and custom types:
   - Custom types (`film_struct` and `quality_class`)
   - `actors` table for yearly data
   - `actors_history_scd` table for historical tracking

2. [2_scd_modeling.sql](2_scd_modeling.sql) - Implements SCD Type 2 logic:
   - Populates the `actors` table with yearly data
   - Implements backfill logic for historical data tracking
   - Handles quality classification of actors based on ratings

3. [3_incremental_query.sql](3_incremental_query.sql) - Manages incremental updates:
   - Creates custom type for SCD records
   - Implements logic to handle:
     - Unchanged records
     - Changed records
     - New records
     - Historical records

## Technical Implementation

### Data Types
- `film_struct`: Custom composite type storing film details (name, votes, rating, ID)
- `quality_class`: Enum type for actor classification ('bad', 'average', 'good', 'star')
- `actor_scd_type`: Custom type for SCD record management

### Key Features

- **Historical Tracking**: Maintains complete history of changes in actor quality and activity status
- **Efficient Updates**: Uses incremental loading pattern to handle new data
- **Data Quality**: Implements classification system based on performance metrics
- **Change Detection**: Sophisticated change tracking using window functions and state management

## Use Case

This dimensional model is designed to:
- Track actor performance over time
- Maintain historical quality classifications
- Handle active/inactive status changes
- Support analytical queries across time periods

## Skills Demonstrated

- Dimensional Modeling
- SQL Custom Types
- Window Functions
- CTEs (Common Table Expressions)
- Data Warehousing Concepts
- SCD Type 2 Implementation
- Incremental Loading Patterns

## Technologies Used

- PostgreSQL
- SQL
- Data Warehousing Concepts