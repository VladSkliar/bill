# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.core.urlresolvers import reverse_lazy
from models import BillRegion, Bill
from forms import BillCreationForm


class RegionListView(ListView):
    model = BillRegion
    template_name = 'index.html'
    context_object_name = 'regions'


class BillRegionListView(ListView):
    model = Bill
    template_name = 'billregion.html'
    context_object_name = 'bills'
    paginate_by = 2

    def get_queryset(self):
        qs = super(BillRegionListView, self).get_queryset()
        if 'pk' in self.kwargs.keys():
            region = get_object_or_404(BillRegion, pk=self.kwargs['pk'])
            qs = qs.filter(region=region)
        else:
            qs = qs.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(BillRegionListView, self).get_context_data(**kwargs)
        all_regions = BillRegion.objects.all()
        context['regions'] = all_regions
        if 'pk' in self.kwargs.keys():
            context['region_id'] = int(self.kwargs['pk'])
        return context


class BillDetailView(DetailView):
    model = Bill
    template_name = 'bill.html'
    context_object_name = 'bill'


class BillCreateView(CreateView):
    model = Bill
    template_name = 'bill_creation.html'
    form_class = BillCreationForm

    def form_valid(self, form):
        self.object = form.save()
        return super(BillCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,
                                                             message=u'Форма заполнена неверно'))

    def get_success_url(self):
        return reverse_lazy('bill_detail', kwargs={'pk': self.object.id})
