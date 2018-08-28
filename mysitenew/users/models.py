# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout 
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser 
import smtplib


#RICHER登入前function-------------------------------------------------------------------------------------------
# 取得我的使用者的ID
def GetUserID(request):
    userID = None
    if request.user.is_authenticated():
        userID = request.user.userID
    return userID

#拿取獨一無二的使用者Session地址
def GetUserKey(userID):
    return Session.objects.all()[userID]

def LoginValidate(request,username,password):  
    rtvalue = False  
    user = authenticate(username=username,password=password)  
    if user is not None:  
        if user.is_active:  
            auth_login(request,user)  
            return True  
    return rtvalue  

class User(AbstractUser): 
    Cexmoney = models.FloatField(default=0.0)
    Bittrexmoney = models.FloatField(default=0.0)
    Binancemoney = models.FloatField(default=0.0)
    CexBTC = models.FloatField(default=0.0)
    BittrexBTC = models.FloatField(default=0.0)
    BinanceBTC = models.FloatField(default=0.0)
    userID = models.IntegerField(primary_key=True)
    class Meta(AbstractUser.Meta): 
        pass
    def __str__(self):
		return self.userID


#RICHER登入前function-------------------------------------------------------------------------------------------

#RICHER登入後function-------------------------------------------------------------------------------------------
# 判斷我的帳號使否有登入成功
def FilterUser(userID):
    return User.objects.filter(userID=userID)[0]

# 判斷註冊時使用者有無重複 
def IsUserPassword(username):
    if(User.objects.all().filter(username=username)):
        return True
    return False

# 判斷註冊時email有無重複
def IsUserEmail(email):
    if(User.objects.all().filter(email=email)):
        return True
    return False

# 創建form 存入資料庫
def CreateFrom(username, email, password):
    user = User.objects.create_user(username, email, password) # 創建from
    user.save()

# 重新設定使用者密碼 重新存入資料庫
def CreateNewFrom(request,newPassword):
    newUser = User.objects.get(username__exact=request.user.username)
    newUser.set_password(newPassword) # 重新設定使用者密碼
    newUser.save()

# 判斷錢包-拿錢是否有小於0
def IsWalletSubtakeMoney(money, takemoney):
    if (money - takemoney) < 0:
        return True
    return False 

# Cexwalletfunction-----------------------------------------
def CexDepositWalletMoney(userID,amount):#storedmoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.Cexmoney = user.Cexmoney + amount
    user.save()
    return user.Cexmoney

def CexWithdrawWalletMoney(userID,amount):#takemoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.Cexmoney = user.Cexmoney - amount
    user.save()
    return user.Cexmoney
# Cexwalletfunction-----------------------------------------

# Bittrexwalletfunction-----------------------------------------
def BittrexDepositWalletMoney(userID,amount):#storedmoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.Bittrexmoney = user.Bittrexmoney + amount
    user.save()
    return user.Bittrexmoney

def BittrexWithdrawWalletMoney(userID,amount):#takemoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.Bittrexmoney = user.Bittrexmoney - amount
    user.save()
    return user.Bittrexmoney
# Bittrexwalletfunction-----------------------------------------

# Binancewalletfunction-----------------------------------------
def BinanceDepositWalletMoney(userID,amount):#storedmoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.Binancemoney = user.Binancemoney + amount
    user.save()
    return user.Binancemoney

def BinanceWithdrawWalletMoney(userID,amount):#takemoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.Binancemoney = user.Binancemoney - amount
    user.save()
    return user.Binancemoney
# Binancewalletfunction-----------------------------------------
#RICHER登入後function-------------------------------------------------------------------------------------------
 

import string
import random
def password_creater(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# forgotpassword-----------------------------------------
def CheckUserEmail(email):
    if User.objects.filter(email=email)[0] :
        return True
    else:
        return False

def ResetUserPassword(email):
    resetPassword = password_creater()
    newUser = User.objects.get(email=email)
    newUser.set_password(resetPassword) 
    # 重新設定使用者密碼
    newUser.save()
    
    host = "smtp.gmail.com"
    port = 25
    username = "frankboygx@gmail.com"
    password = "qdudfhxlvfjrdmwd"
    from_email = username
    to_list = [email]
    print "test1"
    email_conn = smtplib.SMTP(host,port)
    print "test2"
    # 試試看能否跟Gmail Server溝通
    print(email_conn.ehlo())
    # TTLS安全認證機制
    email_conn.starttls()
    print "test3"
    # 登錄Gmail
    print(email_conn.login(username,password))
    # 寄信
    email_conn.sendmail(from_email, to_list, resetPassword)
    # 關閉連線
    email_conn.quit()
    return  "success"

def EmailIdentifyingCode(email,IdentifyingCode):
    host = "smtp.gmail.com"
    port = 25
    username = "frankboygx@gmail.com"
    password = "qdudfhxlvfjrdmwd"
    from_email = username
    to_list = [email]
    print "test1"
    email_conn = smtplib.SMTP(host,port)
    print "test2"
    # 試試看能否跟Gmail Server溝通
    print(email_conn.ehlo())
    # TTLS安全認證機制
    email_conn.starttls()
    print "test3"
    # 登錄Gmail
    print(email_conn.login(username,password))
    # 寄信
    email_conn.sendmail(from_email, to_list, IdentifyingCode)
    # 關閉連線
    email_conn.quit()
    return  "success"

