import os
from unittest import skipIf

from django.test import TestCase

from django_ipam.models import IpAddress, Subnet

from .base.base import CreateModelsMixin
from .base.test_models import BaseTestModel


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestModel(BaseTestModel, CreateModelsMixin, TestCase):
    ipaddress_model = IpAddress
    subnet_model = Subnet
