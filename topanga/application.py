# -*- coding: utf-8 -*-


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

    def __init__(self, name, client, containers=None, filename=None):
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

    def add_container(self, container):
        """
        Add a container to application
        :param container: `Container`
        """
        self.containers[container.name] = container

    def _create_from_client(self, client):
        # TODO
        pass

    def _create_from_yaml(self, filename):
        # TODO
        pass

    def _create_from_containers(self, containers):
        # TODO
        pass
