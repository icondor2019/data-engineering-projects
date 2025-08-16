# Data Engineering Portfolio Projects

## Overview
This repository contains four data engineering projects demonstrating different aspects of data processing, modeling, and analysis.

## Projects

### 1. Dimensional Data Modeling
- **Purpose**: Implementation of Slowly Changing Dimensions (SCD) Type 2
- **Key Files**:
  - `1_create_bases.sql`
  - `2_scd_modeling.sql`
  - `3_incremental_query.sql`
- **Technologies**:
  - PostgreSQL
  - SQL
  - Data Warehousing

### 2. Fact Data Modeling
- **Purpose**: Movie ratings and performance metrics analysis
- **Key Files**:
  - `create_fact_bases.sql`
  - `populate_fact_tables.sql`
  - `incremental_fact_load.sql`
- **Technologies**:
  - PostgreSQL
  - ETL Processing
  - Data Warehousing

### 3. PySpark Job & Querying
- **Purpose**: Game analytics and player performance analysis
- **Key Features**:
  - Bucket join optimization
  - Performance metrics calculation
  - Player statistics analysis
- **Technologies**:
  - PySpark
  - Python
  - SQL

### 4. Spark Jobs & Testing
- **Purpose**: ETL processes with comprehensive testing
- **Key Components**:
  - Actor Analysis Pipeline
    - `actors_job.py`
    - `test_actors_job.py`
  - Game Analytics Pipeline
    - `game_analysis_job.py`
    - `test_game_analysis_job.py`
- **Technologies**:
  - PySpark
  - PyTest
  - Python

## Skills Demonstrated

### Data Modeling
- Dimensional modeling
- Fact table design
- SCD implementation
- Incremental loading

### Big Data Processing
- Spark optimization
- Data transformation
- ETL pipeline design
- Performance tuning

### Software Engineering
- Test-driven development
- Code organization
- Documentation
- Version control

### Database Technologies
- PostgreSQL
- SQL optimization
- Index management
- Query performance
