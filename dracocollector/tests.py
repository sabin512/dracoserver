from django.test import TestCase
from django.core.urlresolvers import reverse


class ReadingCollectorTests(TestCase):
    def test_reading_collector_missing_source(self):
        response = self.client.get(reverse('collector'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sourceName')
    
    def test_reading_collector(self):
        response = self.client.get(reverse('collector'),{'sourceName': 'unitTestSource',
                                                         'temperatureReading': '56',
                                                         'humidityReading': '44'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Received sensor reading from unitTestSource')
