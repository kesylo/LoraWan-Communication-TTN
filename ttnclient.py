import csv
import time
import ttn
import math
import pandas as pd
from datetime import datetime

app_id = "kesyloappid94"
access_key = "ttn-account-v2.CtoT7qzOAJjHpLasdo50RfQr673dDaRISe3h7Zhy6Uo"
x_axis = 0
LORA1_id = "a8610a3233328f09"
LORA2_id = "a8610a3233458209"
fieldsName = ["x_values", "temperature", "ligth"]

handler = ttn.HandlerClient(app_id, access_key)

# Create csv lora 
with open('lora1.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
    csv_writer.writeheader()

# Create csv lora 1
with open('lora2.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
    csv_writer.writeheader()


# convert temp (Mv) in (degree)
def temp_to_degree(tempraw):
    tmp = (tempraw / 1023) * 3300
    T = 870.6 - tmp
    T1 = 0.00704 * T
    T2 = math.sqrt(30.316036 + T1)
    T3 = ((5.506 - T2) / (-0.00362))
    temp_in_degree = T3 + 30
    return temp_in_degree


# convert temp (Mv) in (degree)
def ligth_to_lux(ligthraw):
    l_mv = ligthraw * 1.6666667
    resistance = 10000
    luminosite_ice = (l_mv * 1000) / resistance
    luminosite_lux = luminosite_ice * 1.667  # 1.667 car 60 µA = 100 Lux
    return luminosite_lux


# Add first line in lora1
with open('lora1.csv', 'a') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
    data = {
        "x_values": 0,
        "temperature": 0,
        "ligth": 0
    }
    # write to file
    csv_writer.writerow(data)

# Add first line in lora2
with open('lora2.csv', 'a') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
    data = {
        "x_values": 0,
        "temperature": 0,
        "ligth": 0
    }
    # write to file
    csv_writer.writerow(data)


def import_csv(csvfilename):
    data = []
    row_index = 0
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        for row in reader:
            if (row):
                row_index += 1
                columns = [str(row_index), row[0], row[1], row[2]]
                data.append(columns)
    return data


def updatelora1(x_value, temperature, ligth):
    with open('lora1.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
        # prepare the data
        temp_in_deg = temp_to_degree(float(temperature))
        ligth_in_lux = ligth_to_lux(float(ligth))
        data = {
            "x_values": x_value,
            "temperature": temp_in_deg,
            "ligth": ligth_in_lux
        }
        # write to file
        csv_writer.writerow(data)


def updatelora2(x_value, temperature, ligth):
    with open('lora2.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
        # prepare the data
        temp_in_deg = temp_to_degree(float(temperature))
        ligth_in_lux = ligth_to_lux(float(ligth))
        data = {
            "x_values": x_value,
            "temperature": temp_in_deg,
            "ligth": ligth_in_lux
        }
        # write to file
        csv_writer.writerow(data)


def addLineLora2(x, temperature, ligth):
    with open('lora2.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
        data = {
            "x_values": x,
            "temperature": temperature,
            "ligth": ligth
        }
        # write to file
        csv_writer.writerow(data)


def addLineLora1(x, temperature, ligth):
    with open('lora1.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldsName)
        data = {
            "x_values": x,
            "temperature": temperature,
            "ligth": ligth
        }
        # write to file
        csv_writer.writerow(data)


print("Fetching Data")


# ------------------------------------------------------------------------ TTN
def uplink_callback(msg, client):
    # print(msg[7][0])
    # print(msg[1])

    # LORA 1
    if msg[1] == LORA1_id:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("Lora 1: " + msg[7][0] + " - " + dt_string)
        data = msg[7][0]

        datacsv = import_csv('lora1.csv')
        last_row = datacsv[-1]
        x = int(last_row[1])
        x += 1

        datacsv = import_csv('lora2.csv')
        last_row = datacsv[-1]
        last_temp2 = last_row[2]
        last_ligth2 = last_row[3]

        if '-' in data:
            splitted = data.split('-')
            updatelora1(x, splitted[0], splitted[1])
            addLineLora2(x, last_temp2, last_ligth2)

        # LORA 2
    if msg[1] == LORA2_id:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("Lora 2: " + msg[7][0] + " - " + dt_string)
        data = msg[7][0]

        datacsv = import_csv('lora2.csv')
        last_row = datacsv[-1]
        x = int(last_row[1])
        x += 1

        datacsv = import_csv('lora1.csv')
        last_row = datacsv[-1]
        last_temp1 = last_row[2]
        last_ligth1 = last_row[3]

        if '-' in data:
            splitted = data.split('-')
            updatelora2(x, splitted[0], splitted[1])
            addLineLora1(x, last_temp1, last_ligth1)


# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()
time.sleep(12000)
mqtt_client.close()
