import MetaTrader5 as mt5
from database import Status
import datetime as dt
import time
import time_server as ts

def time_now():
    time = dt.datetime.now()
    time = time.strftime("%H:%M:%S  //  %d-%m-%Y")
    return time

connection = "OK"
on = 0
off = 0
while True:
    try:
        connection_stat = mt5.initialize()
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        status = Status()
        stat = str(status.find_status(collection="Status"))
        while "ON" in stat:
            if on == 0:
                print("System activated at :", time_now())

                off = 0
                on += 1
                connection_stat = mt5.initialize()
                print(connection_stat["status"])
                if (int(connection_stat["status"])) == 0:
                    print("MT5 server is : Connected")
                else:
                    print("MT5 server is : Disconnected")
            ts.server_tm()
            stat = status.find_status(collection="Status")

        if off == 0:
            print("System disactivated at :", time_now())
            on = 0
            off += 1
    except Exception as error:
        if "HTTPSConnectionPool" in str(error) and connection == "OK":
            print("Connection timeout ! .......")
            connection_stat = "Error"
            time.sleep(30)

