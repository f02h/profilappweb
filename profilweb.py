import sqlite3
from bottle import route, run, debug, template, request, static_file, error, TEMPLATE_PATH, static_file, redirect
import os, sys
import csv
import re
import bottle
from collections import defaultdict


# only needed when you run Bottle on mod_wsgi
from bottle import default_app
#TEMPLATE_PATH.insert(0, './aluprofili/view')
bottle.TEMPLATE_PATH.insert(0, '/home/pi/profilweb/view')

dirname = os.path.dirname(sys.argv[0])

@route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/asset/css')

@route('/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root=dirname+'/static/asset/js')

def def_value():
    return "Not Present"

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))

@route('/upload', method=['GET', 'POST'])
def do_upload():
    conn = sqlite3.connect('/home/pi/profilapp/todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO job (length, qty,idProfile,loader, qtyD, done) VALUES (?,?,?,?,?,?)",
              (1000, 1, 0, 0, 0,0))

    data = request.files.upload
    if data and data.file:

        category = 'test'
        upload = request.files.get('upload')
        iQty = 1
        if request.GET.quantity:
            iQty = request.GET.quantity
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.csv'):
            return "File extension not allowed."

        save_path = "/tmp/{category}".format(category=category)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path,overwrite=True)

        conn = sqlite3.connect('/home/pi/profilapp/todo.db')
        c = conn.cursor()

        with open(file_path, newline='', encoding='cp1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    part = row[0].encode().decode("utf-8")
                    qty = re.search("[0-9]+x", str(part))
                    try:
                        if qty.group(0):
                            part = part.lstrip(qty.group(0))
                            qty = qty.group(0).rstrip("x")
                        else:
                            qty = 0
                    except:
                        qty = 0

                    if qty:
                        if "profil" not in str(part):
                            c.execute("INSERT INTO vrtalka (name,qty,dimensions,status,project) VALUES (?,?,?,?,?)",
                                      (part, qty * iQty, float(round(float(row[2]), 2)), 1, name))

                        c.execute("INSERT INTO zaga (name,qty,dimensions,status,project) VALUES (?,?,?,?,?)", (part,qty * iQty,float(round(float(row[2]), 2)), 1, name))
                        conn.commit()
                    line_count += 1
        c.close()

        return "File successfully saved to '{0}'.".format(save_path)

    return template('upload.tpl')


@route('/upload2', method=['GET', 'POST'])
def do_upload2(db):
    data = request.files.upload
    if data and data.file:

        category = 'test'
        upload = request.files.get('upload')
        iQty = 1
        if request.GET.quantity:
            iQty = request.GET.quantity
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.csv'):
            return "File extension not allowed."

        save_path = "/tmp/{category}".format(category=category)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path,overwrite=True)

        #conn = sqlite3.connect('/home/pi/aluprofili/todo.db')
        #c = conn.cursor()
        items = {}
        with open(file_path, newline='', encoding='cp1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:

                prefix = False

                if line_count == 0:
                    line_count += 1
                else:
                    part = row[0].encode().decode("utf-8")
                    qty = re.search("[0-9]+x", str(part))
                    try:
                        if qty.group(0):
                            prefix = True
                            part = part.lstrip(qty.group(0))
                            qty = qty.group(0).rstrip("x")
                        else:
                            qty = 0
                    except:
                        qty = 0

                    if qty == 0:
                        qty = row[1]

                    if qty:
                        itemDetails = {}
                        if part not in items.keys():
                            subType = str(round(float(row[5]), 2))
                            if part == 'Plehek':
                                if subType == '31.5' or subType == '19.0':
                                    subType = '19.0'
                                elif subType == '24.0' or subType == '30.0':
                                    subType = '30.0'
                                elif subType == '40.0' or subType == '35':
                                    subType = '40.0'

                            itemDetails = {'qty': qty * iQty, 'width':float(round(float(row[3]), 2)),'length':float(round(float(row[4]), 2)),'subType':subType,'material':row[9],'status':1,'project':name}
                            items[part] = itemDetails
                        else:
                            itemDetails = dict(items[part])
                            itemDetails['qty'] = int(itemDetails['qty']) + 1
                            items[part] = itemDetails

                    line_count += 1

        for item in items.keys():
            db.execute("INSERT INTO items (type,qty,width,length,subType,material,status,project) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (item,items[item]['qty'],items[item]['width'],items[item]['length'],items[item]['subType'],items[item]['material'], items[item]['status'], items[item]['project']))

        return "File successfully saved to '{0}'.".format(save_path)

    return template('upload2.tpl')



@route('/json<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect('/home/pi/aluprofili/todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(host='0.0.0.0',reloader=True)
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment

