# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#django
from django.shortcuts import render
from django.views.generic import TemplateView

#Custom
from tools.utils.discoverer import DomainDiscover




# Create your views here.
class ResultTemplateView(TemplateView):
    template_name = "console_result.html"
    domainDiscover = DomainDiscover()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['domainInfo'] = domain_data = self.domainDiscover.discover(context['domain'])
        return self.render_to_response(context)