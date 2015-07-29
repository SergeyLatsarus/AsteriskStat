import MySQLdb
import re
import mysqlconfig as cfg
from datetime import datetime
from managers import Manager
from flask.ext.wtf import Form
from wtforms.fields import DateField
from wtforms.validators import Required


class UserDate(Form):
    input_date_from = DateField( 'input_date_from' ,validators = [Required()])
    input_date_to = DateField( 'input_date_to' ,validators = [Required()])

def query(input_date_from, input_date_to):
    mysql = cfg.mysql
    conn = MySQLdb.connect(mysql['host'], mysql['user'], mysql['passwd'], mysql['db'])

    c = conn.cursor()
    managers = {}
    callers_name_map = {}

    from_date = str(input_date_from)
    to_date = str(input_date_to)

    requsted_date_from = from_date[6:10] + '-' + from_date[0:2] + '-' + from_date[3:5]
    requsted_date_to = to_date[6:10] + '-' + to_date[0:2] + '-' + to_date[3:5]

    now = datetime.strftime(datetime.now(), "%Y-%m-%d")

    query_date_from = (requsted_date_from if from_date else now) + ' %:_____'
    query_date_from_b = (requsted_date_from if from_date else now)  + ' 00:00:01'
    query_date_to = (requsted_date_to if to_date else now) + ' 23:59:59'

    if query_date_from != None and query_date_to != None:
            c.execute("SELECT  cnam, src, dstchannel, calldate, billsec \
                    FROM asteriskcdrdb.cdr \
                    WHERE calldate BETWEEN '%s' AND '%s' " % (query_date_from_b, query_date_to))
            rows = c.fetchall()
    else:
        c.execute("SELECT  cnam, src, dstchannel, calldate, billsec \
                        FROM asteriskcdrdb.cdr \
                        WHERE calldate like '%s' " % query_date_from)
        rows = c.fetchall()

    src = '%___'
    c.execute("SELECT DISTINCT cnam, src FROM asteriskcdrdb.cdr WHERE src like '%s'" % src)
    rows_src = c.fetchall()

    for eachRow in rows_src:
        if bool(re.search('^\d\d\d$', eachRow[1])):
            callers_name_map[eachRow[1]] = eachRow[0]
            print callers_name_map
    for eachRow in rows:

        incoming_to_caller_name = (eachRow[2])[4:7] if bool(re.search('SIP/\d\d\d', eachRow[2])) else None
        caller_name = eachRow[0]
        caller_id = eachRow[1]
        bill_sec = eachRow[4]
        call_hour = datetime.strftime(eachRow[3], "%H")
        is_succeeded = bill_sec > 0
        is_incoming = bool(re.search('SIP/\d\d\d', eachRow[2]))

        if bool(re.search('^\d\d\d$', eachRow[1])):

            if caller_id in managers:
                if is_succeeded:
                    managers[caller_id].succesed_calls += 1
                else:
                    managers[caller_id].unsuccesed_calls += 1

                if is_incoming:
                    managers[caller_id].inbound_calls += 1
                else:
                    managers[caller_id].outbound_calls += 1

                managers[caller_id].total_calls_time += int(round(bill_sec / 60.0))
                managers[caller_id].store_call(call_hour,
                                               is_succeeded, bill_sec)
                managers[caller_id].average_time  = managers[caller_id].avg_time()


            else:
                managers[caller_id] = Manager(caller_id, caller_name)
                if is_succeeded:
                    managers[caller_id].succesed_calls += 1
                else:
                    managers[caller_id].unsuccesed_calls += 1

                if is_incoming:
                    managers[caller_id].inbound_calls += 1
                else:
                    managers[caller_id].outbound_calls += 1


                managers[caller_id].total_calls_time += int(round(bill_sec / 60.0))
                managers[caller_id].store_call(call_hour,
                                               is_succeeded, bill_sec)
                managers[caller_id].average_time  = managers[caller_id].avg_time()

        else:
            if incoming_to_caller_name:
                if incoming_to_caller_name in managers:
                    if is_succeeded:
                        managers[incoming_to_caller_name].succesed_calls += 1
                    else:
                        managers[incoming_to_caller_name].unsuccesed_calls += 1

                    if is_incoming:
                        managers[incoming_to_caller_name].inbound_calls += 1
                    else:
                        managers[incoming_to_caller_name].outbound_calls += 1


                    managers[incoming_to_caller_name].total_calls_time += int(round(bill_sec / 60.0))
                    managers[incoming_to_caller_name].store_call(call_hour,
                                                   is_succeeded, bill_sec)
                    managers[incoming_to_caller_name].average_time = managers[incoming_to_caller_name].avg_time()


                else:
                    managers[incoming_to_caller_name] = \
                        Manager(incoming_to_caller_name,
                                callers_name_map[incoming_to_caller_name])
                    if is_succeeded:
                        managers[incoming_to_caller_name].succesed_calls += 1
                    else:
                        managers[incoming_to_caller_name].unsuccesed_calls += 1

                    if is_incoming:
                        managers[incoming_to_caller_name].inbound_calls += 1
                    else:
                        managers[incoming_to_caller_name].outbound_calls += 1


                    managers[incoming_to_caller_name].total_calls_time += int(round(bill_sec / 60.0))
                    managers[incoming_to_caller_name].store_call(call_hour,
                                                   is_succeeded, bill_sec)
                    managers[incoming_to_caller_name].average_time  = managers[incoming_to_caller_name].avg_time()


    return managers

