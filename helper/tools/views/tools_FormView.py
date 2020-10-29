# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Django
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
#Custom
from tools.forms.domainForm import DomainForm



# Create your views here.
class ToolFormView(FormView):
    template_name = "console.html"
    form_class    = DomainForm
    success_url   = reverse_lazy('console_result')
    domain        = None

    def form_valid(self, form):
        self.domain = form.cleaned_data['domain']
        return super(ToolFormView, self).form_valid(form)

    def get_success_url(self):
         return reverse('console_result', kwargs={'domain': self.domain})


