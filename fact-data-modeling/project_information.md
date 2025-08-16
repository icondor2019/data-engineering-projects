# Fact Table Data Modeling Example

This project demonstrates the implementation of a fact table in a data warehouse environment, focusing on movie ratings and performance metrics. The implementation showcases best practices in fact table design, including handling of multiple grain levels and incremental loading patterns.

## Project Overview

The project implements a fact table design for movie analytics, demonstrating:
- Fact table creation and modeling
- Aggregation strategies
- Incremental loading patterns
- Performance optimization techniques

## Project Structure

The project consists of three main SQL files:

1. **create_fact_bases.sql**
   - Creates dimension tables (dim_movies, dim_dates, dim_users)
   - Establishes fact table structure
   - Implements foreign key relationships
   - Sets up required indexes

2. **populate_fact_tables.sql**
   - Loads dimension tables with initial data
   - Populates fact table with historical data
   - Implements data quality checks
   - Creates aggregated fact tables

3. **incremental_fact_load.sql**
   - Handles incremental fact table updates
   - Manages late-arriving facts
   - Updates aggregated tables
   - Implements change tracking

### Key Features

- **Multiple Grain Levels**: Supports both detailed and aggregated fact analysis
- **Performance Optimization**: Implemented partitioning and indexing strategies
- **Data Quality**: Built-in validation and error handling
- **Incremental Processing**: Efficient handling of new data loads

## Use Cases

This fact table model supports:
- Movie performance analytics
- User rating analysis
- Temporal trend analysis
- Performance metrics calculation

## Skills Demonstrated

- Fact Table Modeling
- SQL Performance Optimization
- Indexing Strategies
- Incremental Loading Patterns
- Data Quality Management
- Aggregation Techniques

## Technologies Used

- PostgreSQL
- SQL
- Data Warehousing Concepts
- ETL Processing