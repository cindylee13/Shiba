# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import AlgTypeByUser,TransectionRecord,BittrexBTCTable, CexBTCTable, BinanceBTCTable, BitfinexBTCTable, CryptopiaBTCTable
from bot.models import LineBot

admin.site.register(BittrexBTCTable)      #-----1
admin.site.register(CexBTCTable)          #-----2
admin.site.register(BinanceBTCTable)      #-----3
admin.site.register(BitfinexBTCTable)     #-----4
admin.site.register(CryptopiaBTCTable)    #-----5
admin.site.register(AlgTypeByUser)     #-----6
admin.site.register(TransectionRecord)    #-----7