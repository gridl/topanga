# -*- coding: utf-8 -*-
import networkx as nx

from docker import Client
from .container import Container
from .service import Service
from .labels import LABEL_APP_NAME, LABEL_SERVICE_NAME


class Application(object):
    """
    This is a linked set of Services.
    It can be created:

    * From scratch, providing a list of Services.
    * From docker-compose.yml.
    * From docker-py's client.

    """

    name = None
    client = None
    services = {}

    def __init__(self, name, client=None, services=None):
        """
        Initialize the Application

        :param name: string unique name
        :param client: `Client`
        :param services: list of type `Service`
        """
        self.name = name
        self.client = client

        if not services:
            self.services = {}
        else:
            for service in services:
                self.services[service.name] = service

    def add_service(self, service):
        """
        Add a service to application
        :param service: `Service`
        """
        self.services[service.name] = service

    def start(self):
        """
        Start all containers in correct (topological) order.
        """
        cdict = {c.name: c for c in self.containers}
        for cname in self.topology():
            cdict[cname].start()

    def stop(self):
        """
        Stop all containers in correct (reverse topological) order.
        """
        cdict = {c.name: c for c in self.containers}
        for cname in self.topology(reverse=True):
            cdict[cname].stop()

    def topology(self, reverse=False):
        """
        List containing topological sorting of containers.
        :return: list of <container_name>
        """
        g = nx.DiGraph()

        for service_name, service in self.services:

            # Service name is the name of this service's central container.
            g.add_node(service_name)

            # Add edges from containers listed in "--net" to this one.
            if service.net.is_from_container():
                g.add_node(service.net.from_container)
                g.add_edge(service.net.from_container, service_name)

            # Add edges from linked containers to this one.
            for link_name in service.links:
                link_from_name = link_name.split(':')[0]
                g.add_node(link_from_name)
                g.add_edge(link_from_name, service_name)

            # Add edges from containers listed in "--volumes-from" to this one.
            for from_name in service.volumes_from:
                g.add_node(from_name)
                g.add_edge(from_name, service_name)

        return nx.topological_sort(g, reverse=reverse)

    @property
    def containers(self):
        """
        Get dict of containers labeled into this Application.
        :return: dict <name> : `Container`
        """
        containers = {}
        for c in self.client.containers(
                all=True, filters={'labels': self.labels}):
            container = Container.from_ps(self.client, c)
            containers[container.name] = container
        return containers

    @property
    def labels(self):
        return ['{0}={1}'.format(LABEL_APP_NAME, self.name)]

    @classmethod
    def get_containers(cls, name, client):
        """
        Get list of containers labeled into this Application.
        :param name: string unique name
        :param client: `Client`
        :return: list of `Container`
        """
        return [Container.from_ps(client, c) for c in client.containers(
                all=True,
                filters={'labels': ['{0}={1}'.format(LABEL_APP_NAME, name)]})]

    @classmethod
    def from_client(cls, name, client):
        """
        Read all services running in docker labeled with this app name.

        :param name: string unique name
        :param client: `Client`
        :return: `Application`
        """
        assert isinstance(client, Client)

        services = {}

        for container in cls.get_containers(name, client):
            if LABEL_SERVICE_NAME in container.labels:
                services[container.labels[LABEL_SERVICE_NAME]] = \
                    Service.from_container(container, client)

        if services:
            return Application(name, client, services=services)
        else:
            raise Exception(
                'There are no services for application {0}.'.format(name))

    @classmethod
    def from_filename(cls, name, filename):
        """
        Read all containers from the provided YAML file.

        :param name: string unique name
        :param filename: string YAML file name
        :return: `Application`
        """
        # TODO
        raise NotImplementedError('Not Implemented.')
