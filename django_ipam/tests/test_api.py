from django.test import TestCase

from django_ipam.models import IpAddress, Subnet

from .base.base import CreateModelsMixin
from .base.test_api import BaseTestApi


class TestApi(BaseTestApi, CreateModelsMixin, TestCase):
    subnet_model = Subnet
    ipaddress_model = IpAddress
