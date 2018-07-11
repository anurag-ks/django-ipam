import swapper
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .generics import (
    BaseIpAddressListCreateView, BaseIpAddressView, BaseRequestIPView, BaseSubnetListCreateView,
    BaseSubnetView,
)

IpAddress = swapper.load_model('django_ipam', 'IpAddress')
Subnet = swapper.load_model('django_ipam', 'Subnet')


@api_view(['GET'])
def get_first_available_ip(request, subnet_id):
    """
    Get the next available IP address under a subnet
    """
    subnet = get_object_or_404(Subnet, pk=subnet_id)
    return Response(subnet.get_first_available_ip())


class RequestIPView(BaseRequestIPView):
    """
    Request and create a record for the next available IP address under a subnet
    """
    subnet_model = Subnet
    queryset = IpAddress.objects.none()


class SubnetIpAddressListCreateView(BaseIpAddressListCreateView):
    """
    List/Create IP addresses under a specific subnet
    """
    subnet_model = Subnet


class SubnetListCreateView(BaseSubnetListCreateView):
    """
    List/Create subnets
    """
    queryset = Subnet.objects.all()


class SubnetView(BaseSubnetView):
    """
    View for retrieving, updating or deleting a subnet instance.
    """
    queryset = Subnet.objects.all()


class IpAddressView(BaseIpAddressView):
    """
    View for retrieving, updating or deleting a IP address instance.
    """
    queryset = IpAddress.objects.all()


request_ip = RequestIPView.as_view()
subnet_list_create = SubnetListCreateView.as_view()
subnet = SubnetView.as_view()
ip_address = IpAddressView.as_view()
subnet_list_ipaddress = SubnetIpAddressListCreateView.as_view()
