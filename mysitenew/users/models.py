# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout 
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser): 
    money = models.FloatField(default=0.0)
    userID = models.IntegerField(primary_key=True)
    class Meta(AbstractUser.Meta): 
        pass
    def __str__(self):
		return self.userID
 
# GET----------------------------------------------
# 取得我的使用者的ID
def GetUserID(request):
    userID = None
    if request.user.is_authenticated():
        userID = request.user.userID
    return userID

#拿取獨一無二的使用者Session地址
def GetUserKey(userID):
    return Session.objects.all()[userID]
# GET----------------------------------------------

# function-----------------------------------------
# 判斷我的帳號使否有登入成功
def LoginValidate(request,username,password):  
    rtvalue = False  
    user = authenticate(username=username,password=password)  
    if user is not None:  
        if user.is_active:  
            auth_login(request,user)  
            return True  
    return rtvalue  
# function-----------------------------------------

# walletfunction-----------------------------------------
def FilterUser(userID):
    return User.objects.filter(userID=userID)[0]

def DepositWalletMoney(userID,amount):#storedmoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.money = user.money + amount
    user.save()
    return user.money

def WithdrawWalletMoney(userID,amount):#takemoney
    user = User.objects.select_for_update().filter(userID=userID)[0]
    user.money = user.money - amount
    user.save()
    return user.money
# walletfunction-----------------------------------------
