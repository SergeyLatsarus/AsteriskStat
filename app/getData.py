import MySQLdb
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import mysqlconfig as cfg
from datetime import datetime
from managers import Manager
from flask.ext.wtf import Form
from wtforms.fields import DateField
from wtforms.validators import Required
from config import managers_names, dealingers_names

managers = {}
managers_names.update(dealingers_names)


class UserDate(Form):
    input_date_from = DateField( 'input_date_from' ,validators = [Required()])
    input_date_to = DateField( 'input_date_to' ,validators = [Required()])


def query(input_date_from, input_date_to):

    mysql = cfg.mysql
    conn = MySQLdb.connect(mysql['host'], mysql['user'], mysql['passwd'], mysql['db'])
    c = conn.cursor()

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
                    FROM CDR.cdr \
                    WHERE calldate BETWEEN '%s' AND '%s' " % (query_date_from_b, query_date_to))
            rows = c.fetchall()
    else:
        c.execute("SELECT  cnam, src, dstchannel, calldate, billsec \
                        FROM CDR.cdr \
                        WHERE calldate like '%s' " % query_date_from)
        rows = c.fetchall()

    return rows


def is_incoming_call(destination):
    is_incoming = bool(re.search('SIP/\d\d\d', destination))
    return is_incoming


def is_succesed(caller_id, bill_sec):
    if bill_sec > 60:
        managers[caller_id].succesed_calls += 1
    else:
        managers[caller_id].unsuccesed_calls += 1


def is_manager_exist(caller_id):
    if caller_id not in managers and managers_names.has_key(caller_id):
         managers[caller_id] = Manager(caller_id, managers_names[caller_id])


def add_outgoing_details(caller_id, bill_sec, call_hour ):
    is_succesed(caller_id, bill_sec)
    managers[caller_id].outbound_calls += 1
    managers[caller_id].total_calls_time += int(round(bill_sec / 60.0))
    managers[caller_id].store_call_out(call_hour, 1 if bill_sec > 60 else 0, 0 if bill_sec > 60 else 1, bill_sec)
    managers[caller_id].average_time  = managers[caller_id].avg_time()


def add_incoming_details(caller_id, bill_sec, call_hour ):
    is_succesed(caller_id, bill_sec)
    managers[caller_id].inbound_calls += 1
    managers[caller_id].total_calls_time += int(round(bill_sec / 60.0))
    managers[caller_id].store_call_in(call_hour, 1 if bill_sec > 60 else 0, 0 if bill_sec > 60 else 1, bill_sec)
    managers[caller_id].average_time  = managers[caller_id].avg_time()


def main(requsted_date_from, requsted_date_to):

    managers.clear()
    calls = query(requsted_date_from, requsted_date_to)
    for call in calls:
        call_hour = datetime.strftime(call[3], "%H")
        caller_id = call[1]
        destination = call[2]
        bill_sec = 0 if call[4] < 30 else call[4]
        incoming_to_caller_id = (call[2])[4:7] if bool(re.search('SIP/\d\d\d', call[2])) else None

        is_manager_exist(caller_id)
        is_manager_exist(incoming_to_caller_id)

        if is_incoming_call(destination) and managers.has_key(incoming_to_caller_id):
            add_incoming_details(incoming_to_caller_id, bill_sec, call_hour)
        elif managers.has_key( caller_id):
            add_outgoing_details(caller_id, bill_sec, call_hour)

    return managers



