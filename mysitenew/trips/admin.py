# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import BittrexBTCTable, CexBTCTable, BinanceBTCTable, BitfinexBTCTable, CryptopiaBTCTable

admin.site.register(BittrexBTCTable)      #-----1
admin.site.register(CexBTCTable)          #-----2
admin.site.register(BinanceBTCTable)      #-----3
admin.site.register(BitfinexBTCTable)     #-----4
admin.site.register(CryptopiaBTCTable)    #-----5