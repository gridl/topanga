# -*- coding: utf-8 -*-
import networkx as nx

from docker import Client
from .container import Container


class Application(object):
    """
    This is a linked set of Containers.
    It can be created:

    * From scratch, providing a dict of Containers.
    * From docker-compose.yml.
    * From docker-py's client.

    """

    name = None
    containers = {}
    label_key = 'topanga.app'

    def __init__(self, name, containers=None):
        """
        Initialize the Application

        :param name: string unique name
        :param containers: list of type Container
        """
        self.name = name

        if not containers:
            self.containers = {}
        else:
            for container in containers:
                self.containers[container.name] = container

    def add_container(self, container):
        """
        Add a container to application
        :param container: `Container`
        """
        self.containers[container.name] = container

    def start(self, client):
        """
        Start all containers in correct (topological) order.
        :param client: `Client`
        """
        for cname in self.topology(client):
            self.containers[cname].start()

    def stop(self, client):
        """
        Stop all containers in correct (reverse topological) order.
        :param client: `Client`
        """
        for cname in self.topology(client, reverse=True):
            self.containers[cname].stop()

    def topology(self, client, reverse=False):
        """
        List containing topological sorting of containers.
        :param client: `Client`
        :return: list
        """
        g = nx.DiGraph(self.containers.keys())

        for c in self.containers.values():

            # Add edges from linked containers to this one.
            for link_name in c.links:
                g.add_edge(link_name, c.name)

            # Add edges from containers listed in "--net" to this one.
            net = c.get('HostConfig.NetworkMode')
            if net.startswith('container:'):
                other_name = net.split('container:')[0]
                other_name = other_name.split['/'][-1]
                g.add_edge(other_name, c.name)

            # Add edges from containers listed in "--volumes-from" to this one.
            for cid in c.get('HostConfig.VolumesFrom'):
                other = Container.from_id(client, cid)
                g.add_edge(other.name, c.name)

        return nx.topological_sort(g, reverse=reverse)

    @classmethod
    def labels(cls, name):
        return ['{0}={1}'.format(cls.label_key, name)]

    @classmethod
    def from_client(cls, name, client):
        """
        Read all containers running in docker labeled with this app name.

        :param name: string unique name
        :param client: `Client`
        :return: `Application`
        """

        assert isinstance(client, Client)

        containers = {}

        # See if there's any containers labeled into this Application.
        for cdict in client.containers(
                all=True,
                filters={'labels': cls.labels(name)}):
            container = Container.from_ps(cdict)
            containers[container.name] = container

        if containers:
            return Application(name, containers=containers)
        else:
            raise Exception(
                'There are no containers for application {0}'.format(name))

    @classmethod
    def from_filename(cls, name, filename):
        """
        Read all containers from the provided YAML file.

        :param name: string unique name
        :param filename: string YAML file name
        :return: `Application`
        """
        # TODO
        pass
