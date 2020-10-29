#Django
from django.conf.urls import url
from django.contrib import admin
#Custom
from .views.tools_FormView import ToolFormView
from .views.result_TemplateView import ResultTemplateView

urlpatterns = [
    url(r'console/', ToolFormView.as_view(), name="console" ),
    url(r'result/(?P<domain>[-\w.]+)/', ResultTemplateView.as_view(), name="console_result" )
]
