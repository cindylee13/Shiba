# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from users.form import SignUpForm, SignInForm, ChangepwdForm ,StoredMoneyForm , TakeMoneyForm, ForgotPasswordForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import GetUserID, GetUserKey, LoginValidate, User,EmailIdentifyingCode
from .models import FilterUser, CexDepositWalletMoney, CexWithdrawWalletMoney, BittrexDepositWalletMoney, BittrexWithdrawWalletMoney, BitfinexDepositWalletMoney, BitfinexWithdrawWalletMoney, CryptopiaDepositWalletMoney, CryptopiaWithdrawWalletMoney,CheckUserEmail ,ResetUserPassword, IsUserPassword, IsUserEmail, CreateFrom, CreateNewFrom, IsWalletSubtakeMoney
from trips.models import AlgTypeByUser, AlgTypeByUserData, TransectionRecord
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from bot.models import CreateLinePerson

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
                        CreateFrom(username, email, password)
                        LoginValidate(request, username, password)
                        IdentifyingCode = CreateLinePerson(GetUserID(request))
                        print IdentifyingCode
                        EmailIdentifyingCode(email,IdentifyingCode)
                        return render(request,'qrcode.html', {'username': username})
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
    return HttpResponseRedirect('/index/')

def News(request):
    return render(request, 'news.html')

