from django.shortcuts import render, redirect
from django.contrib import messages
import json
from django.core.signing import Signer
from .models import SignupDoctor, SignupPatient, CreateBlog
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.
signer = Signer(salt='extra') # for encription of password

def home(request):
    return render(request, "index.html")

def doctorDashboard(request):
    if 'auth' in request.session and 'name' in request.session:
        patient = SignupPatient.objects.all()
        return render(request, "doctorDashboard.html", { 'patient' : patient, 'name' : request.session.get("name") } )

def patientDashboard(request):
    if 'auth' in request.session:
        doctor = SignupDoctor.objects.all()
        return render(request, "patientDashboard.html", {'doctor':doctor, 'name' : request.session.get("name") } )

def signupDoctor(request):
    if 'msg' in request.session:
        request.session.pop('msg',None)
    if request.method == 'POST':
        profilepic =  request.FILES["file"]
        username = request.POST["username"]
        fname = request.POST["f-name"]
        lname = request.POST["l-name"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        password1 = request.POST["Password"]
        pincode = str(request.POST["pincode"])
        address = request.POST.get("address")
        city = request.POST["city"]
        state = request.POST["state"]

        password = signer.sign_object({'password': f'{password1}'}) #encrypted password
        check_username = SignupDoctor.objects.filter(username=username).exists()

        if(check_username):
            request.session['signupMSG'] = "Username or Phone Number has already been registered!"
            messages.error(request, request.session.get('signupMSG'))
            return redirect('/signupDoctor')
        else:
            if 'signupMSG' in request.session:
                request.session.pop('signupMSG',None)
            signup = SignupDoctor.objects.create(profilePic=profilepic, firstName = fname, lastName=lname, username=username, email=email, gender=gender, password=password, pincode=pincode, address=address, city=city, state=state)
            signup.save()
            request.session['msg'] = "Account has been created successfully !"
            return redirect('/loginDoctor')

    return render(request, "signup doctor.html")

def signupPatient(request):
    if 'msg' in request.session:
        request.session.pop('msg',None)
    if request.method == 'POST':
        profilepic =  request.FILES.get("file")
        # profilepic.name = 'profile'
        # fss = FileSystemStorage()
        # print(profilepic)
        # fss.save(profilepic.name, profilepic) #save profile pic
        username = request.POST["username"]
        fname = request.POST["f-name"]
        lname = request.POST["l-name"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        password1 = request.POST["Password"]
        pincode = str(request.POST["pincode"])
        address = request.POST.get("address")
        city = request.POST["city"]
        state = request.POST["state"]

        password = signer.sign_object({'password': f'{password1}'}) #encrypted password
        check_username = SignupPatient.objects.filter(username=username).exists()

        if(check_username):
            request.session['signupMSG'] = "Username or Phone Number has already been registered!"
            messages.error(request, request.session.get('signupMSG'))
            return redirect('/signupPatient')
        else:
            if 'signupMSG' in request.session:
                request.session.pop('signupMSG',None)
            signup = SignupPatient.objects.create(profilePic=profilepic, firstName = fname, lastName=lname, username=username, email=email, gender=gender, password=password, pincode=pincode, address=address, city=city, state=state)
            signup.save()
            request.session['msg'] = "Account has been created successfully !"
            return redirect('/loginPatient')
    return render(request, "signup patient.html")

def loginDoctor(request):
    if 'signupMSG' in request.session:
        request.session.pop('signupMSG',None)
    if "msg" in request.session:
        pass
    else:
        request.session["msg"] = None

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        request.session['auth'] = False
        user = SignupDoctor.objects.filter(username=name).first()
        if user:
            jsonPassword = json.dumps(signer.unsign_object(user.password)) #dumps() converts python dictionary into json
            dictPassword = json.loads(jsonPassword) #loads() converts json into python dictionary
            if(password==dictPassword['password']):
                request.session['name'] = name
                request.session['auth'] = True
                if "msg" in request.session:
                    request.session.pop("msg",None)
                return redirect('/doctorDashboard')
            else:
                request.session["msg"] = "Wrong Password !"
                messages.error(request, request.session.get('msg'))
        else:
            request.session["msg"] = "This Username doesn't exist."
            messages.error(request, request.session.get('msg'))
    return render(request, "login doctor.html")

def loginPatient(request):
    if 'signupMSG' in request.session:
        request.session.pop('signupMSG',None)
    if "msg" in request.session:
        pass
    else:
        request.session["msg"] = None

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        request.session['auth'] = False
        user = SignupDoctor.objects.filter(username=name).first()
        if user:
            jsonPassword = json.dumps(signer.unsign_object(user.password)) #dumps() converts python dictionary into json
            dictPassword = json.loads(jsonPassword) #loads() converts json into python dictionary
            if(password==dictPassword['password']):
                request.session['name'] = name
                request.session['password'] = password
                request.session['auth'] = True
                if "msg" in request.session:
                    request.session.pop("msg",None)
                return redirect('/patientDashboard')
            else:
                request.session["msg"] = "Wrong Password !"
                messages.error(request, request.session.get('msg'))
        else:
            request.session["msg"] = "This Username doesn't exist."
            messages.error(request, request.session.get('msg'))
 
    return render(request, "login patient.html")


def logout(request):
    store = ['auth','name','signupMSG','msg']
    for i in store:
        if i in request.session:
            request.session.pop(i,None)
    return redirect('/')

def createBlogs(request):
    if request.method == 'POST':
        if 'auth' in request.session and 'name' in request.session:
            username = request.session.get("name")
            title = request.POST.get("title")
            image = request.FILES.get("file")
            categories = request.POST.get("categories")
            summary = request.POST.get("summary")
            content = request.POST.get("content")
            draft = request.POST.get("saveasDraft")
            create = CreateBlog.objects.create(username=username, Title=title, Image=image, Categories=categories, Summary=summary, Content=content, Draft=draft)
            create.save()
            return redirect("/myblog")
    return render(request, "createBlogs.html")

def draft(request):
    if 'auth' in request.session and 'name' in request.session:
        drafts = CreateBlog.objects.filter(username=request.session.get("name"))
        drafts = drafts.filter(Draft="on")
        return render(request, "draft.html", {'drafts':drafts})
    else:
        return redirect("/")

def myblog(request):
    if 'auth' in request.session and 'name' in request.session:
        mentalHealth = CreateBlog.objects.filter(username=request.session.get("name")).filter(Draft=None).filter(Categories="Mental Health")
        heartDisease = CreateBlog.objects.filter(username=request.session.get("name")).filter(Draft=None).filter(Categories="Heart Disease")
        covid19 = CreateBlog.objects.filter(username=request.session.get("name")).filter(Draft=None).filter(Categories="COVID-19")
        immunization = CreateBlog.objects.filter(username=request.session.get("name")).filter(Draft=None).filter(Categories="Immunization")
        return render(request, "myblog.html", {'mentalHealth':mentalHealth, 'heartDisease':heartDisease, 'covid19':covid19, 'immunization':immunization})

def bloglist(request):
            mentalHealth = CreateBlog.objects.filter(Draft=None).filter(Categories="Mental Health")
            heartDisease = CreateBlog.objects.filter(Draft=None).filter(Categories="Heart Disease")
            covid19 = CreateBlog.objects.filter(Draft=None).filter(Categories="COVID-19")
            immunization = CreateBlog.objects.filter(Draft=None).filter(Categories="Immunization")
            return render(request, "bloglist.html", {'mentalHealth':mentalHealth, 'heartDisease':heartDisease, 'covid19':covid19, 'immunization':immunization})

def viewBlogs(request):
    title = request.POST.get("titleInput")
    blog = CreateBlog.objects.filter(Title=title).first()
    return render(request, "blogs.html", {'blog':blog})