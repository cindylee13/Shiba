# -*- coding: utf-8 -*-
from django import forms  
class RegisterForm(forms.Form):  
    username = forms.CharField()  
    email = forms.EmailField()  
    password = forms.CharField(widget=forms.PasswordInput)  
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)  
    # 判斷我密碼跟我確認密碼有沒有相同 
    def pwd_validate(self,p1,p2):  
        return p1==p2  

class LoginForm(forms.Form):  
    username = forms.CharField(label='username', 
                widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))

class ChangepwdForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput)  
    newPassword = forms.CharField(widget=forms.PasswordInput)  
    newPassword2= forms.CharField(label='Confirm',widget=forms.PasswordInput)  
    def pwd_validate(self,p1,p2):  
        return p1==p2  

class TakeMoneyForm(forms.Form):  
    takemoney = forms.FloatField()  

class StoredMoneyForm(forms.Form):
    storedmoney = forms.FloatField()