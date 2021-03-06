# -*- coding: utf-8 -*-
from django import forms  
class SignUpForm(forms.Form):  
    username = forms.CharField(max_length=15,label='username', 
                widget=forms.TextInput(attrs={'placeholder': 'Enter Your Username'})) 
                
    email= forms.CharField(max_length=100,
                widget= forms.EmailInput(attrs={'placeholder':'Enter Your Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Your Password"}))
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput(attrs={'placeholder': "Enter Your Password"}))
    # 判斷我密碼跟我確認密碼有沒有相同 
    def pwd_validate(self,p1,p2):  
        return p1==p2  

class SignInForm(forms.Form):  
    username = forms.CharField(max_length=15,label='username', 
                widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))

class ChangepwdForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Your Old Password"}))
    newPassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter Your New Password"}))
    newPassword2= forms.CharField(label='Confirm',widget=forms.PasswordInput(attrs={'placeholder': "Confirm Your New Password"}))  
    def pwd_validate(self,p1,p2):  
        return p1==p2  

class TakeMoneyForm(forms.Form):  
    takemoney = forms.FloatField()  
    takemoney2 = forms.FloatField()  

class StoredMoneyForm(forms.Form):
    storedmoney = forms.FloatField()
    storedmoney2 = forms.FloatField()

class ForgotPasswordForm(forms.Form):  
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'})) 