######################################### IMPORTS ##########################################################################################################################################################
from flask import Flask, render_template, request, make_response, Response, jsonify 
from flask_assistant import Assistant, ask, tell
from flask_mysqldb import MySQL
import mysql.connector 
import MySQLdb   
import sched, time
import datetime 
import pygal  
import yaml 
import json 
import pymysql 
import io
import csv 
import zipfile 

from pygal.style import Style 
from datetime import date

import textinput 
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

############################################################## GLOBAL VARIABLES ######################################
#G Constants
SUCCESS         = "POST SUCCESS"
FAIL            = "POST FAILED"
SOMETHING_WRONG = "<h3 style='color: maroon;'>SOMETHING WENT WRONG. PLEASE CHECK YOUR ENTRY AND TRY AGAIN</h3>"

#flask handle
server = Flask(__name__)
#assistant
assist = Assistant(server, project_id='replace_the_project_id') 

#db param handle
dbParam = yaml.safe_load(open('loginParams.yaml')) 


#db config variables
server.config['MYSQL_HOST']     = dbParam['mysql_host']
server.config['MYSQL_USER']     = dbParam['mysql_user']
server.config['MYSQL_PASSWORD'] = dbParam['mysql_password']
server.config['MYSQL_DB']       = dbParam['mysql_db'] 

#db handle
dbConn = MySQL(server)

#global dictionary
allsensors = {} 

def warning_checker():
    global allsensors

    ########################## GOOGLE ASSISTANT ACTIONS #############################
    action1 = 'Switch everything off'
    action5 = 'Switch everything on'
    action4 = 'Turn on bulb one'    
    action8 = 'Set bulb one to RED'



    #################### ACTION TRIGGER LOGIC ########################

    if (("temperature_l1" in allsensors) and ("max_temperature" in allsensors)):
        if allsensors["temperature_l1"] > float(allsensors["max_temperature"]): 
            temp_brdcst = 'Broadcast Warning: temperature is %0.2f degrees' % allsensors["temperature_l1"]  
            textinput.start_ga(temp_brdcst) 
            if "action_temperature" in allsensors:
                if allsensors["action_temperature"]   == "option1":
                    textinput.start_ga(action4)
                    textinput.start_ga(action8) 
                elif allsensors["action_temperature"] == "option2":
                    textinput.start_ga(action1) 
                elif allsensors["action_temperature"] == "option3": 
                    textinput.start_ga(action5) 
    
    if (("pressure_l1" in allsensors) and ("max_pressure" in allsensors)):
        if allsensors["pressure_l1"] > float(allsensors["max_pressure"]):
            pres_brdcst = 'Broadcast Warning: pressure is %0.2f Pascal' % allsensors["pressure_l1"]  
            textinput.start_ga(pres_brdcst) 
            if "action_pressure" in allsensors:
                if allsensors["action_pressure"]   == "option1":
                    textinput.start_ga(action4)
                    textinput.start_ga(action8) 
                elif allsensors["action_pressure"] == "option2":
                    textinput.start_ga(action1) 
                elif allsensors["action_pressure"] == "option3": 
                    textinput.start_ga(action5) 

    if (("humidity_l1" in allsensors) and ("max_humidity" in allsensors)):
        if allsensors["humidity_l1"] > float(allsensors["max_humidity"]): 
            hum_brdcst = 'Broadcast Warning: humidity is %0.2f %%' % allsensors["humidity_l1"]  
            textinput.start_ga(hum_brdcst) 
            if "action_humidity" in allsensors:
                if allsensors["action_humidity"]   == "option1":
                    textinput.start_ga(action4)
                    textinput.start_ga(action8) 
                elif allsensors["action_humidity"] == "option2":
                    textinput.start_ga(action1) 
                elif allsensors["action_humidity"] == "option3": 
                    textinput.start_ga(action5)
    
    if (("lux_l1" in allsensors) and ("min_lux" in allsensors)):
        if allsensors["lux_l1"] < float(allsensors["min_lux"]):
            lux_brdcst = 'Broadcast Warning: illuminance is %0.2f lux' % allsensors["lux_l1"]  
            textinput.start_ga(lux_brdcst) 
            if "action_lux" in allsensors:
                if allsensors["action_lux"]   == "option1":
                    textinput.start_ga(action4)
                    textinput.start_ga(action8) 
                elif allsensors["action_lux"] == "option2":
                    textinput.start_ga(action1) 
                elif allsensors["action_lux"] == "option3": 
                    textinput.start_ga(action5)

    if (("luminosity_l1" in allsensors) and ("min_luminosity" in allsensors)):
        if allsensors["luminosity_l1"] < float(allsensors["min_luminosity"]):
            lum_brdcst = 'Broadcast Warning: luminosity is %0.2f lumens' % allsensors["luminosity_l1"]  
            textinput.start_ga(lum_brdcst) 
            if "action_luminosity" in allsensors:
                if allsensors["action_luminosity"]   == "option1":
                    textinput.start_ga(action4)
                    textinput.start_ga(action8) 
                elif allsensors["action_luminosity"] == "option2":
                    textinput.start_ga(action1) 
                elif allsensors["action_luminosity"] == "option3": 
                    textinput.start_ga(action5)

    if (("co_l2" in allsensors) and ("max_co" in allsensors)): 
        if allsensors["co_l2"] > float(allsensors["max_co"]):
            co_brdcst = 'Broadcast Warning: carbon mono oxide level is %0.2f ppm, exit the building' % allsensors["co_l2"]  
            textinput.start_ga(co_brdcst) 
            if "action_co" in allsensors:
                if allsensors["action_co"]   == "option1":
                    textinput.start_ga(action4)
                    textinput.start_ga(action8) 
                elif allsensors["action_co"] == "option2":
                    textinput.start_ga(action1) 
                elif allsensors["action_co"] == "option3": 
                    textinput.start_ga(action5)

