from django.shortcuts import redirect, render
import requests, json
from django.db import connection
from . import models
from datetime import datetime, date

# Create your views here.

# class book:
#     def __init__(self, id):
#         self.id = id
bookid = 0

from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def books(request):
    title = request.POST['title']
    response = requests.get('https://frappe.io/api/method/frappe-library?page=1&title=' + title)
    data = response.text
    parse_json = json.loads(data)
    print(parse_json)
    # cursor = connection.cursor()
    # for list in parse_json['message']:
    #     cursor.execute('INSERT INTO books(bknm, bookid) VALUES(%s, %s)', [list['title'], list['bookID']])
    
    return render(request, 'dashboard.html', { 'parse_json': parse_json })


def allocate(request):
    # c1 = book(request.GET['bookid'])
    # print(c1.id)

    global bookid
    bookid = request.GET['bookid']
    return render(request, 'allocate1.html')



def add_new_member(request):
    if request.method == 'POST':
        global bookid
        name = request.POST['member_name']
        email = request.POST['member_email']
        cursor = connection.cursor()
        cursor.execute('select count(*) FROM members where email = %s', [email])
        len = cursor.fetchone()[0]
        print(len)
        if (len > 0):
            return render(request, 'error.html')
        cursor.execute('SELECT * FROM members WHERE email = %s', [email])
        # if len(cursor) > 0:
        #     pass
        cursor.execute('INSERT INTO members(nm, bookid, is_active, dt, email) VALUES(%s, %s, true, CURDATE(), %s)', [name, bookid, email ])
        return redirect('main:dashboard')
    return render(request, 'add_new_member.html')

email = '' 
name = ''

def existing_members(request):
    if request.method == 'POST':
        global email, name
        email = request.POST['email']
        cursor = connection.cursor()
        cursor.execute('select sum(DATEDIFF(CURDATE(), dt)) FROM members where email = %s;', [email])
        days = cursor.fetchone()[0]
        # name = cursor.execute('SELECT nm FROM members WHERE email = %s', [email])
        # print(name)
        query = "SELECT nm FROM members WHERE email = %s"
        cursor.execute(query, (email,))

        # # Fetch the result
        result = cursor.fetchone()
        name = result[0]
        cursor.close()
        connection.close()

        cursor = connection.cursor()
        cursor.execute('select count(*) FROM members where email = %s', [email])
        no_of_books  = cursor.fetchone()[0]
        debt = days * 10
        return render(request, 'allocate1.html', {
            'name': name,
            'no_of_books': no_of_books,
            'debt': debt,
            'email': email
        })
        
    return redirect('main:dashboard')


def return_book(request):
    if request.method == 'POST':
        email = request.POST['email']
        bookid = request.POST['bookid']
        cursor = connection.cursor()
        cursor.execute('DELETE FROM members WHERE email = %s AND bookid = %s', [email, bookid])
        return redirect('main:dashboard')
    return render(request, 'return.html')



def allocate2(request):
    global bookid, email, name
    cursor = connection.cursor()
    cursor.execute('INSERT INTO members(nm, bookid, is_active, dt, email) VALUES(%s, %s, true, CURDATE(), %s)', [name, bookid, email ])
    return redirect('main:dashboard')
