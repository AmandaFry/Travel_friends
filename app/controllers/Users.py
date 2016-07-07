from system.core.controller import *
from flask import Flask, flash

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        # Note that we have to load the model before using it in the methods below
        self.load_model('Loginreg')

    # method to display registration page
    def index(self):
        return self.load_view('index.html')

    def process_login(self):
        #Process a login request
        user_info = {
            'email' : request.form['email'],
            'password' : request.form['passw']
        }
        users = self.models['Loginreg'].login_user(user_info)
        print users['status']

        #if user was not found it will bring back status False
        if  users['status'] == False:
            #switch error message from array to Falsh and redirect to login page again
            for message in users['errors']:
                flash(message)
            return redirect('/')
        else:
            # print users
            # #accessing the dicitionary value 
            # print users['users']['id']
            #adding the user name and id into session that will be used for applications
            session['id']= users['users']['id']
            session['name'] = users['users']['first_name'] + ' ' + users['users']['last_name']
            #checking to make sure I got the correct info in session
            # print 'I am seesion id ', session['id']
            # print 'I am session name', session['name']
            # return self.load_view('dashboard.html', users=users['users'])
            return redirect('/dashboard')

    def dashboard(self):
            return self.load_view('dashboard.html')


    def logout(self):
        # when login out cleared out the id and name of the user who logged in
        session.clear()
        return redirect('/')

    def process_registration(self):
        #register a new user - gather data from index form and pass it to the model
        user_info = {
            'f_name':request.form['f_name'],
            'l_name':request.form['l_name'],
            'email':request.form['email'],
            'passw':request.form['passw'],
            'conf_passw':request.form['conf_passw'],
        }
        #I call the model the register)usr method
        register = self.models['Loginreg'].register_user(user_info)

        if  register['status'] == False:
            #switch error message from array to flash and redirect to registered
            for message in register['errors']:
                flash(message)
            return redirect('/')
        else:
            #In this version I return a flash message letting the user know the registration was successful
            flash('Succesfully registered please login')
            return redirect('/')