def Qrcode(request):
    return render(request, 'qrcode.html')

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
                    return render(request,'trading.html', {'username': request.user.username,'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})

                else:
                    error.append('Please input the same password')
            else:
                error.append('Please correct the old password')
        else:
            error.append('Please input the required domain')
    else:
        form = ChangepwdForm()
    
    return render(request,'changepassword.html', {'form': form, 'error': error, 'username': request.user.username, 'email' : request.user.email,'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
#RICHER登入前-------------------------------------------------------------------------------------------

#RICHER登入後-------------------------------------------------------------------------------------------

def SelectPage(request, pageName):
    if not request.user.is_authenticated():  # prevent anonymous Sign in，尚未登入看不到頁面，要顯示錯誤
        return HttpResponseRedirect('/users/signin/')
    elif('Trading' == pageName):   
        return render(request,'trading.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('Order' == pageName):
        error = []
        isRepeat = 0
        if 'drop2' not in request.POST:
            return render_to_response('order.html')
        if 'drop3' not in request.POST:
            return render_to_response('order.html')
        a=request.POST['drop2']
        b=request.POST['drop3']
        unit = AlgTypeByUser.objects.filter(userID=GetUserID(request))
        for item in range(0, len(unit)):
            if(str(unit[item].Head)==str(a) and str(unit[item].Foot==str(b))):
                isRepeat = 1
                break

        if (str(a) == 'drop2-empty' or str(b) =='drop3-empty'):
            error.append('Please select an exchange')
        elif (str(a) == str(b)):
            error.append('Exchange repeat') 
        elif (isRepeat== 1): 
            error.append('Repeat Orders')
        else:
            AlgTypeByUser.objects.create(userID = GetUserID(request) ,Head = str(a) ,Foot = str(b))
            AlgTypeByUserData.objects.create(userID = GetUserID(request) ,Head = str(a) ,Foot = str(b))
        return render(request,'order.html',{'error': error, 'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('Withdraw' == pageName):
        return render(request,'withdraw.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('Deposit' == pageName):
        return render(request,'deposit.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('History' == pageName):   
        AlgTypeByUserTable = AlgTypeByUser.objects.all()
        AlgTypeByUserDataTable = AlgTypeByUserData.objects.all()
        return render(request,'history.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney, 'AlgTypeByUserTable' : AlgTypeByUserTable, 'AlgTypeByUserDataTable':AlgTypeByUserDataTable})
        
    else:
        return HttpResponseRedirect('/users/signin/') # 防呆

def Trading(request):
    return SelectPage(request, 'Trading')

def DeleteOrder(request, id):
    unit = AlgTypeByUser.objects.filter(userID=GetUserID(request))
    unit[int(id)].delete()
    AlgTypeByUserTable = AlgTypeByUser.objects.all()
    AlgTypeByUserDataTable = AlgTypeByUserData.objects.all()
    return render(request,'history.html', {'username': request.user.username, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney, 'AlgTypeByUserTable' : AlgTypeByUserTable, 'AlgTypeByUserDataTable':AlgTypeByUserDataTable})

def Order(request):
    return SelectPage(request, 'Order')

def Withdraw(request):
    return SelectPage(request, 'Withdraw')

def Deposit(request):
    return SelectPage(request, 'Deposit')
    
def History(request):
    return SelectPage(request, 'History')

#Withdraw------------------------------------------------------------------------------
def SelectWithdrawWalletSubtakeMoney(request, withdrawName, isTrueFalse, user):
    if isTrueFalse == False:
        if('CexWithdraw' == withdrawName):
            return 'You wallet have '+ str(user.Cexmoney) +' USD'
        elif('BittrexWithdraw' == withdrawName):
            return 'You wallet have '+ str(user.Bittrexmoney) +' USD'
        elif('BitfinexWithdraw' == withdrawName):
            return 'You wallet have '+ str(user.Bitfinexmoney) +' USD'
        elif('CryptopiaWithdraw' == withdrawName):
            return 'You wallet have '+ str(user.Cryptopiamoney) +' USD'
    if isTrueFalse == True:
        if('CexWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/CexWallet/')
        elif('BittrexWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/BittrexWallet/')
        elif('BitfinexWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/BitfinexWallet/')
        elif('CryptopiaWithdraw' == withdrawName):
            return HttpResponseRedirect('/users/CryptopiaWallet/')
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
    elif('BitfinexWithdraw' == withdrawName):
        if IsWalletSubtakeMoney(user.Bitfinexmoney, takemoney): 
            return False
        else:
            BitfinexWithdrawWalletMoney(userID,takemoney)
            return True
    elif('CryptopiaWithdraw' == withdrawName):
        if IsWalletSubtakeMoney(user.Cryptopiamoney, takemoney): 
            return False
        else:
            CryptopiaWithdrawWalletMoney(userID,takemoney)
            return True

def selectWithdrawHtml(request, withdrawName, form, error):
    if('CexWithdraw' == withdrawName):
        return render(request,'CexWithdraw.html', {'form':form,'error':error})
    elif('BittrexWithdraw' == withdrawName):
        return render(request,'BittrexWithdraw.html', {'form':form,'error':error})
    elif('BitfinexWithdraw' == withdrawName):
        return render(request,'BitfinexWithdraw.html', {'form':form,'error':error})
    elif('CryptopiaWithdraw' == withdrawName):
        return render(request,'BitfinexWithdraw.html', {'form':form,'error':error})
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

def BitfinexWithdraw(request):
    return selectWithdraw(request, 'BitfinexWithdraw')

def CryptopiaWithdraw(request):
    return selectWithdraw(request, 'CryptopiaWithdraw')

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
    elif('BitfinexDeposit' == DepositName):
        BitfinexDepositWalletMoney(userID,storedmoney)
        return HttpResponseRedirect('/users/BitfinexWallet/')
    elif('CryptopiaDeposit' == DepositName):
        CryptopiaDepositWalletMoney(userID,storedmoney)
        return HttpResponseRedirect('/users/CryptopiaWallet/')

def selectDepositHtml(request, DepositName, form, error):
    if('CexDeposit' == DepositName):
        return render(request,'CexDeposit.html', {'form':form,'error':error})
    elif('BittrexDeposit' == DepositName):
        return render(request,'BittrexDeposit.html', {'form':form,'error':error})
    elif('BitfinexDeposit' == DepositName):
        return render(request,'BitfinexDeposit.html', {'form':form,'error':error})
    elif('CryptopiaDeposit' == DepositName):
        return render(request,'CryptopiaDeposit.html', {'form':form,'error':error})
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

def BitfinexDeposit(request):
    return selectDeposit(request, 'BitfinexDeposit')

def CryptopiaDeposit(request):
    return selectDeposit(request, 'CryptopiaDeposit')

#Deposit------------------------------------------------------------------------------

#Wallet------------------------------------------------------------------------------
def SelectWallet(request, walletName):
    user = FilterUser(GetUserID(request))
    if('CexWallet' == walletName):
        return render(request, 'Cex_Wallet.html', {'username' : user.username,'money' : user.Cexmoney, 'BTC' : user.CexBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('BittrexWallet' == walletName):
        return render(request, 'Bittrex_Wallet.html', {'username' : user.username,'money' : user.Bittrexmoney, 'BTC' : user.BittrexBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('BitfinexWallet' == walletName):
        return render(request, 'Bitfinex_Wallet.html', {'username' : user.username,'money' : user.Bitfinexmoney, 'BTC' : user.BitfinexBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
    elif('CryptopiaWallet' == walletName):
        return render(request, 'Cryptopia_Wallet.html', {'username' : user.username,'money' : user.Cryptopiamoney, 'BTC' : user.CryptopiaBTC, 'CexMoney' : request.user.Cexmoney, 'BittrexMoney' : request.user.Bittrexmoney, 'BitfinexMoney' : request.user.Bitfinexmoney, 'CryptopiaMoney' : request.user.Cryptopiamoney, 'Total' :request.user.Cexmoney + request.user.Bittrexmoney + request.user.Bitfinexmoney + request.user.Cryptopiamoney})
def CexWallet(request):
    return SelectWallet(request, 'CexWallet')

def BittrexWallet(request):
    return SelectWallet(request, 'BittrexWallet')

def BitfinexWallet(request):
    return SelectWallet(request, 'BitfinexWallet')

def CryptopiaWallet(request):
    return SelectWallet(request, 'CryptopiaWallet')
#Wallet------------------------------------------------------------------------------

def Error(request):
    return render_to_response('error.html')

#RICHER登入後-------------------------------------------------------------------------------------------
        
