# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template, request
from app import app
from getData import UserDate
import getData
import salesforce_dashboard
from config import managers_num, managers_names, dealingers_num, work_hours, all_hours


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])

def index():

    form = UserDate(request.form)
    requsted_date_from = form.input_date_from._value()
    requsted_date_to = form.input_date_to._value()

    all_managers = getData.main(requsted_date_from, requsted_date_to)
    visible_managers = {}
    visible_dealingers = {}

    for num in managers_num:
        if all_managers.has_key(num):
            visible_managers[num] = all_managers[num]

    for num in dealingers_num:
        if all_managers.has_key(num):
            visible_dealingers[num] = all_managers[num]

    return render_template("index.html",
        work_hours = work_hours,
        all_hours = all_hours,
        today = requsted_date_from,
        title = 'Get Report',
        form = form,
        dealingers = visible_dealingers,
        managers_names = managers_names,
        visible_managers = visible_managers,
        managers = all_managers)


@app.route('/stat', methods = ['GET', 'POST'])

def stat():

    form = UserDate(request.form)
    requsted_date_from = form.input_date_from._value()
    requsted_date_to = form.input_date_to._value()

    all_managers = getData.main(requsted_date_from, requsted_date_to)
    visible_managers = {}
    visible_dealingers = {}

    for num in managers_num:
        if all_managers.has_key(num):
            visible_managers[num] = all_managers[num]

    for num in dealingers_num:
        if all_managers.has_key(num):
            visible_dealingers[num] = all_managers[num]

    return render_template("stat.html",
        work_hours = work_hours,
        all_hours = all_hours,
        today = requsted_date_from,
        title = 'Get Report',
        form = form,
        dealingers = visible_dealingers,
        managers_names = managers_names,
        visible_managers = visible_managers,
        managers = all_managers)


@app.route('/config')
def config():

    return render_template("config.html")

@app.route('/dashboard')
def dashboard():

    funding_by_users,\
    funding_user_names,\
    withdrawal_by_users,\
    withdrawal_user_names,\
    converted_leads_by_users,\
    converted_leads_user_names,\
    sum_of_incentive_deposites_by_users,\
    sum_of_incentive_user_names,\
    outbount_calls_to_accounts_by_users,\
    outbount_calls_to_accounts_user_names, \
    outbount_calls_to_leads_by_users,\
    outbount_calls_to_leads_user_names \
    = salesforce_dashboard.main()

    return render_template("dashboard.html",
                           funding_by_users = funding_by_users,
                           funding_user_names = funding_user_names,
                           withdrawal_by_users = withdrawal_by_users,
                           withdrawal_user_names = withdrawal_user_names,
                           converted_leads_by_users = converted_leads_by_users,
                           converted_leads_user_names = converted_leads_user_names,
                           sum_of_incentive_deposites_by_users = sum_of_incentive_deposites_by_users,
                           sum_of_incentive_user_names = sum_of_incentive_user_names,
                           outbount_calls_to_accounts_by_users = outbount_calls_to_accounts_by_users,
                           outbount_calls_to_accounts_user_names = outbount_calls_to_accounts_user_names,
                           outbount_calls_to_leads_by_users = outbount_calls_to_leads_by_users,
                           outbount_calls_to_leads_user_names = outbount_calls_to_leads_user_names)

