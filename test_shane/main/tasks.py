import json
from celery import shared_task
from pymongo import MongoClient
from psycopg2.extras import Json

import requests

import psycopg2

def get_database_mongo():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    client = MongoClient("mongodb+srv://u1:3Y55QyrlyUE8ceaY@c1.bkjgyg3.mongodb.net/?retryWrites=true&w=majority")

    # Create database for our example (we will use the same database throughout the tutorial
    return client["test_shane"]


collection_name = get_database_mongo()["users"]

def get_database_postgres():

    #establishing the connection
    conn = psycopg2.connect(
    database="postgres", user='postgres', password='root2', host='localhost', port= '5432'
    )
    conn.autocommit = True

    # Creating a cursor object using cursor() method
    cursor = conn.cursor()


    return cursor, conn


def readPostgres():
    # Call get_database_mongo function
    cursor, conn = get_database_postgres()

    # Create empty list
    user_list = []

    # Iterate over collection_name
    cursor.execute("SELECT * FROM main_user")
    for user in cursor.fetchall():
        user_data = {
            "id": user[0],
            "address": user[1],
            "username": user[2],
            "password": user[3],
            "firstname": user[4],
            "lastname": user[5],
            "phonennumber": user[6]
        }
        user_list.append(user_data)

    # print(user_list)

    # Convert list to string
    user_list = json.dumps(user_list)

    return user_list


def readMongo():
    # Call get_database_mongo function
    collection_name = get_database_mongo()["users"]

    # Create empty list
    user_list = []

    # Convert list to string
    user_list = json.dumps(user_list)

    user_list = []

    # Iterate over collection_name
    for user in collection_name.find():
        user_data = {
            "name": user["name"],
            "email": user["email"],
            "address": user["address"],
            "username": user["username"],
            "password": user["password"],
            "name": user["name"],
            "phone": user["phone"]
        }
        user_list.append(user_data)

    return user_list

@shared_task(name="call_api")
def call_api(count):
    userList = []

    try:
        response = requests.get('https://fakestoreapi.com/users', 'Accept: application/json')
        item = response.json()
        
        cursor, conn = get_database_postgres()

        # Create users database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'users'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute('CREATE DATABASE users')
            print("Database created successfully........")
        else:
            print("Database already exists........")

        # print all tables

        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    except:
        print("Error occurred while connecting to postgres db")


    if response.status_code == 200:
        for i in range(count):

            # Store in mongodb and postgres db

            # Convert the response to a json object

            try:

                for i in item:

                    # Ignore duplicates when inserting into table
                    userList.append(i)

                    # Write to postgres db
                    cursor.execute("INSERT INTO main_user (id, address, username, password, firstname, lastname, phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;", (i['id'], Json(i['address']), i['username'], i['password'], i['name']['firstname'], i['name']['lastname'], i['phone']))

                    conn.commit()

                conn.commit()
                cursor.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()



            # Store everything in collection_name
            collection_name.insert_many(userList)

            return item
        else:
            # handle error
            print("Error occurred while calling the API")
            # Return error
            return response.status_code




