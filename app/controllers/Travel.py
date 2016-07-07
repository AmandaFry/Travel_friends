from system.core.controller import *
from system.core.model import Model
from flask import Flask, flash, session

class Travel(Controller):
    def __init__(self, action):
        super(Travel, self).__init__(action)
        self.load_model('Travel')
        # self.db = self._app.db

    def add_travel(self):
        return self.load_view('addplan.html')

    def add_plan(self):
        trip_info = {
            'destination' : request.form['destination'],
            'plan' : request.form['plan'],
            'start_date' : request.form['start_date'],
            'end_date' : request.form['end_date']
        }
        trips = self.models['Travel'].add_trip(trip_info)

        if  trips['status'] == False:
            #switch error message from array to Falsh and redirect to login page again
            for message in trips['errors']:
                flash(message)
            return self.load_view('addplan.html')
        else:
            return self.load_view('addplan.html')

