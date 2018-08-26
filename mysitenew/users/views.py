# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from users.form import SignUpForm, SignInForm, ChangepwdForm ,StoredMoneyForm , TakeMoneyForm, ForgotPasswordForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import GetUserID, GetUserKey, LoginValidate, User
from .models import FilterUser, CexDepositWalletMoney, CexWithdrawWalletMoney, BittrexDepositWalletMoney, BittrexWithdrawWalletMoney, BinanceDepositWalletMoney, BinanceWithdrawWalletMoney,CheckUserEmail ,ResetUserPassword, IsUserPassword, IsUserEmail, CreateFrom, CreateNewFrom, IsWalletSubtakeMoney
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

#RICHER登入前-------------------------------------------------------------------------------------------
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
             # 判斷註冊時使用者和email有無重複 內建判斷密碼跟確認密碼有沒有相同
            if not (IsUserPassword(username)):
                if not (IsUserEmail(email)):
                    if form.pwd_validate(password, password2):
                        try:
                            CreateFrom(username, email, password)
                        except IntegrityError as e:
                            # print e.message
                            if 'UNIQUE constraint failed' in e.message:
                                LoginValidate(request, username, password) # 確認帳號密碼
                                return render(request,'trading.html', {'username': username})
                        else:
                            LoginValidate(request, username, password)
                            return render(request,'trading.html', {'username': username})
                    else:
                        error.append('Please input the same password')
                else:
                     error.append(
                        'The email has existed,please change your username')
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
                # return render_to_response('trading.html',{'username': request.user.username})
                return HttpResponseRedirect('/users/trading/') 
                #return render(request,'trading.html', {'username': request.user.username})
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = SignInForm()
    return render(request,'signin.html', {'error': error, 'form': form})


def SignOut(request):
    auth_logout(request)
    return HttpResponseRedirect('/index')

def ForgotPassword(request):
    error = []
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            if CheckUserEmail(email):
                ResetUserPassword(email)
                return HttpResponseRedirect('/users/signin/')
            else:
                error.append('Please input the correct email')
        else:
            error.append('Please input email')
    else:
        form = ForgotPasswordForm()
    return render(request,'forgot.html', {'error': error, 'form': form}) 

