import csv
import json
import mysql.connector

with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

insert_stmt = (
    "INSERT INTO stories (story_name, surface_story, truth) "
    "VALUES (%s, %s, %s)"
)

with open('story_database/story_table.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        cursor.execute(insert_stmt, row)
        a = 1
db_connection.commit()
cursor.close()
db_connection.close()
