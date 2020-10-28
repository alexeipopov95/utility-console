#Django
from django.conf.urls import url
from django.contrib import admin
#Custom
from .views.tools_TemplateView import ToolTemplateView
from .views.result_TemplateView import ResultTemplateView

urlpatterns = [
    url(r'console/', ToolTemplateView.as_view(), name="console" ),
    url(r'result/', ResultTemplateView.as_view(), name="console" )
]
