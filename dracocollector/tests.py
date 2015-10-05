from django.test import TestCase
from django.core.urlresolvers import reverse
from dracocollector.models import SensorReading 

class ReadingCollectorTests(TestCase):
    def test_reading_collector(self):
        response = self.client.get(reverse('collector'),
                                   {'sourceName': 'unitTestSource',
                                    'fwVersion': '0.1',
                                    'temperature': '56',
                                    'humidity': '44'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Received sensor reading from unitTestSource')
        readings = SensorReading.objects.filter(source='unitTestSource')
        self.assertEqual(len(readings), 1)
        self.assertEqual(readings[0].temperature, 56)
        self.assertEqual(readings[0].humidity, 44)
        self.assertEqual(readings[0].lci1_active, False)
        self.assertEqual(readings[0].lci2_active, False)

    def test_reading_collector_with_lci2(self):
        response = self.client.get(reverse('collector'),
                                   {'sourceName': 'unitTestSourceWithLci2',
                                    'fwVersion': '0.1',
                                    'temperature': '11',
                                    'humidity': '57',
                                    'lci2': True})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Received sensor reading from unitTestSource')
        readings = SensorReading.objects.filter(source='unitTestSourceWithLci2')
        self.assertEqual(len(readings), 1)
        self.assertEqual(readings[0].temperature, 11)
        self.assertEqual(readings[0].humidity, 57)
        self.assertEqual(readings[0].lci1_active, False)
        self.assertEqual(readings[0].lci2_active, True)

    def test_reading_collector_missing_source(self):
        self.assert_missing_mandatory_parameter('sourceName',
                                                {'fwVersion': '0.1',
                                                 'temperature': '56',
                                                 'humidity': '44'})
    def test_reading_collector_missing_version(self):
        self.assert_missing_mandatory_parameter('fwVersion',
                                                {'sourceName': 'unitTestSourceMissingVersion',
                                                 'temperature': '56',
                                                 'humidity': '44'})

    def test_reading_collector_missing_temperature(self):
        self.assert_missing_mandatory_parameter('temperature',
                                                {'sourceName': 'unitTestSource',
                                                 'fwVersion': '0.1',
                                                 'humidity': '44'})

    def test_reading_collector_missing_humidity(self):
        self.assert_missing_mandatory_parameter('humidity',
                                                {'sourceName': 'unitTestSource',
                                                 'fwVersion': '0.1',
                                                 'temperature': '23'})

    def assert_missing_mandatory_parameter(self, parameter, existing_parameters):
        response = self.client.get(reverse('collector'), existing_parameters)
        self.assertEqual(response.status_code, 200)
        mandatory_parameter = "You need to provide the fields: ['%s']\n" % parameter
        self.assertContains(response, mandatory_parameter)

