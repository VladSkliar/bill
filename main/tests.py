# -*- coding: utf-8 -*-
from django.test import TestCase
from models import BillRegion, Bill
from views import RegionListView, BillDetailView
from django.core.urlresolvers import reverse_lazy
from django.test import Client


class RegionModel(TestCase):
    def setUp(self):
        self.region = BillRegion.objects.create(title=u'Test')
        self.client = Client()

    def test_create(self):
        test_region = BillRegion.objects.last()
        self.assertEqual(self.region, test_region)

    def test_region_view(self):
        self.assertTrue(self.region in RegionListView().get_queryset())

    def test_region_get_request(self):
        response = self.client.get(reverse_lazy('region-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['regions']), 1)

    def test_bill_region_get_request(self):
        BillRegion.objects.create(title=u'Test2')
        response = self.client.get(reverse_lazy('region_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['regions']), 2)
        response = self.client.get(reverse_lazy('region_detail',
                                                kwargs={'pk': self.region.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['regions']), 2)
        self.assertEqual(response.context['region_id'], self.region.id)


class BillModel(TestCase):
    def setUp(self):
        self.region = BillRegion.objects.create(title=u'TestRegion')
        self.bill = Bill.objects.create(title=u'TestBill',
                                        description=u'BillDescription',
                                        region=self.region,
                                        contacts=u'TestContacts')
        self.client = Client()

    def test_create(self):
        test_bill = Bill.objects.last()
        self.assertEqual(self.bill, test_bill)

    def test_bill_view(self):
        self.assertTrue(self.bill in BillDetailView().get_queryset())

    def test_bill_get_request(self):
        response = self.client.get(reverse_lazy('bill_detail',
                                                kwargs={'pk': self.bill.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bill'], self.bill)
        self.assertEqual(self.region, self.bill.region)

    def test_bill_region_get_request(self):
        BillRegion.objects.create(title=u'Test2')
        Bill.objects.create(title=u'TestBill2',
                            description=u'BillDescription',
                            region=self.region,
                            contacts=u'TestContacts')
        Bill.objects.create(title=u'TestBill3',
                            description=u'BillDescription',
                            region=self.region,
                            contacts=u'TestContacts') 
        response = self.client.get(reverse_lazy('region_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['regions']), 2)
        self.assertEqual(len(response.context['bills']), 2)
        self.assertTrue(response.context['is_paginated'])

        response = self.client.get(reverse_lazy('region_detail',
                                                kwargs={'pk': self.region.id}))
        self.assertEqual(len(response.context['regions']), 2)
        self.assertEqual(len(response.context['bills']), 2)
        self.assertTrue(response.context['is_paginated'])
        for bill in response.context['bills']:
            self.assertEqual(self.region, bill.region)

    def test_bill_create_view(self):
        response = self.client.post(reverse_lazy('create_bill'), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(unicode(response.context['message']),
                         u'Форма заполнена неверно')
        data = {'title': 'test', 'description': 'decs', 'contacts': 'contacts',
                'region': 1}
        response = self.client.post(reverse_lazy('create_bill'), data)
        self.assertEqual(response.status_code, 302)
        bill = Bill.objects.last()
        region = BillRegion.objects.get(id=1)
        self.assertEqual(bill.title, 'test')
        self.assertEqual(bill.description, 'decs')
        self.assertEqual(bill.contacts, 'contacts')
        self.assertEqual(bill.region, region)
