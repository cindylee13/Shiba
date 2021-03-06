from django.conf.urls import include, url  
from django.contrib import admin  
from .views import Index
from users.views import Trading, ForgotPassword, SignUp, SignIn, SignOut, News, Qrcode, ChangePassword , Error , Order, DeleteOrder,  Withdraw, Deposit, History
from users.views import CexWithdraw, BittrexWithdraw, BitfinexWithdraw, CryptopiaWithdraw, CexDeposit, BittrexDeposit, BitfinexDeposit, CryptopiaDeposit, CexWallet, BittrexWallet, BitfinexWallet, CryptopiaWallet
from trips.views import BTC,Trading
#from users.views import ForgotPassword, SignUp, SignIn, SignOut, ChangePassword , Error , MyProfile, MyWallet, StoredWalletMoney, TakeWalletMoney
admin.autodiscover()  
  
urlpatterns = [  
    url(r'^admin/', include(admin.site.urls)),  
    url(r'^BTC/$', BTC),
    url(r'^index/', Index),
    url(r'^users/news/',News),
    url(r'^users/qrcode/',Qrcode),
    url(r'^users/signin/',SignIn), 
    url(r'^users/forgot/',ForgotPassword), 
    url(r'^users/signup/', SignUp),  
    url(r'^users/signout/', SignOut),  
    url(r'^users/changepassword/',ChangePassword), 
    url(r'^users/error/', Error), 
    url(r'^users/trading/', Trading), 
    url(r'^users/order/', Order), 
    url(r'^users/deleteOrder/(?P<id>\d+)', DeleteOrder, name='DeleteOrder'),
    
    url(r'^users/withdraw/CexWithdraw/', CexWithdraw),  
    url(r'^users/withdraw/BittrexWithdraw/', BittrexWithdraw), 
    url(r'^users/withdraw/BitfinexWithdraw/', BitfinexWithdraw),  
    url(r'^users/withdraw/CryptopiaWithdraw/', CryptopiaWithdraw), 

    url(r'^users/deposit/CexDeposit/', CexDeposit),  
    url(r'^users/deposit/BittrexDeposit/', BittrexDeposit),  
    url(r'^users/deposit/BitfinexDeposit/', BitfinexDeposit),
    url(r'^users/deposit/CryptopiaDeposit/', CryptopiaDeposit), 

    url(r'^users/withdraw/', Withdraw), 
    url(r'^users/deposit/', Deposit), 
    
    url(r'^users/CexWallet/', CexWallet), 
    url(r'^users/BittrexWallet/', BittrexWallet),
    url(r'^users/BitfinexWallet/', BitfinexWallet),
    url(r'^users/CryptopiaWallet/', CryptopiaWallet),
    
    
    url(r'^users/history/', History), 
    url(r'^bot/',include('bot.urls')),

]