@login_required(login_url='/users/error/') # 如果在使用者已登出 直接改網頁位置是沒有辦法進入的就會直接跳轉到這裡
def ChangePassword(request):
    if not request.user.is_authenticated():  # prevent anonymous Sign in
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) # 判斷使用者有沒有登出過
    error = []
    if request.method== 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=request.user.username,
                                password=data['oldPassword']) # 內建判斷舊使用者和使用者密碼
            if user is not None:
                if data['newPassword'] == data['newPassword2']:
                    newPassword = data['newPassword']
                    CreateNewFrom(request, newPassword)
                    return render(request,'trading.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})

                else:
                    error.append('Please input the same password')
            else:
                error.append('Please correct the old password')
        else:
            error.append('Please input the required domain')
    else:
        form = ChangepwdForm()
    return render(request,'changepassword.html', {'form': form, 'error': error, 'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
#RICHER登入前-------------------------------------------------------------------------------------------

#RICHER登入後-------------------------------------------------------------------------------------------

def SelectPage(request, pageName):
    if not request.user.is_authenticated():  # prevent anonymous Sign in，尚未登入看不到頁面，要顯示錯誤
        return HttpResponseRedirect('/users/signin/')
    elif('Trading' == pageName):   
        return render(request,'trading.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
    elif('Order' == pageName):
        return render(request,'order.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
    elif('Withdraw' == pageName):
        return render(request,'withdraw.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
    elif('Deposit' == pageName):
        return render(request,'deposit.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
    else:
        return HttpResponseRedirect('/users/signin/') # 防呆

def Trading(request):
    return SelectPage(request, 'Trading')

def Order(request):
    return SelectPage(request, 'Order')

def Withdraw(request):
    return SelectPage(request, 'Withdraw')

def Deposit(request):
    return SelectPage(request, 'Deposit')

#Withdraw------------------------------------------------------------------------------
def SelectWithdrawWalletSubtakeMoney(request, withdrawName, isTrueFalse, user):
    if isTrueFalse == False:
        return 'You wallet have '+ str(user.Cexmoney) +' USD'
    if isTrueFalse == True:
        if('CexWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/CexWallet/')
        elif('BittrexWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/BittrexWallet/')
        elif('BinanceWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/BinanceWallet/')
def IsSelectWithdrawWalletSubtakeMoney(request, withdrawName, user, userID, takemoney):
    if('CexWithdraw' == withdrawName):
        if IsWalletSubtakeMoney(user.Cexmoney, takemoney): 
            return False
        else:
            CexWithdrawWalletMoney(userID,takemoney)
            return True
    elif('BittrexWithdraw' == withdrawName):
        if IsWalletSubtakeMoney(user.Bittrexmoney, takemoney): 
            return False
        else:
            BittrexWithdrawWalletMoney(userID,takemoney)
            return True
    elif('BinanceWithdraw' == withdrawName):
        if IsWalletSubtakeMoney(user.Binancemoney, takemoney): 
            return False
        else:
            BinanceWithdrawWalletMoney(userID,takemoney)
            return True

def selectWithdrawHtml(request, withdrawName, form, error):
    if('CexWithdraw' == withdrawName):
        return render(request,'CexWithdraw.html', {'form':form,'error':error})
    elif('BittrexWithdraw' == withdrawName):
        return render(request,'BittrexWithdraw.html', {'form':form,'error':error})
    elif('BinanceWithdraw' == withdrawName):
        return render(request,'BinanceWithdraw.html', {'form':form,'error':error})
    else:
        return HttpResponseRedirect('/users/signin/') # 防呆

def selectWithdraw(request, withdrawName):
    if not request.user.is_authenticated():  # prevent anonymous Sign in，尚未登入看不到頁面，要顯示錯誤
        return HttpResponseRedirect('/users/signin/')
    error=[]
    if request.method == 'POST':  
        form = TakeMoneyForm(request.POST)  
        if form.is_valid():  
            data = form.cleaned_data 
            userID = GetUserID(request)
            takemoney = data['takemoney'] #  將外面的資料丟到takemoney
            takemoney2 = data['takemoney2']
            if takemoney == takemoney2:
                user = FilterUser(userID)
                if IsSelectWithdrawWalletSubtakeMoney(request, withdrawName, user, userID, takemoney)==True:
                    return SelectWithdrawWalletSubtakeMoney(request, withdrawName, True, user)
                elif IsSelectWithdrawWalletSubtakeMoney(request, withdrawName, user, userID, takemoney)==False:
                    error.append(str(SelectWithdrawWalletSubtakeMoney(request, withdrawName, False, user)))
            else:
                error.append('Please input the same number')
        else:
            error.append('Please input the correct number')
    else :
        form = TakeMoneyForm()
    return selectWithdrawHtml(request, withdrawName, form, error)

def CexWithdraw(request):
    return selectWithdraw(request, 'CexWithdraw')
    
def BittrexWithdraw(request):
    return selectWithdraw(request, 'BittrexWithdraw')

def BinanceWithdraw(request):
    return selectWithdraw(request, 'BinanceWithdraw')

#Withdraw-----------------------------------------------------------------------------

#Deposit------------------------------------------------------------------------------
def selectDepositStore(request, DepositName, userID, storedmoney):
    user = FilterUser(userID)
    if('CexDeposit' == DepositName):
        CexDepositWalletMoney(userID,storedmoney)
        return HttpResponseRedirect('/users/CexWallet/')
    elif('BittrexDeposit' == DepositName):
        BittrexDepositWalletMoney(userID,storedmoney)
        return HttpResponseRedirect('/users/BittrexWallet/')
    elif('BinanceDeposit' == DepositName):
        BinanceDepositWalletMoney(userID,storedmoney)
        return HttpResponseRedirect('/users/BinanceWallet/')

def selectDepositHtml(request, DepositName, form, error):
    if('CexDeposit' == DepositName):
        return render(request,'CexDeposit.html', {'form':form,'error':error})
    elif('BittrexDeposit' == DepositName):
        return render(request,'BittrexDeposit.html', {'form':form,'error':error})
    elif('BinanceDeposit' == DepositName):
        return render(request,'BinanceDeposit.html', {'form':form,'error':error})
    else:
        return HttpResponseRedirect('/users/signin/') # 防呆

def selectDeposit(request, DepositName):
    if not request.user.is_authenticated():  # prevent anonymous Sign in，尚未登入看不到頁面，要顯示錯誤
        return HttpResponseRedirect('/users/signin/')
    error = []
    if request.method == 'POST':  
        form = StoredMoneyForm(request.POST)  
        if form.is_valid():
            data = form.cleaned_data 
            userID = GetUserID(request)
            storedmoney = data['storedmoney']  
            storedmoney2 = data['storedmoney2']  
            if storedmoney == storedmoney2 :
                return selectDepositStore(request, DepositName, userID, storedmoney)
            else:
                error.append('Please input the same number')  
        else:
            error.append('Please input the correct number')
    else :
        form = StoredMoneyForm() 
    return selectDepositHtml(request, DepositName, form, error)

def CexDeposit(request):
    return selectDeposit(request, 'CexDeposit')
    
def BittrexDeposit(request):
    return selectDeposit(request, 'BittrexDeposit')

def BinanceDeposit(request):
    return selectDeposit(request, 'BinanceDeposit')

#Deposit------------------------------------------------------------------------------

#Wallet------------------------------------------------------------------------------
def SelectWallet(request, walletName):
    user = FilterUser(GetUserID(request))
    if('CexWallet' == walletName):
        return render(request, 'Cex_Wallet.html', {'username' : user.username,'money' : user.Cexmoney, 'BTC' : user.CexBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
    elif('BittrexWallet' == walletName):
        return render(request, 'Bittrex_Wallet.html', {'username' : user.username,'money' : user.Bittrexmoney, 'BTC' : user.BittrexBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
    elif('BinanceWallet' == walletName):
        return render(request, 'Binance_Wallet.html', {'username' : user.username,'money' : user.Binancemoney, 'BTC' : user.BinanceBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BinanceMoney' : request.user.Binancemoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Binancemoney})
def CexWallet(request):
    return SelectWallet(request, 'CexWallet')

def BittrexWallet(request):
    return SelectWallet(request, 'BittrexWallet')

def BinanceWallet(request):
    return SelectWallet(request, 'BinanceWallet')
#Wallet------------------------------------------------------------------------------

def Error(request):
    return render_to_response('error.html')

#RICHER登入後-------------------------------------------------------------------------------------------
        
