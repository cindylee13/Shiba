# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from users.form import SignUpForm, SignInForm, ChangepwdForm ,StoredMoneyForm , TakeMoneyForm, ForgotPasswordForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import GetUserID, GetUserKey, LoginValidate, User, FilterUser, DepositWalletMoney, WithdrawWalletMoney
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def SignUp(request):
    error = [] # 創建可以顯示error的陣列
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']   # 把web的資料丟到username
            email = data['email']
            password2 = data['password2']
            password = data['password']
             # 判斷註冊時使用者有無重複 內建判斷密碼跟確認密碼有沒有相同
            if not User.objects.all().filter(username=username):
                if form.pwd_validate(password, password2):
                    try:
                        user = User.objects.create_user(username, email, password) # 創建from
                        user.save() # 存入資料庫
                    except IntegrityError as e:
                        # print e.message
                        if 'UNIQUE constraint failed' in e.message:
                            LoginValidate(request, username, password) # 確認帳號密碼
                            return render(request,'welcome.html', {'user': username})
                    else:
                        LoginValidate(request, username, password)
                        return render(request,'welcome.html', {'user': username})
                else:
                    error.append('Please input the same password')
            else:
                error.append(
                    'The username has existed,please change your username')
    else:
        form = SignUpForm()
    return render(request,'signup.html', {'form': form, 'error': error})


def SignIn(request):
    error = []
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password'] # 確認密碼有沒有對
            if LoginValidate(request, username, password):
                # print GetUserKey(GetUserID(request))
                return render(request,'trading.html', {'username': username})
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = SignInForm()
    return render(request,'signin.html', {'error': error, 'form': form})


def SignOut(request):
    auth_logout(request)
    return HttpResponseRedirect('/users/signin/')

def ForgotPassword(request):
    error = []
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            if LoginValidate(request, email):
                return render(request,'index.html', {'username': username})
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = ForgotPasswordForm()
    return render(request,'forgot.html', {'error': error, 'form': form}) 

@login_required(login_url='/users/error/') # 如果在使用者已登出 直接改網頁位置是沒有辦法進入的就會直接跳轉到這裡
def ChangePassword(request):
    if not request.user.is_authenticated():  # prevent anonymous Sign in
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) # 判斷使用者有沒有登出過
        # return HttpResponseRedirect('/users/signin/')
    error = []
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=request.user.username,
                                password=data['oldPassword']) # 內建判斷舊使用者和使用者密碼
            if user is not None:
                if data['newPassword'] == data['newPassword2']:
                    newUser = User.objects.get(username__exact=request.user.username)
                    newUser.set_password(data['newPassword']) # 重新設定使用者密碼
                    newUser.save()
                    return render(request,'welcome.html', {'user': request.user.username})

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
            takemoney = data['takemoney'] #  將外面的資料丟到takemoney
            user = FilterUser(userID)
            #  判斷我的錢包和我拿的錢有無小於零
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

def Trading(request):   #尚未登入看不到葉面  要顯示錯誤
    if not request.user.is_authenticated():  # prevent anonymous Sign in
        # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
        return HttpResponseRedirect('/users/signin/')
    return render(request,'trading.html')

def Order(request):   #尚未登入看不到葉面  要顯示錯誤
    if not request.user.is_authenticated():  # prevent anonymous Sign in
        # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
        return HttpResponseRedirect('/users/signin/')
    return render(request,'order.html')

def Withdraw(request):   #尚未登入看不到葉面  要顯示錯誤
    if not request.user.is_authenticated():  # prevent anonymous Sign in
    # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
        return HttpResponseRedirect('/users/signin/')
    return render(request,'withdraw.html')

def Deposit(request):   #尚未登入看不到葉面  要顯示錯誤
    if not request.user.is_authenticated():  # prevent anonymous Sign in
    # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
        return HttpResponseRedirect('/users/signin/')
    return render(request,'deposit.html')
    


        
