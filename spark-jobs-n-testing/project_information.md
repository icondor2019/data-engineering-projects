# Spark Jobs & Testing

A PySpark project demonstrating ETL processing and data transformation for actor performance analysis across different years. This project showcases best practices in Spark job development, data quality management, and performance optimization.

## Project Overview
This project processes and analyzes actor performance data across multiple years, calculating quality classifications based on movie ratings. It implements a sophisticated ETL process that:

- Tracks actor participation in films year over year
- Calculates performance metrics
- Assigns quality classifications
- Maintains historical data

## Project Structure

### Main Components
- **Actor Analysis Pipeline**
  - `actors_job.py` - Main transformation logic
  - `test_actors_job.py` - Test suite
- **Game Analytics Pipeline**
  - `game_analysis_job.py` - Game data processing
  - `test_game_analysis_job.py` - Test suite

## Technical Implementation

### Actor Analysis Features
- Year-over-year performance tracking
- Quality classification system:
  - Star: Rating > 8.0
  - Good: Rating > 7.0
  - Average: Rating > 6.0
  - Bad: Rating <= 6.0

### Game Analytics Features
- Optimized bucket joins
- Multi-source data integration
- Complex player statistics

## Testing Framework

### Test Components
- Unit tests for transformations
- Integration tests for Spark ops
- Mock data frameworks
- Performance validation

## Key Features

### Data Processing
- ETL transformation pipelines
- Spark configuration optimization
- Data quality checks
- Historical tracking
- Performance monitoring

## Technologies

### Core Stack
- Apache Spark
- PySpark
- Python
- PyTest
- SQL

## Skills Demonstrated

### Technical Competencies
- Spark Job Development
- Test-Driven Development
- SQL Optimization
- ETL Design
- Performance Tuning
- Data Quality Management
- Complex Joins
- Window Functions