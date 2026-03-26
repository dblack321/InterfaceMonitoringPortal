from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Interface, AlertLevel, Alert, Metric, Threshold


class AuthenticatedTestCase(TestCase):
    def setUp(self):
        super().setUp()
        # create a user and give it the permissions needed for CRUD operations
        self.user = User.objects.create_user(username='tester', password='password')

        content_types = [
            ContentType.objects.get_for_model(Interface),
            ContentType.objects.get_for_model(Metric),
            ContentType.objects.get_for_model(Threshold),
            ContentType.objects.get_for_model(Alert),
        ]

        perms = Permission.objects.filter(
            content_type__in=content_types,
            codename__in=[
                'add_interface', 'change_interface', 'delete_interface',
                'add_metric', 'change_metric', 'delete_metric',
                'add_threshold', 'change_threshold', 'delete_threshold',
                'add_alert', 'change_alert', 'delete_alert',
            ],
        )

        self.user.user_permissions.add(*perms)
        self.client.force_login(self.user)

        self.minor_alert_level = AlertLevel.objects.create(name='Minor', description='Minor Alert')
        self.critical_alert_level = AlertLevel.objects.create(name='Critical', description='Critical Alert')
        self.warning_alert_level = AlertLevel.objects.create(name='Warning', description='Warning Alert')


class InterfaceModelTests(AuthenticatedTestCase):


    def test_interface_add(self):
        self.client.post('/addInterface/', {'name': 'testInterface1', 'description': 'testInterface1'})
        self.assertEqual(Interface.objects.filter(name='testInterface1').first().name, 'testInterface1')

    def test_interface_update(self):
        interface = Interface.objects.create(name='testInterface2', description='testInterface2')
        self.client.post(f'/editInterface/{interface.pk}/', {'name': 'testInterface2', 'description': 'Updated description'})
        self.assertEqual(Interface.objects.filter(pk=interface.pk).first().description, 'Updated description')

    def test_interface_deleteTresholdAssigned(self):
        interface = Interface.objects.create(name='testInterface3', description='testInterface3')
        metric = Metric.objects.create(name='testMetric1', unit_of_measure='units')
        Threshold.objects.create(interface=interface, metric=metric, alert_level=self.warning_alert_level, upper_limit=100.0, lower_limit=0.0, description='Test threshold description')
        self.client.post(f'/removeInterface/{interface.pk}/')
        self.assertTrue(Interface.objects.filter(pk=interface.pk).exists())

    def test_interface_delete(self):
        interface = Interface.objects.create(name='testInterface3', description='testInterface3')
        self.client.post(f'/removeInterface/{interface.pk}/')
        self.assertFalse(Interface.objects.filter(pk=interface.pk).exists())


class AlertModelTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.interface = Interface.objects.create(name='testInterface1', description='testInterface1')

    def test_alert_createDummyAlerts(self):
        self.client.post('/createDummyAlerts/')
        self.assertEqual(Alert.objects.filter(status='NEW').count(), 5)

    def test_alert_acknowledge(self):
        alert = Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message', status='NEW')
        self.client.post(f'/acknowledgeAlert/{alert.pk}/')
        self.assertEqual(Alert.objects.filter(pk=alert.pk).first().status, 'ACKNOWLEDGED')

    def test_alert_delete(self):
        alert = Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message', status='NEW')
        self.client.post(f'/removeAlert/{alert.pk}/')
        self.assertFalse(Alert.objects.filter(pk=alert.pk).exists())

    def test_alert_deleteAllAcknowledged(self):
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 1', status='ACKNOWLEDGED')
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 2', status='ACKNOWLEDGED')
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 3', status='ACKNOWLEDGED')
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 4', status='ACKNOWLEDGED')
        self.client.post(f'/removeAllAlerts/')
        self.assertFalse(Alert.objects.all().exists())
    
    def test_alert_deleteAllNew(self):
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 1', status='NEW')
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 2', status='NEW')
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 3', status='NEW')
        Alert.objects.create(interface=self.interface, alert_level=self.warning_alert_level, message='Test alert message 4', status='NEW')
        self.client.post(f'/removeAllAlerts/')
        self.assertTrue(Alert.objects.all().exists())


class MetricModelTests(AuthenticatedTestCase):
    def test_metric_add(self):
        self.client.post('/addMetric/', {'name': 'testMetric1', 'unit_of_measure': 'units'})
        self.assertEqual(Metric.objects.filter(name='testMetric1').first().name, 'testMetric1')

    def test_metric_update(self):
        metric = Metric.objects.create(name='testMetric2', unit_of_measure='units')
        self.client.post(f'/editMetric/{metric.pk}/', {'name': 'testMetric2', 'unit_of_measure': 'updated units'})
        self.assertEqual(Metric.objects.filter(pk=metric.pk).first().unit_of_measure, 'updated units')

    def test_metric_delete(self):
        metric = Metric.objects.create(name='testMetric3', unit_of_measure='units')
        self.client.post(f'/removeMetric/{metric.pk}/')
        self.assertFalse(Metric.objects.filter(pk=metric.pk).exists())

class ThresholdModelTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.interface = Interface.objects.create(name='testInterface1', description='testInterface1')
        self.metric = Metric.objects.create(name='testMetric1', unit_of_measure='units')

    def test_threshold_add(self):
        self.client.post('/addThreshold/', {
            'interface': self.interface.pk,
            'metric': self.metric.pk,
            'alert_level': self.warning_alert_level.pk,
            'upper_limit': 100.0,
            'lower_limit': 0.0,
            'description': 'Test threshold description'
        })
        self.assertEqual(Threshold.objects.filter(description='Test threshold description').first().description, 'Test threshold description')

    def test_threshold_update(self):
        threshold = Threshold.objects.create(interface=self.interface, metric=self.metric, alert_level=self.warning_alert_level, upper_limit=100.0, lower_limit=0.0, description='Test threshold description')
        self.client.post(f'/editThreshold/{threshold.pk}/', {
            'interface': self.interface.pk,
            'metric': self.metric.pk,
            'alert_level': self.warning_alert_level.pk,
            'upper_limit': 150.0,
            'lower_limit': 10.0,
            'description': 'Updated threshold description'
        })
        self.assertEqual(Threshold.objects.filter(pk=threshold.pk).first().upper_limit, 150.0)
        self.assertEqual(Threshold.objects.filter(pk=threshold.pk).first().lower_limit, 10.0)
        self.assertEqual(Threshold.objects.filter(pk=threshold.pk).first().description, 'Updated threshold description')

    def test_threshold_delete(self):
        threshold = Threshold.objects.create(interface=self.interface, metric=self.metric, alert_level=self.warning_alert_level, upper_limit=100.0, lower_limit=0.0, description='Test threshold description')
        self.client.post(f'/removeThreshold/{threshold.pk}/')
        self.assertFalse(Threshold.objects.filter(pk=threshold.pk).exists())
