from django.conf.urls import include, url  
from django.contrib import admin  
from users.views import Register, Login, ChangePassword , Error , MyProfile, MyWallet, StoredWalletMoney, TakeWalletMoney
from django.contrib.auth.views import logout
admin.autodiscover()  
  
urlpatterns = [  
    url(r'^admin/', include(admin.site.urls)),  

    #url(r'^register/$',Register),  
    url(r'^users/login/$',Login), 
    url(r'^users/login/register/$',Register),  
    url(r'^users/logout/$', logout), 
    # url(r'^users/changepassword/(?P<username>\w+)/$',ChangePassword),
    url(r'^users/changepassword/$',ChangePassword),
    url(r'^users/myProfile/$',MyProfile),  
    url(r'^users/myWallet/$',MyWallet),  
    url(r'^users/myWallet/storedWalletMoney/$',StoredWalletMoney),  
    url(r'^users/myWallet/takeWalletMoney/$',TakeWalletMoney),  
    url(r'^users/error/$', Error), 
]