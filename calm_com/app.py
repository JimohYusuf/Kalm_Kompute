######################################### IMPORTS ##########################################################################################################################################################
from flask import Flask, render_template, request, make_response, Response
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

from pygal.style import Style 
from datetime import date

import textinput 
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

############################################################## GLOBAL VARIABLES ######################################
#G Constants
SUCCESS = "POST Success"
FAIL    = "POST Failed"

#flask handle
server = Flask(__name__)
#assistant
assist = Assistant(server, project_id='sensorreadings-qccmpb')

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
        
        datte           = str(datetime.date.today().strftime("%d/%m/%Y"))
        time            = str(datetime.datetime.now().strftime("%H:%M:%S")) 

        phone_1_data    = request.values
        time_stamp      = phone_1_data['time_stamp'] 
        device_state    = phone_1_data['device_state']
        call_state      = phone_1_data['call_state'] 

        allsensors["device_state"] = device_state
        allsensors["call_state"] = call_state

        cur = dbConn.connection.cursor() 

        try:
            cur.execute("INSERT INTO mphone_1 (date, time, device_state, call_state) VALUES(%s, %s, %s, %s)", (datte, time , device_state, call_state)) 
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
    return render_template('phone_1.html')  


########################################### WATCH DATA ROUTE #############################################################
@server.route('/watch_1', methods=['POST', 'GET']) 
def watch():
    global allsensors
    if request.method == 'POST': 
        data            = request.get_json(force=True)
        try:
            HRvalue     = data["heartRateVal"] 
        except:
            print("could not find key 'heartRateVal' in POST data") 
            return 

        datte               = str(datetime.date.today().strftime("%d/%m/%Y"))
        time                = str(datetime.datetime.now().strftime("%H:%M:%S"))   

        allsensors["heart_rate"]  = int(HRvalue)   

        cur = dbConn.connection.cursor() 

        try:
            cur.execute("INSERT INTO mwatch_1 (date, time, heart_rate) VALUES(%s, %s, %s)", (datte, time , HRvalue)) 
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
        heartRate = getAllData(cur, "mwatch_1")  

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
            cur.execute("INSERT INTO mlibelium_1 (date, time, temperature, pressure, humidity, lux, lumen) VALUES (%s, %s, %s, %s, %s, %s, %s)", (datte, time, temp_libelium_1, pres_libelium_1, hum_libelium_1, lux_libelium_1, lum_libelium_1))
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
        temp, pres, hum, lux, lum = getAllData(cur, "mlibelium_1")
        
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
            cur.execute("INSERT INTO mlibelium_2 (date, time, CO, temperature, pressure, humidity) VALUES (%s, %s, %s, %s, %s, %s)", (datte, time, CO_libelium_2, temp_libelium_2, pres_libelium_2, hum_libelium_2)) 
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
        co, temp, pres, hum = getAllData(cur, "mlibelium_2") 
        
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

#################################### REAL TIME DATA LIBELIUM 1 ######################################################

@server.route('/libelium_1_rt', methods=['POST', 'GET']) 
def libelium_1_rt():
    return render_template('libelium_1_rt.html')   

@server.route('/l1_data', methods=['POST', 'GET']) 
def data_l1():
    cur = dbConn.connection.cursor() 
    temp, pres, hum, lux, lum = getRealTimeData(cur, "mlibelium_1")

    data = [temp, pres, hum, lux, lum] 
    json_data = json.dumps(data)
  
    return json_data 

@server.route('/l1_ltdata', methods=['POST', 'GET']) 
def latestdata_l1():
    cur = dbConn.connection.cursor()
    temp, pres, hum, lux, lum = getLatestData(cur, "mlibelium_1")

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
    co, temp, pres, hum = getRealTimeData(cur, "mlibelium_2")

    data = [co, temp, pres, hum] 
    json_data = json.dumps(data)
  
    return json_data 

@server.route('/l2_ltdata', methods=['POST', 'GET']) 
def latestdata_l2():
    cur = dbConn.connection.cursor()
    co, temp, pres, hum = getLatestData(cur, "mlibelium_2")  

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
    heartRate = getRealTimeData(cur, "mwatch_1")

    data = [heartRate]  
    json_data = json.dumps(data)
  
    return json_data 

@server.route('/w1_ltdata', methods=['POST', 'GET']) 
def latestdata_w1(): 
    cur = dbConn.connection.cursor()
    heartRate = getLatestData(cur, "mwatch_1")   

    data = [heartRate] 
    json_data = json.dumps(data) 
  
    return json_data     

############################################ GET LATEST PHONE STATE ######################################################
@server.route('/ph1_ltdata', methods=['POST', 'GET']) 
def latestdata_ph1(): 
    cur = dbConn.connection.cursor()
    time, dev_st, call_st = getLatestData(cur, "mphone_1")   

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

@server.route('/download_csv_1')  
def download_data_1():
    try:
        cur = dbConn.connection.cursor() 

        cur.execute("SELECT * FROM mlibelium_1 ORDER BY id DESC LIMIT 5000") 
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

@server.route('/download_csv_2')  
def download_data_2():
    try:
        cur = dbConn.connection.cursor() 

        cur.execute("SELECT * FROM mlibelium_2 ORDER BY id DESC LIMIT 5000") 
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

    return 'SUCESS' 

########################################## GET ALL DATA IN DATABASE ##################################################
def getAllData(cursor_object, table_name):

    if table_name == "mlibelium_1":
        try:
            cursor_object.execute("SELECT * FROM mlibelium_1 ORDER BY id DESC LIMIT 3000") 
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

    elif table_name == "mlibelium_2":
        try:
            cursor_object.execute("SELECT * FROM mlibelium_2 ORDER BY id DESC LIMIT 3000") 
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

    elif table_name == "mwatch_1":
        try:
            cursor_object.execute("SELECT * FROM mwatch_1 ORDER BY id DESC LIMIT 3000") 
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
    if table_name == "mlibelium_1":
        try:
            cursor_object.execute("SELECT * FROM mlibelium_1 ORDER BY id DESC LIMIT 300") 
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

    elif table_name == "mlibelium_2":
        try:
            cursor_object.execute("SELECT * FROM mlibelium_2 ORDER BY id DESC LIMIT 300") 
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
    
    elif table_name == "mwatch_1":
        try:
            cursor_object.execute("SELECT * FROM mwatch_1 ORDER BY id DESC LIMIT 300") 
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

    if table_name == "mlibelium_1":
        try:
            cursor_object.execute("SELECT * FROM mlibelium_1 ORDER BY id DESC LIMIT 1") 
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

    elif table_name == "mlibelium_2":
        try:
            cursor_object.execute("SELECT * FROM mlibelium_2 ORDER BY id DESC LIMIT 1") 
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
    
    elif table_name == "mphone_1":
        try:
            cursor_object.execute("SELECT * FROM mphone_1 ORDER BY id DESC LIMIT 1")  
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

    elif table_name == "mwatch_1":
        try:
            cursor_object.execute("SELECT * FROM mwatch_1 ORDER BY id DESC LIMIT 1")  
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
   server.run(debug=True, host='192.168.1.159', port='80')   
