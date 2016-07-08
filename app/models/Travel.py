from system.core.model import Model
from flask import Flask, flash, session
from datetime import datetime
import re

NOSPACE_REGEX = re.compile(r'^[a-zA-Z0-9]*$')

class Travel(Model):
    def __init__(self):
        super(Travel, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """
    

    def add_trip(self, trip_info):
        travel_erorrs = []
        print "I made it to travel model"
        trip_info = {
            'destination' : trip_info['destination'],
            'plan' : trip_info['plan'],
            'start_date' : trip_info['start_date'],
            'end_date' : trip_info['end_date']
        }
        print ('*' * 25)
        print trip_info
        print ('*' * 25)

        today = datetime.now().strftime("%Y-%m-%d")
        print ('^' * 25)
        print today
        print "User logged in: ", session['id']
        print ('^' * 25)
        
        if len(trip_info['destination']) < 2:
            travel_erorrs.append("Please enter a valid destination")
        elif len(trip_info['plan']) < 2:
            travel_erorrs.append("Please enter a valid plan")
        # elif not NOSPACE_REGEX.match(trip_info['plan']):
        #     travel_erorrs.append("Plan cannot be just spaces")
        elif today > trip_info['start_date']:
            travel_erorrs.append("Start date must be in the future")
        elif today > trip_info['end_date']:
            travel_erorrs.append("End date must be in the future")
        elif trip_info['start_date'] >= trip_info['end_date']:
            travel_erorrs.append("Start date must be before end date")
        if travel_erorrs:
            return {"status": False, "errors": travel_erorrs}
        else:
            sql = "INSERT into trips (organizer_id, destination, plan, start_date, end_date, created_at, updated_at) values(:organizer_id, :destination, :plan, :start_date, :end_date, NOW(), NOW())"
            data = {
                'organizer_id': session['id'], 
                'destination': trip_info['destination'],
                'plan' : trip_info['plan'],
                'start_date' : trip_info['start_date'],
                'end_date' : trip_info['end_date'] 
            }
            self.db.query_db(sql, data) #run the insert
            return {"status": True}

    def my_trip(self):
        query = "SELECT * from trips where organizer_id = :id"
        data = {'id': session['id']}
        # result_mytrip = self.db.get_one(query, data)
        # return {"status": True, 'mytrips': mytrips}
        return self.db.query_db(query, data)

    def others_trip(self):
        # query = "SELECT * from trips where organizer_id != :id"
        query = "SELECT users.first_name, users.last_name, trips.destination, trips.start_date, trips.end_date, trips.id FROM users JOIN trips ON users.id = trips.organizer_id WHERE organizer_id != :id"
        data = {'id': session['id']}
        # result_mytrip = self.db.get_one(query, data)
        # return {"status": True, 'mytrips': mytrips}
        return self.db.query_db(query, data)
