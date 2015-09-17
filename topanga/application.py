# -*- coding: utf-8 -*-
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
    client = None
    containers = {}
    filename = None
    label_key = 'topanga.app'

    def __init__(self, name, client=None, containers=None, filename=None):
        """
        Initialize the Application

        :param name: string unique name
        :param client: docker-py's client
        :param filename: string YAML file name
        """
        self.name = name
        self.client = client
        self.containers = containers
        self.filename = filename

        if not containers:
            self.containers = {}

        if containers:
            for container in containers:
                self.containers[container.name] = container
        elif filename:
            instance = self.create_from_filename(filename)
            self.containers = instance.containers
        elif client:
            instance = self.create_from_client(name, client)
            self.containers = instance.containers

    def add_container(self, container):
        """
        Add a container to application
        :param container: `Container`
        """
        self.containers[container.name] = container

    @classmethod
    def create_from_client(cls, name, client):
        """
        Read all containers running in docker with either this name prefix,
        or this name tag.

        :param name: string unique name
        :param client: `Client`
        :return: `Application`
        """

        assert isinstance(client, Client)

        cs = {}

        def has_application_tag(c):
            """ Is container marked with this application name? """
            return c.get('Labels', {}).get(cls.label_key) and \
                   c['Labels'][cls.label_key] == name

        def get_name(c):
            """ Retrieve container name from dict. """
            return c['Names'][0]

        # Go through all containers and look at their Labels to see
        # if our application name is in there.
        for c in client.containers(all=True):
            if has_application_tag(c):
                cs[get_name(c)] = Container.from_ps(c)

        if cs:
            return Application(name, containers=cs)
        else:
            raise Exception(
                'There are no containers for application {0}'.format(name))

    @classmethod
    def create_from_filename(cls, filename):
        """
        Read all containers from the provided YAML file.

        :param name: string unique name
        :return: `Application`
        """
        # TODO
        pass
