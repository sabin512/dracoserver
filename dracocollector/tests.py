from django.test import TestCase
from django.core.urlresolvers import reverse


class ReadingCollectorTests(TestCase):
    
    def test_reading_collector(self):
        response = self.client.get(reverse('collector'),
                                   {'sourceName': 'unitTestSource',
                                    'temperatureReading': '56',
                                    'humidityReading': '44'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Received sensor reading from unitTestSource')

    def test_reading_collector_missing_source(self):
        self.assert_missing_mandatory_parameter('sourceName',
                                                {'temperatureReading': '56',
                                                 'humidityReading': '44'})

    def test_reading_collector_missing_temperature(self):
        self.assert_missing_mandatory_parameter('temperatureReading',
                                                {'sourceName': 'unitTestSource',
                                                 'humidityReading': '44'})

    def test_reading_collector_missing_temperature(self):
        self.assert_missing_mandatory_parameter('humidityReading',
                                                {'sourceName': 'unitTestSource',
                                                 'temperatureReading': '23'})

    def assert_missing_mandatory_parameter(self, parameter, existing_parameters):
        response = self.client.get(reverse('collector'), existing_parameters)
        self.assertEqual(response.status_code, 200)
        mandatory_parameter = "You need to provide '%s' in your request.\n" % parameter
        self.assertContains(response, mandatory_parameter)

