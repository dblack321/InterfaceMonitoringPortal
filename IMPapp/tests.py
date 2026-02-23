from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Interface, AlertLevel, Alert, Metric, Threshold


class InterfaceModelTests(TestCase):
    def test_interface_add(self):
        self.client.post('/manageInterface/add/', {'name': 'Router', 'description': 'Core router'})
        self.assertEqual(Interface.objects.get(name='Router').name, 'Router')

    def test_interface_update(self):
        interface = Interface.objects.create(name='Switch', description='Network switch')
        self.client.post(f'/manageInterface/edit/{interface.pk}/', {'name': 'Switch', 'description': 'Updated description'})
        self.assertEqual(Interface.objects.get(pk=interface.pk).description, 'Updated description')


