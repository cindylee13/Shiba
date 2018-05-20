from django.conf.urls import include, url  
from django.contrib import admin  
from .views import Index
from users.views import ForgotPassword, SignUp, SignIn, SignOut, ChangePassword , Error , MyProfile, MyWallet, StoredWalletMoney, TakeWalletMoney
admin.autodiscover()  
  
urlpatterns = [  
    url(r'^admin/', include(admin.site.urls)),  

    url(r'^index/', Index),
    url(r'^users/signin/',SignIn), 
    url(r'^users/forgot/',ForgotPassword), 
    url(r'^users/signup/', SignUp),  
    url(r'^users/signout/', SignOut), 
    # url(r'^users/changepassword/(?P<username>\w+)/$',ChangePassword),
    url(r'^users/changepassword/',ChangePassword),
    url(r'^users/myProfile/',MyProfile),  
    url(r'^users/myWallet/',MyWallet),  
    url(r'^users/myWallet/storedWalletMoney/',StoredWalletMoney),  
    url(r'^users/myWallet/takeWalletMoney/',TakeWalletMoney),  
    url(r'^users/error/', Error), 
]