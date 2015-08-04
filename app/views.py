from flask import render_template, flash, redirect, request
from app import app
from getData import UserDate
import getData


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])


def index():

    managers_num = ('205', '207', '223', '251', '300', '221', '227')
    work_hours = ('08','09','10','11','12','13','14','15','16','17','18','19','20')

    form = UserDate(request.form)
    requsted_date_from = form.input_date_from._value()
    requsted_date_to = form.input_date_to._value()

    all_managers = getData.query(requsted_date_from, requsted_date_to)
    visible_managers = {}

    for num in managers_num:
        if all_managers.has_key(num):
            visible_managers[num] = all_managers[num]


    return render_template("index.html",
        work_hours = work_hours,
        today = requsted_date_from,
        title = 'Get Report',
        form = form,
        managers = visible_managers)


@app.route('/config')
def config():

    return render_template("config.html")