from io import StringIO

from django.core.management import CommandError, call_command

from .base import CreateModelsMixin


class BaseTestCommands(CreateModelsMixin):
    def test_export_subnet_command(self):
        subnet = self._create_subnet(subnet='10.0.0.0/24', name='Sample Subnet')
        self._create_ipaddress(ip_address='10.0.0.1', subnet=subnet, description='Testing')
        self._create_ipaddress(ip_address='10.0.0.2', subnet=subnet, description='Testing')
        self._create_ipaddress(ip_address='10.0.0.3', subnet=subnet)
        self._create_ipaddress(ip_address='10.0.0.4', subnet=subnet)
        out = StringIO()
        call_command('export_subnet', '10.0.0.0/24', stdout=out)
        self.assertIn('Successfully exported 10.0.0.0/24', out.getvalue())
        with self.assertRaises(CommandError):
            call_command('export_subnet', '11.0.0.0./24')
        with self.assertRaises(CommandError):
            call_command('export_subnet', '11.0.0.0/24')

    def test_import_subnet_command(self):
        with self.assertRaises(CommandError):
            call_command('import_subnet', file='{0}/tests/static/invalid_data.csv'.format(self.app_name))
        self.assertEqual(self.subnet_model.objects.all().count(), 0)
        self.assertEqual(self.ipaddress_model.objects.all().count(), 0)
        call_command('import_subnet', file='{0}/tests/static/import_data.xls'.format(self.app_name))
        self.assertEqual(self.subnet_model.objects.all().count(), 1)
        self.assertEqual(self.ipaddress_model.objects.all().count(), 8)
        with self.assertRaises(CommandError):
            call_command('import_subnet', file='invalid.pdf')
        with self.assertRaises(CommandError):
            call_command('import_subnet', file='invalid_path.csv')
