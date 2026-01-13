#!/usr/bin/env python3

import sys
import json
from pymongo import MongoClient

# Load JSON file into MongoDB database
def load_json_to_mongodb(json_filename, port):
    client = MongoClient('localhost', int(port))
    db = client['291db']
    
    if 'articles' in db.list_collection_names():
        db['articles'].drop()
        print("Dropped existing 'articles' collection")
    
    collection = db['articles']
    
    # Process in batches to avoid memory issues with large files
    BATCH_SIZE = 5000
    batch = []
    total_inserted = 0
    
    print(f"Loading data from {json_filename}...")
    
    # Read line by line instead of loading entire file into memory
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    doc = json.loads(line)
                    batch.append(doc)
                    
                    # Insert batch when it reaches the size limit
                    if len(batch) >= BATCH_SIZE:
                        collection.insert_many(batch)
                        total_inserted += len(batch)
                        print(f"Inserted {total_inserted} documents...")
                        batch = []
                        
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON on line {line_num}: {e}")
                    continue
        
        # Insert any remaining documents in the batch
        if batch:
            collection.insert_many(batch)
            total_inserted += len(batch)
            print(f"Inserted {total_inserted} documents...")
        
        print(f"\nCompleted! Total documents inserted: {total_inserted}")
        
    except FileNotFoundError:
        print(f"Error: File '{json_filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python load-json.py <json_filename> <port>")
        sys.exit(1)
    
    json_filename = sys.argv[1]
    port = sys.argv[2]
    
    load_json_to_mongodb(json_filename, port)

