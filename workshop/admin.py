from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Source)
admin.site.register(Client)
admin.site.register(Hardware)
admin.site.register(Entry)
admin.site.register(Service)
admin.site.register(Piece)
admin.site.register(OtherPiece)
admin.site.register(Fix)
admin.site.register(RoadEntry)
admin.site.register(RoadService)
admin.site.register(Log)
admin.site.register(PieceRequest)
admin.site.register(OtherPieceRequest)