from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .base import CreateModelsMixin


class BaseTestAdmin(CreateModelsMixin):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                      password='tester',
                                      email='admin@admin.com')
        self.client.login(username='admin', password='tester')

    def test_ipaddress_invalid_entry(self):
        subnet = self._create_subnet(subnet="10.0.0.0/24", description="Sample Subnet")
        post_data = {
            'ip_address': "12344",
            'subnet': subnet.id,
            'created_0': '2017-08-08',
            'created_1': '15:16:10',
            'modified_0': '2017-08-08',
            'modified_1': '15:16:10',
        }
        response = self.client.post(reverse('admin:{0}_ipaddress_add'.format(self.app_name)),
                                    post_data, follow=True)
        self.assertContains(response, 'ok')
        self.assertContains(response, 'Enter a valid IPv4 or IPv6 address.')

    def test_ipaddress_change(self):
        subnet = self._create_subnet(subnet="10.0.0.0/24", description="Sample Subnet")
        obj = self._create_ipaddress(ip_address="10.0.0.1", subnet=subnet)

        response = self.client.get(reverse('admin:{0}_ipaddress_change'.format(self.app_name), args=[obj.pk]),
                                   follow=True)
        self.assertContains(response, 'ok')
        self.assertEqual(self.ipaddress_model.objects.get(pk=obj.pk).ip_address, '10.0.0.1')

    def test_ipv4_subnet_change(self):
        subnet = self._create_subnet(subnet="10.0.0.0/24", description="Sample Subnet")
        self._create_ipaddress(ip_address="10.0.0.1", subnet=subnet)

        response = self.client.get(reverse('admin:{0}_subnet_change'.format(self.app_name), args=[subnet.pk]),
                                   follow=True)
        self.assertContains(response, 'ok')
        self.assertContains(response, '<h3>Subnet Visual Display</h3>')

    def test_ipv6_subnet_change(self):
        subnet = self._create_subnet(subnet="fdb6:21b:a477::9f7/64", description="Sample Subnet")
        self._create_ipaddress(ip_address="fdb6:21b:a477::9f7", subnet=subnet)

        response = self.client.get(reverse('admin:{0}_subnet_change'.format(self.app_name), args=[subnet.pk]),
                                   follow=True)
        self.assertContains(response, 'ok')
        self.assertContains(response, '<h3>Used IP address</h3>')

    def test_subnet_invalid_entry(self):
        post_data = {
            'subnet': "12344",
            'created_0': '2017-08-08',
            'created_1': '15:16:10',
            'modified_0': '2017-08-08',
            'modified_1': '15:16:10',
        }

        response = self.client.post(reverse('admin:{0}_subnet_add'.format(self.app_name)),
                                    post_data, follow=True)
        self.assertContains(response, 'ok')
        self.assertContains(response, 'Enter a valid CIDR address.')

    def test_subnet_popup_response(self):
        subnet = self._create_subnet(subnet="fdb6:21b:a477::9f7/64", description="Sample Subnet")
        self._create_ipaddress(ip_address="fdb6:21b:a477::9f7", subnet=subnet)

        response = self.client.get('/admin/{0}/subnet/{1}/change/?_popup=1'.format(self.app_name, subnet.id),
                                   follow=True)
        self.assertContains(response, 'ok')

    def test_ipaddress_response(self):
        subnet = self._create_subnet(subnet="10.0.0.0/24", description="Sample Subnet")
        post_data = {
            'ip_address': "10.0.0.1",
            'subnet': subnet.id,
            'created_0': '2017-08-08',
            'created_1': '15:16:10',
            'modified_0': '2017-08-08',
            'modified_1': '15:16:10',
        }
        response = self.client.post(reverse('admin:{0}_ipaddress_add'.format(self.app_name)),
                                    post_data, follow=True)
        self.assertContains(response, 'ok')

    def test_ipaddress_popup_response(self):
        subnet = self._create_subnet(subnet="10.0.0.0/24", description="Sample Subnet")
        post_data = {
            'ip_address': "10.0.0.1",
            'subnet': subnet.id,
            'created_0': '2017-08-08',
            'created_1': '15:16:10',
            'modified_0': '2017-08-08',
            'modified_1': '15:16:10',
            '_popup': '1',
        }
        response = self.client.post(reverse('admin:{0}_ipaddress_add'.format(self.app_name)),
                                    post_data)
        self.assertContains(response, 'opener.dismissAddAnotherPopup(window);')

    def test_csv_upload(self):
        csv_data = """Monachers - Matera,
        10.27.1.0/24,
        ,
        ip address,description
        10.27.1.1,Monachers
        10.27.1.252,NanoStation M5
        10.27.1.253,NanoStation M5
        10.27.1.254,Nano Beam 5 19AC"""

        csvfile = SimpleUploadedFile("data.csv", bytes(csv_data, 'utf-8'))
        response = self.client.post(reverse('admin:import_ipaddress'.format(self.app_name)),
                                    {'csvfile': csvfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.subnet_model.objects.first().subnet), '10.27.1.0/24')
        self.assertEqual(str(self.ipaddress_model.objects.all()[0].ip_address), '10.27.1.1')
        self.assertEqual(str(self.ipaddress_model.objects.all()[1].ip_address), '10.27.1.252')
        self.assertEqual(str(self.ipaddress_model.objects.all()[2].ip_address), '10.27.1.253')
        self.assertEqual(str(self.ipaddress_model.objects.all()[3].ip_address), '10.27.1.254')

    def test_subnet_csv_export(self):
        subnet = self._create_subnet(subnet="10.0.0.0/24", name="Sample Subnet")
        self._create_ipaddress(ip_address="10.0.0.1", subnet=subnet, description="Testing")
        self._create_ipaddress(ip_address="10.0.0.2", subnet=subnet, description="Testing")
        self._create_ipaddress(ip_address="10.0.0.3", subnet=subnet)
        self._create_ipaddress(ip_address="10.0.0.4", subnet=subnet)

        csv_data = """Sample Subnet\r
        10.0.0.0/24\r
        \r
        ip_address,description\r
        10.0.0.1,Testing\r
        10.0.0.2,Testing\r
        10.0.0.3,\r
        10.0.0.4,\r
        """

        csv_data = bytes(csv_data.replace('        ', ''), 'utf-8')
        response = self.client.get(reverse('admin:export_ipaddress', args=[subnet.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, csv_data)

    def test_importcsv_form(self):
        response = self.client.get(reverse('admin:import_ipaddress'), follow=True)
        self.assertEqual(response.status_code, 200)
