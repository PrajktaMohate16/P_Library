from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from book.models import Book
import traceback
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

# Create your views here.
# view willalways take request as an argument
def homepage(request):              # request -- HttpRequest ---contains meta data --default argument

    """Return home page of web application"""

########################################---------------Basic operations--------------####################################

    # Http - Hyper Text Transfer Protocol
    # function returns HttpResponse 

    # return HttpResponse("hii")

    # return HttpResponse("The Economic Times is an Indian English-language business-focused daily newspaper.")

    # x = 10+20+30+40
    # print(x)
    # return HttpResponse(x)

    # a = "[1,2,3,4,5]"
    # print(a)
    # return HttpResponse(a)

    # t = "(11,22,33,44)"
    # print(t)
    # return HttpResponse(t)

    # return HttpResponse("<h1>Hii Hello<br>How are you?</h1>")

########################################---------------Main operation--------------####################################

    # print(dir(request))
    # print(request.method)           # GET

    # print(request.build_absolute_uri())     # http://127.0.0.1:8000/home/

    # print(request.method)               # GET
    # print(request.GET)                  # <QueryDict: {}>

    # print(request.method)               # POST
    # print(request.POST)                 # <QueryDict: {'csrfmiddlewaretoken': ['S6YVwu9yU17d95mzKZBWNPOk3FyCfSgzTSw5Nu6pv7rwWcU1S6R27hwWdCRzipj8']}>
    
    # print(request.POST)                 # <QueryDict: {'csrfmiddlewaretoken': ['gWorMzU5kzFDHbgenXFiGBbA9Mj8Qb89hIWB3zRWVFZWuiOGv4Vo03TcjJC5TIbI'], 'bname': ['Book1'], 'bprice': ['250'], 'bqty': ['2']}>


    # optimizing code
    name = request.POST.get("bname")
    price = request.POST.get("bprice")
    qty = request.POST.get("bqty")

    # fetching data in backend

    if request.method == "POST":
        if not request.POST.get("bid"):
            book_name = name
            book_price = price
            book_qty = qty

            # fetching data in console
            # print(book_name,book_price,book_qty)        # Book1 250 2
            # print(type(book_name))                      # <class 'str'>

            # creating book objects
            b1 = Book.objects.create(name=book_name,price=book_price,quantity=book_qty)
            # print(b1)
            return redirect("homepage")
            

        else:
            try:
                bid = request.POST.get("bid")
            except Book.DoesNotExist as err_msg:
                print(err_msg)
            else:
                book_obj = Book.objects.get(id=bid)
                book_obj.name = name
                book_obj.price = price
                book_obj.quantity = qty
                book_obj.save()
            redirect("show_all_books")

    elif request.method == "GET":
        return render(request,template_name="home.html")


########################################---------------Show-all-books--------------###############################

def show_all_books(request):

    """Return all books"""

    all_books = Book.objects.all()
    data = {"books":all_books}
    return render(request,template_name="show_books.html",context=data)   # context


########################################---------------Edit data--------------####################################

def edit_data(request,id):

    """Edit data available in table"""
    if request.method == "POST":
        try:
            singal_data = Book.objects.get(id=id)
        except Book.DoesNotExist as err_msg:
            print(err_msg)
        else:
            return render(request,template_name="home.html",context={"singal_book":singal_data})
    
    else:
        return HttpResponse("Error...!")


########################################---------------Delete data--------------####################################

def delete_data(request,id):

    """delete data from table"""

    print(request.method)

    if request.method == "POST":
        try:
            singal_data = Book.objects.get(id=id)
        except Book.DoesNotExist as err_msg:
            traceback.print_exc()
            return HttpResponse(f"Book dose not exits for ID:-{id}")
        else:
            singal_data.delete()
            return redirect("show_all_books")

    else:
        return HttpResponse(f"Request method:{request.method} is not allowed ....! Only POST method is allowed ")


########################################---------------Delete all books from database--------------####################################

def delete_all_books(request):

    """delete all books"""

    print(request.method)
    if request.method == "POST":
        all_books = Book.objects.all()
        all_books.delete()
        data = {"books":all_books}
        return render(request,template_name="show_books.html",context=data)

    else:
        return HttpResponse("Error...!")

########################################---------------Soft Delete Books--------------####################################

def soft_delete(request,id):

    """deleting books from tables"""

    if request.method == "POST":
        try:
            singal_book = Book.objects.get(id=id)
        except Book.DoesNotExist as msg:
            print(msg)
        else:
            singal_book.is_active = "N"
            singal_book.save()
            print(singal_book)
            return redirect("show_all_books")

    else:
        return HttpResponse("Error...!")

########################################---------------Soft Delete all books--------------####################################

def soft_delete_all(request):

    """delete all books from table"""

    all_books = Book.objects.all()
    all_books.is_active = "N"
    all_books.save()
    return redirect("Show_soft_deleted_books.html")


########################################--------------- show Soft Delete all books--------------####################################

def show_soft_deleted_books(request):
    
    """ Show all soft deleted books"""

    books = Book.objects.filter(is_active="N")
    data = {"soft_deleted_books":books}
    return render(request,template_name="Show_soft_deleted_books.html",context=data)
    
########################################--------------- Restore Soft Delete all books--------------####################################

def restore_data(request,id):

    """Restore all soft deleted data"""

    try:
        singal_book = Book.objects.get(id=id)
    except Book.DoesNotExist as msg:
        print(msg)
    else:
        singal_book.is_active = "Y"
        singal_book.save()
        return redirect("show_all_books")

# --------------------------------------------------------------------------------------------------------------------------------

def product_video(request):
    print("In product video")
    return HttpResponse("Here you can see product video")
    
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username,password)
    if user:
        login(request,user)
        return HttpResponse("Successfully logged in .....!")
