# -*- coding: utf-8 -*-
from django import forms  
class SignUpForm(forms.Form):  
    username = forms.CharField(max_length=15,label='username', 
                widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'})) 
                
    email= forms.CharField(max_length=100,
                widget= forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter your Password"}))
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput(attrs={'placeholder': "Enter your Password"}))
    # 判斷我密碼跟我確認密碼有沒有相同 
    def pwd_validate(self,p1,p2):  
        return p1==p2  

class SignInForm(forms.Form):  
    username = forms.CharField(max_length=15,label='username', 
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

class ForgotPasswordForm(forms.Form):  
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'})) 