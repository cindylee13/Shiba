from django.shortcuts import render_to_response, render
from users.form import RegisterForm, LoginForm, ChangepwdForm ,StoredMoneyForm , TakeMoneyForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import GetUserID, GetUserKey, LoginValidate, User, FilterUser, DepositWalletMoney, WithdrawWalletMoney
from django.contrib.auth.decorators import login_required


def Register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password2 = data['password2']
            if not User.objects.all().filter(username=username):
                if form.pwd_validate(password, password2):
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    LoginValidate(request, username, password)
                    return render(request,'welcome.html', {'user': username})
                else:
                    error.append('Please input the same password')
            else:
                error.append(
                    'The username has existed,please change your username')
    else:
        form = RegisterForm()
    return render(request,'register.html', {'form': form, 'error': error})


def Login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if LoginValidate(request, username, password):
                # GetUserKey(GetUserID(request))
                return render(request,'welcome.html', {'username': username})
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = LoginForm()
    return render(request,'login.html', {'error': error, 'form': form})


def Logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url='/users/error/')
def ChangePassword(request):
    if not request.user.is_authenticated():  # prevent anonymous Sign in
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    error = []
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=username,
                                password=data['oldPassword'])
            if user is not None:
                if data['newPassword'] == data['newPassword2']:
                    newUser = User.objects.get(username__exact=username)
                    newUser.set_password(data['newPassword'])
                    newUser.save()
                    return render(request,'welcome.html', {'user': username})

                else:
                    error.append('Please input the same password')
            else:
                error.append('Please correct the old password')
        else:
            error.append('Please input the required domain')
    else:
        form = ChangepwdForm()
    return render(request,'changepassword.html', {'form': form, 'error': error})


def Error(request):
    return render_to_response('error.html')

def MyProfile(request):
    user = FilterUser(GetUserID(request))
    return render(request, 'myProfile.html', {'username' : user.username,'mail' : user.email})

def MyWallet(request):
    user = FilterUser(GetUserID(request))
    return render(request, 'mywallet.html', {'username' : user.username,'money' : user.money})

def TakeWalletMoney(request):   
    error=[]
    if request.method == 'POST':  
        form = TakeMoneyForm(request.POST)  
        if form.is_valid():  
            data = form.cleaned_data 
            userID = GetUserID(request)
            takemoney = data['takemoney']
            user = FilterUser(userID)
            if (user.money-takemoney) < 0:
                error.append('Please input the same password')
            WithdrawWalletMoney(userID,takemoney)
            return HttpResponseRedirect('/users/myWallet')
        else:
            error.append('Please input the correct number')
    else :
        form = TakeMoneyForm() 
    return render(request,'takeWalletMoney.html',{'form':form,'error':error})

def StoredWalletMoney(request):   
    error = []
    if request.method == 'POST':  
        form = StoredMoneyForm(request.POST)  
        if form.is_valid():
            data = form.cleaned_data 
            userID = GetUserID(request)
            storedmoney = data['storedmoney']  
            user = FilterUser(userID)
            DepositWalletMoney(userID,storedmoney)
            return HttpResponseRedirect('/users/myWallet')
        else:
            error.append('Please input the correct number')
    else :
        form = StoredMoneyForm() 
    return render(request,'storedWalletMoney.html',{'form':form,'error':error})
