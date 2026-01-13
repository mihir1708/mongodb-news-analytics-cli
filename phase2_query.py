#!/usr/bin/env python3

import sys
from datetime import datetime
from pymongo import MongoClient

# Connect to MongoDB database
def connect_to_db(port):
    client = MongoClient('localhost', int(port))
    db = client['291db']
    return db

# Find top 5 most common words for a given media type
def most_common_words_by_media_type(db, media_type):
    pipeline = [
        {
            '$match': {
                'media-type': {'$regex': f'^{media_type}$', '$options': 'i'}
            }
        },
        {
            '$project': {
                'combined_text': {
                    '$concat': [
                        {'$ifNull': ['$content', '']},
                        ' ',
                        {'$ifNull': ['$title', '']}
                    ]
                }
            }
        },
        {
            '$project': {
                'words': {
                    '$split': [
                        {'$toLower': '$combined_text'},
                        ' '
                    ]
                }
            }
        },
        {
            '$unwind': '$words'
        },
        {
            '$match': {
                'words': {
                    '$regex': '^[a-zA-Z]+$',
                    '$ne': ''
                }
            }
        },
        {
            '$group': {
                '_id': '$words',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 5
        }
    ]
    
    results = list(db['articles'].aggregate(pipeline))
    
    print(f"\nTop 5 most common words for '{media_type}':")
    if results:
        for result in results:
            word = result['_id']
            count = result['count']
            print(f"  {word}: {count}")
    else:
        print("  No words found")
    
    return results

# Count articles by media type for a specific date
def article_count_difference(db, date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        
        # Convert date to ISO format for full day range
        start_date = date_str + 'T00:00:00Z'
        end_date = date_str + 'T23:59:59Z'
        
        pipeline = [
            {
                '$match': {
                    'published': {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }
            },
            {
                '$match': {
                    'media-type': {
                        '$regex': r'^(news|blog)$',
                        '$options': 'i'
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        '$toLower': '$media-type'
                    },
                    'count': {'$sum': 1}
                }
            }
        ]
        
        results = list(db['articles'].aggregate(pipeline))
        
        news_count = 0
        blog_count = 0
        for result in results:
            media_type = result['_id']
            count = result['count']
            if media_type == 'news':
                news_count = count
            elif media_type == 'blog':
                blog_count = count
        
        if news_count == 0 and blog_count == 0:
            print("\nNo articles were published on this day.")
        else:
            print(f"\nDate: {date_str}")
            print(f"News articles: {news_count}")
            print(f"Blog articles: {blog_count}")
            
            if news_count > blog_count:
                diff = news_count - blog_count
                print(f"News had more articles by {diff}")
            elif blog_count > news_count:
                diff = blog_count - news_count
                print(f"Blog had more articles by {diff}")
            else:
                print("Both media types had the same number of articles")
        
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD")
    except Exception as e:
        print(f"Error: {e}")

# Find top 5 news sources by article count in 2015
def top_5_sources_2015(db):
    start_date = '2015-01-01T00:00:00Z'
    end_date = '2015-12-31T23:59:59Z'
    
    pipeline = [
        {
            '$match': {
                'published': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
        {
            '$group': {
                '_id': '$source',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 5
        }
    ]
    
    results = list(db['articles'].aggregate(pipeline))
    
    print("\nTop 5 news sources by article count (2015):")
    if results:
        for i, result in enumerate(results, 1):
            source = result['_id'] if result['_id'] else 'Unknown'
            count = result['count']
            print(f"  {i}. {source}: {count} articles")
    else:
        print("  No articles found for 2015")

# Find 5 most recent articles from a given source
def most_recent_articles_by_source(db, source_name):
    source_name_lower = source_name.lower()
    pipeline = [
        {
            '$match': {
                '$expr': {
                    '$eq': [
                        {'$toLower': '$source'},
                        source_name_lower
                    ]
                }
            }
        },
        {
            '$sort': {'published': -1}
        },
        {
            '$limit': 5
        },
        {
            '$project': {
                'title': {'$ifNull': ['$title', 'No title']},
                'published': {'$ifNull': ['$published', '']}
            }
        }
    ]
    
    results = list(db['articles'].aggregate(pipeline))
    
    if not results:
        print(f"\nSource '{source_name}' was not found.")
    else:
        print(f"\nTop {len(results)} most recent articles from '{source_name}':")
        for i, article in enumerate(results, 1):
            title = article.get('title', 'No title')
            published = article.get('published', '')
            
            # Get date from ISO format
            if published:
                try:
                    date_part = published.split('T')[0]
                except:
                    date_part = published
            else:
                date_part = 'Unknown date'
            
            print(f"  {i}. {title} ({date_part})")

# Display main menu and handle user input
def main_menu(db):
    while True:
        print("\n" + "="*50)
        print("Main Menu")
        print("="*50)
        print("1. Most Common Words by Media Type")
        print("2. Article Count Difference Between News and Blogs")
        print("3. Top 5 News Sources by Article Count (2015)")
        print("4. 5 Most Recent Articles by Source")
        print("5. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            media_type = input("Enter media type (news or blog): ").strip()
            if media_type:
                most_common_words_by_media_type(db, media_type)
            else:
                print("Error: Media type cannot be empty")
        
        elif choice == '2':
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            if date_str:
                article_count_difference(db, date_str)
            else:
                print("Error: Date cannot be empty")
        
        elif choice == '3':
            top_5_sources_2015(db)
        
        elif choice == '4':
            source_name = input("Enter source name: ").strip()
            if source_name:
                most_recent_articles_by_source(db, source_name)
            else:
                print("Error: Source name cannot be empty")
        
        elif choice == '5':
            print("\nExiting program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python phase2_query.py <port>")
        sys.exit(1)
    
    port = sys.argv[1]
    
    try:
        db = connect_to_db(port)
        print(f"Connected to MongoDB database '291db' on port {port}")
        main_menu(db)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