################### ACTION LOGIC END #################################


scheduler = BackgroundScheduler()
scheduler.add_job(func=warning_checker, trigger="interval", seconds=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


################################################################# GOOGLE ASSISTANT ROUTES ###############################

@server.route('/test_ga_on', methods=['POST', 'GET']) 
def test_ga_on(): 
    value1 = 'Turn on switch one'
    textinput.start_ga(value1)
    return 'success'

@server.route('/test_ga_off', methods=['POST', 'GET']) 
def test_ga_off(): 
    temp_value = 37.4
    #value1 = 'Broadcast %d degrees' % temp_value 
    value1 = 'Turn off switch one'
    textinput.start_ga(value1)
    return 'success'

################################################################# FLASK ASSISTANT ROUTES ###################################

@assist.action('Default Welcome Intent')
def welcome():
    return ask("What sensor reading do you want?")

@assist.action('sensor-readings', mapping={'sensorVal': 'sensor'})
def sensor_manager(sensorVal):
    global allsensors
    if sensorVal == "temperature":
        if "temperature_l1" in allsensors:
            speech = "The temperature is %0.2f Celsius" % allsensors["temperature_l1"]
        else:
            speech = "Temperature sensor not available"
    elif sensorVal == "pressure":
        if "pressure_l1" in allsensors:
            speech = "The pressure is %0.2f Pa" % allsensors["pressure_l1"] 
        else:
            speech = "Pressure sensor not available"
    elif sensorVal == "humidity":
        if "humidity_l1" in allsensors:
            speech = "The humidity is %0.2f%%" % allsensors["humidity_l1"]
        else:
            speech = "Pressure sensor not available"
    elif sensorVal == "illuminance":
        if "lux_l1" in allsensors:
            speech = "The illuminance is %0.2f" % allsensors["lux_l1"] 
        else:
            speech = "Illuminance sensor not available"
    elif sensorVal == "luminosity":
        if "luminosity_l1" in allsensors:
            speech = "The luminosity is %0.2f" % allsensors["luminosity_l1"] 
        else:
            speech = "Luminosity sensor not available"
    elif sensorVal == "carbon mono oxide":
        if (("co_l2" in allsensors) and ("temperature_l2" in allsensors) and ("pressure_l2" in allsensors) and ("humidity_l2" in allsensors)):
            speech = "The carbon mono oxide reading is %0.2f ppm at %0.2f Celsius, %0.2f Pa and %0.2f%% humidity" % (allsensors["co_l2"], allsensors["temperature_l2"], allsensors["pressure_l2"], allsensors["humidity_l2"])
        else:
            speech = "Carbon mono oxide sensor not available"
    elif sensorVal == "phone device state":
        if "device_state" in allsensors:
            speech = "The phone state is %s" % allsensors["device_state"] 
        else:
            speech = "Phone device state not available"
    elif sensorVal == "phone call state":
        if "call_state" in allsensors:
            speech = "The call state is %s" % allsensors["call_state"] 
        else:
            speech = "Phone call state not available"
    elif sensorVal == "heart rate":
        if "heart_rate" in allsensors:
            speech = "The heart rate value is %s beats per minute" % allsensors["heart_rate"] 
        else:
            speech = "Heart rate value is not available" 
    else:
        speech = "Please specify a sensor"

    return tell(speech)

######################################################## HOME PAGE #################################################

@server.route('/home', methods=['POST', 'GET']) 
def home():   
    return render_template('home.html') 

########################################### PHONE DATA ROUTE #############################################################

@server.route('/phone_1', methods=['POST', 'GET']) 
def phone_1(): 
    global allsensors
    if request.method == 'POST':  
        phone_1_data    = request.values

        time_date       = phone_1_data['time_stamp'].split(",") 
        datte           = time_date[0]
        time            = time_date[1]
        device_state    = phone_1_data['device_state']
        call_state      = phone_1_data['call_state'] 

        if device_state != "UNDEFINED":

            allsensors["device_state"] = device_state
            allsensors["call_state"] = call_state

            cur = dbConn.connection.cursor() 

            try:
                cur.execute("INSERT INTO phone_1 (date, time, device_state, call_state) VALUES(%s, %s, %s, %s)", (datte, time, device_state, call_state)) 
                dbConn.connection.commit() 
            except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
                print("DataError or IntegrityError")
                print(err)
                return FAIL
            except mysql.connector.ProgrammingError as err:
                print("Programming Error")
                print(err) 
                return FAIL
            except mysql.connector.Error as err:
                print(err)
                return FAIL
            except MySQLdb.Error as err: 
                print(err) 
                return FAIL  
            
            return SUCCESS
        return SUCCESS 
    return render_template('phone_1.html')  


########################################### WATCH DATA ROUTE #############################################################
@server.route('/watch_1', methods=['POST', 'GET']) 
def watch():
    cur = dbConn.connection.cursor()  
    global allsensors
    if request.method == 'POST': 
        data            = request.get_json(force=True)
        try:
            HRvalue     = data["heartRateVal"] 
        except:
            print("could not find key 'heartRateVal' in POST data") 
            return 

        if int(HRvalue) > 0: 
            datte               = str(datetime.date.today().strftime("%d/%m/%Y"))
            time                = str(datetime.datetime.now().strftime("%H:%M:%S"))   

            allsensors["heart_rate"]  = int(HRvalue)  

            
            try:
                cur.execute("INSERT INTO watch_1 (date, time, heart_rate) VALUES(%s, %s, %s)", (datte, time , HRvalue)) 
                dbConn.connection.commit() 
            except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
                print("DataError or IntegrityError")
                print(err)
                return FAIL
            except mysql.connector.ProgrammingError as err:
                print("Programming Error")
                print(err) 
                return FAIL
            except mysql.connector.Error as err:
                print(err)
                return FAIL
            except MySQLdb.Error as err: 
                print(err) 
                return FAIL
            return SUCCESS  
        return SUCCESS 
    else:
        #Handle get request
        heartRate = getAllData(cur, "watch_1")  

        graph_hr = pygal.Line() 
       
        graph_hr.add('Heart Rate', heartRate) 
        graph_hr_data = graph_hr.render_data_uri() 

        graph_data = graph_hr_data

    return render_template('watch_1.html',  graph_data=graph_data) 

########################################### LIBELIUM SENSOR 1 ROUTE ############################################################

@server.route('/libelium_1', methods=['POST', 'GET'])
def libelium_1(): 
    global allsensors
    cur = dbConn.connection.cursor() 

    if request.method == 'POST':
        libelium_1_data     = request.values

        datte               = str(datetime.date.today().strftime("%d/%m/%Y"))
        time                = str(datetime.datetime.now().strftime("%H:%M:%S")) 
        temp_libelium_1     = libelium_1_data['tp']
        pres_libelium_1     = libelium_1_data['pr']
        hum_libelium_1      = libelium_1_data['hu']
        lux_libelium_1      = libelium_1_data['lx']
        lum_libelium_1      = libelium_1_data['lm'] 

        allsensors["temperature_l1"]  = float(temp_libelium_1) 
        allsensors["pressure_l1"]     = float(pres_libelium_1)
        allsensors["humidity_l1"]     = float(hum_libelium_1)
        allsensors["lux_l1"]          = float(lux_libelium_1)
        allsensors["luminosity_l1"]   = float(lum_libelium_1) 
  
        try:
            cur.execute("INSERT INTO libelium_1 (date, time, temperature, pressure, humidity, lux, lumen) VALUES (%s, %s, %s, %s, %s, %s, %s)", (datte, time, temp_libelium_1, pres_libelium_1, hum_libelium_1, lux_libelium_1, lum_libelium_1))
            dbConn.connection.commit()

        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL 
        
        return SUCCESS
    else:
        temp, pres, hum, lux, lum = getAllData(cur, "libelium_1")
        
        blue_style  = Style(colors=["#00008B"])
        green_style = Style(colors=["#006400"]) 
        cadet_style = Style(colors=["#5F9EA0"])
        slate_style = Style(colors=["#2F4F4F"])

        graph_temp  = pygal.Line()
        graph_pres  = pygal.Line(style=blue_style)
        graph_hum   = pygal.Line(style=green_style)
        graph_lux   = pygal.Line(style=cadet_style)
        graph_lum   = pygal.Line(style=slate_style) 

        graph_temp.add('Temperature', temp) 
        graph_temp_data = graph_temp.render_data_uri()

        graph_pres.add('Pressure', pres) 
        graph_pres_data = graph_pres.render_data_uri()

        graph_hum.add('Humidity', hum) 
        graph_hum_data  = graph_hum.render_data_uri()

        graph_lux.add('lux', lux) 
        graph_lux_data  = graph_lux.render_data_uri()

        graph_lum.add('lumen', lum) 
        graph_lum_data  = graph_lum.render_data_uri()

        graph_data = [graph_temp_data, graph_pres_data, graph_hum_data, graph_lux_data, graph_lum_data]

    return render_template('libelium_1.html', graph_data=graph_data)   



################################################ LIBELIUM SENSOR 2 ROUTE ###################################################### 

@server.route('/libelium_2', methods=['POST', 'GET'])
def libelium_2(): 
    global allsensors
    cur = dbConn.connection.cursor() 

    if request.method == 'POST':
        libelium_2_data = request.values

        datte               = str(datetime.date.today().strftime("%d/%m/%Y")) 
        time                = str(datetime.datetime.now().strftime("%H:%M:%S")) 
        CO_libelium_2       = libelium_2_data['co']
        temp_libelium_2     = libelium_2_data['tp']
        pres_libelium_2     = libelium_2_data['pr']
        hum_libelium_2      = libelium_2_data['hu']  

        allsensors["co_l2"]             = float(CO_libelium_2)
        allsensors["temperature_l2"]    = float(temp_libelium_2)
        allsensors["pressure_l2"]       = float(pres_libelium_2)
        allsensors["humidity_l2"]       = float(hum_libelium_2)

        ########################## GOOGLE ASSISTANT ACTIONS #############################
        action1 = 'Switch everything off'
        action5 = 'Switch everything on'
        action4 = 'Turn on bulb one'    
        action8 = 'Set bulb one to RED'


        if (("co_l2" in allsensors) and ("max_co" in allsensors)): 
            if allsensors["co_l2"] > float(allsensors["max_co"]):
                co_brdcst = 'Broadcast Warning: carbon mono oxide level is %0.2f ppm, exit the building' % allsensors["co_l2"]  
                textinput.start_ga(co_brdcst) 
                if "action_co" in allsensors:
                    if allsensors["action_co"]   == "option1":
                        textinput.start_ga(action4)
                        textinput.start_ga(action8) 
                    elif allsensors["action_co"] == "option2":
                        textinput.start_ga(action1) 
                    elif allsensors["action_co"] == "option3": 
                        textinput.start_ga(action5)

        #################### ACTION TRIGGER LOGIC ########################
        
        try:
            cur.execute("INSERT INTO libelium_2 (date, time, CO, temperature, pressure, humidity) VALUES (%s, %s, %s, %s, %s, %s)", (datte, time, CO_libelium_2, temp_libelium_2, pres_libelium_2, hum_libelium_2)) 
            dbConn.connection.commit()
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  
        
        return SUCCESS
    else:
        #Handle get request
        co, temp, pres, hum = getAllData(cur, "libelium_2") 
        
        blue_style = Style(colors=["#00008B"])
        green_style = Style(colors=["#006400"]) 
        cadet_style = Style(colors=["#5F9EA0"])
       
        graph_co = pygal.Line() 
        graph_temp = pygal.Line(style=cadet_style) 
        graph_pres = pygal.Line(style=blue_style)
        graph_hum = pygal.Line(style=green_style)
       
        graph_co.add('CO level', co) 
        graph_co_data = graph_co.render_data_uri()

        graph_temp.add('Temperature', temp) 
        graph_temp_data = graph_temp.render_data_uri()

        graph_pres.add('Pressure', pres) 
        graph_pres_data = graph_pres.render_data_uri()

        graph_hum.add('Humidity', hum) 
        graph_hum_data = graph_hum.render_data_uri()

        graph_data = [graph_co_data, graph_temp_data, graph_pres_data, graph_hum_data] 


    return render_template('libelium_2.html',  graph_data=graph_data) 







################################################################################################################################
################################################################################################################################
################################## NEW SENSORS #################################################################################
################################################################################################################################
################################################################################################################################

@server.route('/user_defined/<usensor_name>', methods=['POST', 'GET']) 
def new_sensor(usensor_name):
    cur = dbConn.connection.cursor()  
    if request.method == 'POST':
        sensor_data = request.values

        sensor_name = usensor_name 

        registered_sensors = getSensorNames(cur) 

        if sensor_name in registered_sensors:
            datte               = str(datetime.date.today().strftime("%d/%m/%Y")) 
            time                = str(datetime.datetime.now().strftime("%H:%M:%S")) 

            column_names_list   = getColumnNames(cur, sensor_name).split(',') 

            sensor_data_values  = [datte, time] 
            for name in column_names_list:
                sensor_data_values.append(sensor_data[name])
            
            sensor_data_tuple   = tuple(sensor_data_values)

            ############################
            sql_insert_statmnt  = "INSERT INTO " + sensor_name + " (date, time"

            for name in column_names_list:
                sql_insert_statmnt += ", " + name
            
            sql_insert_statmnt += ") VALUES(%s, %s"

            for name in column_names_list:
                sql_insert_statmnt += ", %s"
            
            sql_insert_statmnt += ")" 

            #############################
            
            try:
                cur.execute(sql_insert_statmnt, sensor_data_tuple) 
                dbConn.connection.commit() 
            except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
                print("DataError or IntegrityError")
                print(err)
                return FAIL
            except mysql.connector.ProgrammingError as err:
                print("Programming Error")
                print(err) 
                return FAIL
            except mysql.connector.Error as err:
                print(err)
                return FAIL
            except MySQLdb.Error as err: 
                print(err) 
                return FAIL  
            
            return SUCCESS

        else:
            return FAIL 

        return 

####################################################################################
####################################################################################
@server.route('/add_sensor', methods=['POST', 'GET']) 
def add_sensor():
    cur = dbConn.connection.cursor()  
    global allsensors
    if request.form:
        sensor_init = request.form 

        allsensors["latest_table_name"]     = sensor_init["sensor_name"] 
        allsensors["latest_col_names"]      = sensor_init["col_names"] 

        sensor_name         = sensor_init["sensor_name"] 
        column_names        = sensor_init["col_names"] 
        column_names_list   = column_names.split(',') 
        column_no           = len(column_names_list) 

        button_display_all  = sensor_name + " (last 3000 datapoints)" 
        button_display_rt   = sensor_name + " (real-time)" 
    
        sql_create_table = "CREATE TABLE calm_computing." + sensor_name + "(id int AUTO_INCREMENT, date varchar(30), time varchar(30)" 

        for name in column_names_list:
            sql_create_table += ", " + name + " varchar(100)"
        
        sql_create_table += ", primary key(id));" 
                        

        try:
            cur.execute(sql_create_table) 
            print("finished creating table") 
            cur.execute("INSERT INTO tables_info ( \
                        sensor_name, column_no, column_names, display_all, display_rt) \
                        VALUES (%s, %s, %s, %s, %s)",
                        (sensor_name, column_no, column_names, button_display_all, button_display_rt))  

            dbConn.connection.commit()
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return SOMETHING_WRONG
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return SOMETHING_WRONG
        except mysql.connector.Error as err:
            print(err)
            return SOMETHING_WRONG
        except MySQLdb.Error as err: 
            print(err) 
            return SOMETHING_WRONG  
        
        return render_template('add_success.html', sensor_name=sensor_name.upper(), column_names=column_names_list)    


####################################################################################
####################################################################################
@server.route('/all_sensors', methods=['POST', 'GET']) 
def all_sensors():
    return render_template('all_sensors.html') 

###################################################################
@server.route('/addn_sensor', methods=['POST', 'GET']) 
def addn_sensors():
    return render_template('add_sensor.html') 


####################################################################################
####################################################################################
@server.route('/get_sensors', methods=['POST', 'GET']) 
def get_sensors(): 
    cur = dbConn.connection.cursor() 
    sensors = getSensorNames(cur) 

    sensors_list = [] 

    for sensor in sensors: 
        sensors_list.append({"name": sensor}) 

    all_sensors_json = jsonify(sensors_list)
    return all_sensors_json 


############################################################################################
def getNoOfColumns(cursor_object, table_name):
    try:
        cursor_object.execute("SELECT * FROM tables_info WHERE sensor_name=" + "\"" + table_name + "\"")  
        all_data  = cursor_object.fetchall() 
    except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
        print("DataError or IntegrityError")
        print(err)
        return FAIL
    except mysql.connector.ProgrammingError as err:
        print("Programming Error")
        print(err) 
        return FAIL
    except mysql.connector.Error as err:
        print(err)
        return FAIL
    except MySQLdb.Error as err: 
        print(err) 
        return FAIL  

    for row in all_data: 
        column_no = row[2] 

    return column_no 

############################################################################################
def getColumnNames(cursor_object, table_name):
    try:
        cursor_object.execute("SELECT * FROM tables_info WHERE sensor_name=" + "\"" + table_name + "\"")  
        all_data  = cursor_object.fetchall() 
    except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
        print("DataError or IntegrityError")
        print(err)
        return FAIL
    except mysql.connector.ProgrammingError as err:
        print("Programming Error")
        print(err) 
        return FAIL
    except mysql.connector.Error as err:
        print(err)
        return FAIL
    except MySQLdb.Error as err: 
        print(err) 
        return FAIL  

    for row in all_data: 
        column_names = row[3] 

    return column_names

############################################################################################
def getSensorNames(cursor_object):
    try:
        cursor_object.execute("SELECT * FROM tables_info")  
        all_data  = cursor_object.fetchall() 
    except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
        print("DataError or IntegrityError")
        print(err)
        return FAIL
    except mysql.connector.ProgrammingError as err:
        print("Programming Error")
        print(err) 
        return FAIL
    except mysql.connector.Error as err:
        print(err)
        return FAIL
    except MySQLdb.Error as err: 
        print(err) 
        return FAIL  

    sensor_names = [] 
    for row in all_data: 
        sensor_names.append(row[1]) 

    return sensor_names  


####################################################################################
########################### GET ANY SENSOR DATA AS JSON ############################
####################################################################################
@server.route('/data/<usensor>/<points>', methods=['POST', 'GET']) 
def data_acquire(usensor,points):
    global allsensors
    cur         = dbConn.connection.cursor() 
    sensor_name = usensor
    no_of_pnts  = points 

    any_data = getAnyData(cur, sensor_name, int(no_of_pnts)) 

    json_data = jsonify(any_data)

    return json_data 


############################################################################################
def getAnyData(cursor_object, table_name, no_of_pnts): 
        try:
            if no_of_pnts == 0:
                cursor_object.execute("SELECT * FROM " + table_name) 
            else:
                cursor_object.execute("SELECT * FROM " + table_name + " ORDER BY id DESC LIMIT " + str(no_of_pnts)) 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return SOMETHING_WRONG  
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return SOMETHING_WRONG
        except mysql.connector.Error as err:
            print(err)
            return SOMETHING_WRONG
        except MySQLdb.Error as err: 
            print(err) 
            return SOMETHING_WRONG
        
        column_names = getColumnNames(cursor_object, table_name).split(',') 

        data = [] 
    
        for row in reversed(all_data):
            temp_dict = {}
            temp_dict["id"]   = row[0]
            temp_dict["date"] = row[1]
            temp_dict["time"] = row[2]
            cnt = 3
            for name in column_names:
                temp_dict[name] = row[cnt]
                cnt += 1
            data.append(temp_dict)  

        return data 

############################################################################################
@server.route('/download_any', methods=['POST', 'GET'])  
def download_any(): 
    global allsensors
    if request.form:
        init_values     = request.form 
        table_name      = init_values['table_name'] 
        no_of_points    = int(init_values['points'])

        cur = dbConn.connection.cursor() 

        print (table_name) 

        if str(table_name) == "all":
            all_tables = getSensorNames(cur) 

            data_dict = []
            print(all_tables) 
            for table in all_tables: 
                data_dict.append(download_csv_file(cur,no_of_points,table)) 
            
            compression = zipfile.ZIP_DEFLATED
            zf = zipfile.ZipFile("all_data.zip", mode="w")
            
            for file in data_dict:
                fille = file.text() 
                zf.write(fille,compress_type=compression) 
            
            return zf
        else:
            csv_data = download_csv_file(cur,no_of_points,table_name)
            return csv_data 

    return SUCCESS    

############################################################################################
def download_csv_file(cur, no_of_points, table_name): 
    try:  
        if no_of_points > 0: 
            cur.execute("SELECT * FROM " + table_name + " ORDER BY id DESC LIMIT " + str(no_of_points))  
        else:
            cur.execute("SELECT * FROM "+ table_name) 

        result = cur.fetchall()

        output = io.StringIO()
        writer = csv.writer(output) 

        line = ['id', 'date', 'time']

        column_names = getColumnNames(cur,table_name).split(',')

        for name in column_names:
            line.append(name)  

        writer.writerow(line)

        for row in result: 
            line = [str(row[0]) , row[1] , row[2]] 
            cnt = 3
            for name in column_names:
                line.append(row[cnt])
                cnt += 1 
            writer.writerow(line)
        
        print("here")
        
        output.seek(0)
        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=" + table_name + "_data.csv"}) 
    except Exception as e:
        print(e)
        return SOMETHING_WRONG

    return SUCCESS 

############################################################################################
@server.route('/download_csv', methods=['POST', 'GET'])  
def download_csv():
    return render_template('download_any.html')  


################################################################################################################################
################################################################################################################################
################################## NEW SENSORS END #############################################################################
################################################################################################################################
################################################################################################################################









#################################### REAL TIME DATA LIBELIUM 1 ######################################################

@server.route('/libelium_1_rt', methods=['POST', 'GET']) 
def libelium_1_rt():
    return render_template('libelium_1_rt.html')   

@server.route('/l1_data', methods=['POST', 'GET']) 
def data_l1():
    cur = dbConn.connection.cursor() 
    temp, pres, hum, lux, lum = getRealTimeData(cur, "libelium_1")

    data = [temp, pres, hum, lux, lum] 
    json_data = json.dumps(data)
  
    return json_data 

@server.route('/l1_ltdata', methods=['POST', 'GET']) 
def latestdata_l1():
    cur = dbConn.connection.cursor()
    temp, pres, hum, lux, lum = getLatestData(cur, "libelium_1")

    data = [temp, pres, hum, lux, lum] 
    json_data = json.dumps(data)
  
    return json_data  

######################################## REAL TIME DATA LIBELIUM 2 ###################################################
@server.route('/libelium_2_rt', methods=['POST', 'GET']) 
def libelium_2_rt():
    return render_template('libelium_2_rt.html') 

@server.route('/l2_data', methods=['POST', 'GET']) 
def data_l2():
    cur = dbConn.connection.cursor() 
    co, temp, pres, hum = getRealTimeData(cur, "libelium_2")

    data = [co, temp, pres, hum] 
    json_data = json.dumps(data)
  
    return json_data 

@server.route('/l2_ltdata', methods=['POST', 'GET']) 
def latestdata_l2():
    cur = dbConn.connection.cursor()
    co, temp, pres, hum = getLatestData(cur, "libelium_2")  

    data = [co, temp, pres, hum] 
    json_data = json.dumps(data)
  
    return json_data     

######################################## REAL TIME DATA WATCH 1 ###################################################
@server.route('/watch_1_rt', methods=['POST', 'GET']) 
def watch_1_rt():
    return render_template('watch_1_rt.html') 

@server.route('/w1_data', methods=['POST', 'GET']) 
def data_w1():
    cur = dbConn.connection.cursor() 
    heartRate = getRealTimeData(cur, "watch_1")

    data = [heartRate]  
    json_data = json.dumps(data)
  
    return json_data 

@server.route('/w1_ltdata', methods=['POST', 'GET']) 
def latestdata_w1(): 
    cur = dbConn.connection.cursor()
    heartRate = getLatestData(cur, "watch_1")   

    data = [heartRate] 
    json_data = json.dumps(data) 
  
    return json_data     

############################################ GET LATEST PHONE STATE ######################################################
@server.route('/ph1_ltdata', methods=['POST', 'GET']) 
def latestdata_ph1(): 
    cur = dbConn.connection.cursor()
    time, dev_st, call_st = getLatestData(cur, "phone_1")   

    data = [time, dev_st, call_st] 
    json_data = json.dumps(data) 
  
    return json_data

############################################### SETTING EXTREME VALUES ####################################################
@server.route('/initialization', methods=['POST', 'GET'])
def initialization():
    global allsensors
    if request.form:
        init_values = request.form

        allsensors["max_temperature"]      = init_values["temp_max"]
        allsensors["action_temperature"]   = init_values["temperature"] 
    

        allsensors["max_pressure"]         = init_values["pres_max"]
        allsensors["action_pressure"]      = init_values["pressure"]

        allsensors["max_humidity"]         = init_values["hum_max"]
        allsensors["action_humidity"]      = init_values["humidity"]

        allsensors["min_lux"]              = init_values["lux_min"]
        allsensors["action_lux"]           = init_values["lux"] 

        allsensors["min_luminosity"]       = init_values["lum_min"]
        allsensors["action_luminosity"]    = init_values["luminosity"] 

        allsensors["max_co"]               = init_values["co_max"]
        allsensors["action_co"]            = init_values["co"]  

        allsensors["max_hr"]               = init_values["hr_max"]
        allsensors["action_hr"]            = init_values["hr"]   


        return "EXRTREME VALUES SET SUCCESSFULLY" 

    return render_template('initialization.html') 



################################### EXPORT DATA AS CSV ##############################################################

@server.route('/download_csv_1', methods=['POST', 'GET'])  
def download_data_1():
    try:
        cur = dbConn.connection.cursor() 

        cur.execute("SELECT * FROM libelium_1 ORDER BY id DESC LIMIT 5000") 
        result = cur.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        line = ['id', 'date', 'time', 'temperature', 'pressure', 'humidity', 'illuminance', 'luminosity'] 
        writer.writerow(line)

        for row in result:
            line = [str(row[0]) , row[1] , row[2], row[3], row[4], row[5], row[6], row[7]] 
            writer.writerow(line)

        output.seek(0)
        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=libelium_1_data.csv"}) 
    except Exception as e:
        print(e)  

    return 'SUCESS' 

@server.route('/download_csv_2', methods=['POST', 'GET'])  
def download_data_2():
    try:
        cur = dbConn.connection.cursor() 

        cur.execute("SELECT * FROM libelium_2 ORDER BY id DESC LIMIT 5000") 
        result = cur.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        line = ['id', 'date', 'time', 'CO', 'temperature', 'pressure', 'humidity'] 
        writer.writerow(line)

        for row in result:
            line = [str(row[0]) , row[1] , row[2], row[3], row[4], row[5], row[6]] 
            writer.writerow(line)

        output.seek(0)
        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=libelium_2_data.csv"}) 
    except Exception as e:
        print(e)  

    return 'SUCCESS' 

########################################## GET ALL DATA IN DATABASE ##################################################
def getAllData(cursor_object, table_name):

    if table_name == "libelium_1":
        try:
            cursor_object.execute("SELECT * FROM libelium_1 ORDER BY id DESC LIMIT 3000") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        temp    = []
        pres    = []
        hum     = []
        lux     = []
        lum     = [] 
    
        for row in reversed(all_data):
            temp.append(float(row[3])) 
            pres.append(float(row[4]))
            hum.append(float(row[5]))
            lux.append(float(row[6]))
            lum.append(float(row[7]))  
        return temp, pres, hum, lux, lum 

    elif table_name == "libelium_2":
        try:
            cursor_object.execute("SELECT * FROM libelium_2 ORDER BY id DESC LIMIT 3000") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        co      = []
        temp    = []
        pres    = []
        hum     = []

        for row in reversed(all_data):
            co.append(float(row[3])) 
            temp.append(float(row[4])) 
            pres.append(float(row[5]))
            hum.append(float(row[6]))  
        return co, temp, pres, hum

    elif table_name == "watch_1":
        try:
            cursor_object.execute("SELECT * FROM watch_1 ORDER BY id DESC LIMIT 3000") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        hr      = []
        
        for row in reversed(all_data):
            hr.append(float(row[3]))   
        return hr 



############################################ GET LAST X NUMBER OF DATA POINTS ############################################
def getRealTimeData(cursor_object, table_name): 
    if table_name == "libelium_1":
        try:
            cursor_object.execute("SELECT * FROM libelium_1 ORDER BY id DESC LIMIT 300") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  
 

        temp = []
        pres = []
        hum  = []
        lux  = []
        lum  = []

        for row in reversed(all_data):
            temp.append([row[2], float(row[3])]) 
            pres.append([row[2], float(row[4])])
            hum.append([row[2], float(row[5])])
            lux.append([row[2], float(row[6])])
            lum.append([row[2], float(row[7])]) 
        return temp, pres, hum, lux, lum 

    elif table_name == "libelium_2":
        try:
            cursor_object.execute("SELECT * FROM libelium_2 ORDER BY id DESC LIMIT 300") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error") 
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        co      = []
        temp    = []
        pres    = []
        hum     = []

        for row in reversed(all_data):
            co.append([row[2], float(row[3])]) 
            temp.append([row[2], float(row[4])]) 
            pres.append([row[2], float(row[5])])
            hum.append([row[2], float(row[6])]) 
        return co, temp, pres, hum
    
    elif table_name == "watch_1":
        try:
            cursor_object.execute("SELECT * FROM watch_1 ORDER BY id DESC LIMIT 300") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        hr      = []
        
        for row in reversed(all_data):
            hr.append([row[2], float(row[3])])   
        return hr 



########################################## GET THE MOST RECENT DATAPOINT #######################################################
def getLatestData(cursor_object, table_name):   

    if table_name == "libelium_1":
        try:
            cursor_object.execute("SELECT * FROM libelium_1 ORDER BY id DESC LIMIT 1") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL   

        temp = []
        pres = []
        hum  = []
        lux  = []
        lum  = []

        for row in reversed(all_data):
            temp.append([row[2], float(row[3])]) 
            pres.append([row[2], float(row[4])])
            hum.append([row[2], float(row[5])])
            lux.append([row[2], float(row[6])])
            lum.append([row[2], float(row[7])]) 
        return temp, pres, hum, lux, lum 

    elif table_name == "libelium_2": 
        try:
            cursor_object.execute("SELECT * FROM libelium_2 ORDER BY id DESC LIMIT 1") 
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        co      = []
        temp    = []
        pres    = []
        hum     = []

        for row in reversed(all_data):
            co.append([row[2], float(row[3])]) 
            temp.append([row[2], float(row[4])]) 
            pres.append([row[2], float(row[5])])
            hum.append([row[2], float(row[6])]) 
        return co, temp, pres, hum
    
    elif table_name == "phone_1":
        try:
            cursor_object.execute("SELECT * FROM phone_1 ORDER BY id DESC LIMIT 1")  
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        time            = []
        device_state    = []
        call_state      = []

        for row in reversed(all_data):
            time.append(["time", row[2]])
            device_state.append(["device_state", row[3]])
            call_state.append(["call_state",row[4]])  

        return time, device_state, call_state

    elif table_name == "watch_1":
        try:
            cursor_object.execute("SELECT * FROM watch_1 ORDER BY id DESC LIMIT 1")  
            all_data  = cursor_object.fetchall() 
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            return FAIL
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err) 
            return FAIL
        except mysql.connector.Error as err:
            print(err)
            return FAIL
        except MySQLdb.Error as err: 
            print(err) 
            return FAIL  


        hr      = []
        
        for row in reversed(all_data):
            hr.append([row[2], float(row[3])])    
        return hr 
 




###################################### START SERVER ############################################################# 

if __name__ == '__main__':
   server.run(debug=True, host='replace_the_ip_address', port='80')   
