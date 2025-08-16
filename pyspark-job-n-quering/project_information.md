# PySpark Game Analytics Project
Welcome to my PySpark Game Analytics project! This project demonstrates how to analyze gaming data using Apache Spark, focusing on player performance, map popularity, and medal achievements.

## 📋 Project Overview
This project analyzes gaming match data to uncover interesting patterns and statistics. We'll look at things like which players are performing best, which maps are most popular, and where players earn special achievements.

## 🎮 Data Structure
We're working with four main datasets:
- Match Details: Individual player performance in each match
- Matches: Information about each game played
- Medal Matches Players: Records of medals earned by players
- Medals: Types of achievements players can earn

## 🛠️ Technical Implementation
The project consists of several PySpark jobs that:

### Setup and Configuration
- Disables automatic broadcast joins
- Implements manual broadcast optimization for smaller tables
- Uses bucket joining for larger tables

### Data Analysis
- Calculates player kill averages
- Determines most popular playlists
- Identifies frequently played maps
- Analyzes medal achievements by location

### Performance Optimization
- Implements partition sorting
- Tests different data organization strategies


## 📊 Key Features
- Advanced join optimizations
- Bucket-based data organization
- Aggregation pipelines
- Performance tuning

## 📈 Sample Queries
Here are some questions we answer:

- Who's the top performer in terms of kills per game?
- Which game mode (playlist) do players choose most often?
- What's the most popular map?
- Where do players earn the most Killing Spree medals?

## 🔧 Technologies Used
- Python
- Apache Spark (PySpark)
- SQL
- Data Analysis Libraries

## 📚 Skills Demonstrated
- Big Data Processing
- Data Analysis
- Performance Optimization
- SQL and DataFrame Operations
- Data Visualization