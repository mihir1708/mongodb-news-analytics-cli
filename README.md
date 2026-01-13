# MongoDB News Analytics CLI

A Python command-line application for loading large JSON datasets into MongoDB and running analytical queries using aggregation pipelines.

---

## 📌 Overview

This project demonstrates backend data engineering and analytics skills using **MongoDB** and **Python**. It provides tooling to efficiently ingest large JSONL datasets into a MongoDB collection and query them through a menu-driven CLI.

The focus is on **data ingestion, aggregation pipelines, and query design**, simulating real-world analytics workflows on semi-structured data.

---

## 🚀 Features

* Batch loading of large JSONL files into MongoDB
* Automatic collection reset for clean reloads
* Case-insensitive filtering and text processing
* Aggregation pipelines for analytical queries
* Interactive CLI menu for executing queries

### Supported Analytics

* Most common words by media type (news/blog)
* Daily article count comparison between media types
* Top news sources by article volume (2015)
* Most recent articles by source

---

## 🗂️ Project Structure

```
load-json.py        # Batch JSON loader for MongoDB
phase2_query.py    # CLI analytics and aggregation queries
testdb.json        # Sample JSONL dataset
```

---

## ▶️ How to Run

### Requirements

* Python 3
* MongoDB server running locally
* PyMongo (`pip install pymongo`)

### Start MongoDB

```bash
mongod --port <PORT> --dbpath <DB_PATH>
```

### Load Data

```bash
python3 load-json.py <json_file> <PORT>
```

### Run Analytics CLI

```bash
python3 phase2_query.py <PORT>
```

---

## 🛠️ Tech Stack

* Python 3
* MongoDB
* PyMongo
* MongoDB Aggregation Framework

---

## 🎯 What This Project Shows

* Designing efficient batch ingestion for large datasets
* Writing non-trivial MongoDB aggregation pipelines
* Handling semi-structured data at scale
* Building interactive developer tooling via CLI

---

## 📄 Notes

* Data is processed incrementally to avoid memory overhead
* Aggregations are optimized using `$match`, `$group`, and `$project`
* Designed to mirror real analytics and backend data workflows
