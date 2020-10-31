# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Django
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
#Custom
from tools.forms.domainForm import DomainForm
#Python
import re



# Create your views here.
class ToolFormView(FormView):
    STARTSWITH_PATTERN = ('https://', 'http://')
    template_name      = "console.html"
    form_class         = DomainForm
    success_url        = reverse_lazy('console_result')
    domain             = None

    def cleaner(self, value):
        """ in charge of cleaning the value passed """

        for pattern in self.STARTSWITH_PATTERN:
            try:
                if value.startswith(pattern):
                    value = value.replace(pattern, '')
            except Exception as Error:
                print("ToolFormView [cleaner] Error: %s" % Error)

        return value




    def form_valid(self, form):
        self.domain = self.cleaner(form.cleaned_data['domain'])
        return super(ToolFormView, self).form_valid(form)

    def get_success_url(self):
         return reverse('console_result', kwargs={'domain': self.domain})


