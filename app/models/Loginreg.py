from system.core.model import Model
from flask import Flask, flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NOSPACE_REGEX = re.compile(r'^[a-zA-Z0-9]*$')
PW_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?\d)[A-Za-z\d]{8,}$')


class Loginreg(Model):
    def __init__(self):
        super(Loginreg, self).__init__()

    def login_user(self, user_info):
        # This section processing user login info
        errors=[] #reset errors to blank

        #check to see if both field has at least two entry
        if len(user_info['email'])<2 or len(user_info['password'])<2:
            errors.append("email or password was too short")
        #check to see if email has an email format
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append("Please enter a valid email format")
        # check to see if any of the entry is only spaces
        elif not NOSPACE_REGEX.match(user_info['password']):
            errors.append("Email or password did not match")
        if errors:
            #if found error than send back a dictionary for status False and the error message
            return {"status": False, "errors": errors}
        else:
            #the initial check to send infor to database passed now prefomaning access to the db.
            #pulls the information it needs for user_info to perform the db qurey 
            data = {'email': user_info['email']}
            #the query to db
            query = "SELECT * FROM users WHERE email = :email"
            #execting the the db, once excuted users is populated but not returned to contoroller yet
            # I still need to do a return to send the info back to the controller
            users = self.db.query_db(query, data)

            #if the users are 0 length than it did not find the entr in the db. Tis check should
            #be done before checking password
            if len(users) == 0:
                errors.append("User was not found please register")
            #check to see if the password is matches what was typed in
            elif not self.bcrypt.check_password_hash(users[0]['password'],user_info['password']):
                errors.append('Incorrect password - login was not successful')
                return {"status": False, "errors": errors}
            else:
                #the user exist and the password matched return the status True and users information
                return {"status": True, "users": users[0] }

    def register_user(self, user_info):
        errors=[] #reset errors to blank
        print "I got to register model"
        print user_info

        #validating entries before db insert
        #check to see if the fist name is empty
        if len(user_info['f_name']) < 2 :
            errors.append("First name cannot be empty")
        #check to see if first name only spaces
        elif not NOSPACE_REGEX.match(user_info['f_name']):
            errors.append("Please enter a valid first name")
        elif len(user_info['l_name']) < 2 :
        #check to see if last name is empty
            errors.append("Last name cannot be empty")
        #check to see if last name only has spcaes
        elif not NOSPACE_REGEX.match(user_info['f_name']):
            errors.append("Please enter a valid last name")
        #check to see if email is empty
        elif len(user_info) < 2 :
            errors.append("Email cannot be empty")
        #check to see if email has an email format
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append("Please enter a valid email format")
        #check to see if password empty
        elif len(user_info['passw']) < 2 :
            errors.append("Password cannot be empty")   
        #check to see if password a right format
        elif not PW_REGEX.match(user_info['passw']):
            errors.append("Please enter a valid password. It must be 8 charater long, at must include least one upper case and number")
        #check to see if confirm password is empty
        elif len(user_info['conf_passw']) < 2 :
            errors.append("Confirm password cannot be empty")
        #check to see if password match
        elif not (user_info['passw'] == user_info['conf_passw']):
            errors.append("Password and confirm password must match")

        if errors:
            #if found error than send back a dictionary for status False and the error message
            return {"status": False, "errors": errors}
        else:
        #check if email already in use
            data = {'email': user_info['email']}
            #the query to db
            query = "SELECT * FROM users WHERE email = :email"
            #execting the the db, once excuted users is populated but not returned to contoroller yet
            # I still need to do a return to send the info back to the controller
            users = self.db.query_db(query, data)
            print users
            if users:
                errors.append("Email account already in use")
                return {"status": False, "errors": errors}
            else:
            # at this point the informaiton is all valid and the email accoutn is not in use.
                password = user_info['passw']
                hashed_pw = self.bcrypt.generate_password_hash(password)
                #inserting data
                data = {
                    'f_name':user_info['f_name'],
                    'l_name':user_info['l_name'],
                    'email':user_info['email'],
                    'passw':hashed_pw,
                }
                query = "INSERT into users (first_name, last_name, email, password, created_at, updated_at) values(:f_name, :l_name, :email, :passw, NOW(), NOW())"
                registered_user = self.db.query_db(query, data)
                return {"status": True }
