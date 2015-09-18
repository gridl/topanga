# -*- coding: utf-8 -*-
import json

from .labels import LABEL_APP_NAME, LABEL_SERVICE_NAME, LABEL_LINKS, \
    LABEL_NET, LABEL_VOLUMES_FROM


class Service(object):

    """
    Service is pretty much a wrapper for a single record in docker-compose
    YAML. It adds volumes-from, links, network to container, connecting it to
    other containers.

    Note that service name is the name of the container that's central to
    this service.

    """

    name = None
    app_name = None
    client = None
    links = None
    volumes_from = None
    net = None

    def __init__(self, name, app_name, client=None, links=None,
                 volumes_from=None, net=None):
        """
        Set this service's parameters (dependencies).
        :param name: string
        :param app_name: string
        :param client: `Client`
        :param links: list of container <name>:<alias>
        :param volumes_from: list of container <name>
        :param net: string
        """
        self.name = name
        self.app_name = app_name
        self.client = client
        self.links = links or []
        self.volumes_from = volumes_from or []
        self.net = Net(net)

    @property
    def container(self):
        """
        Return container to which this service label was applied.
        """
        cs = self.client.containers(all=True, filters={'labels': self.labels})
        return cs[0] if cs else None

    def create_container(self):
        """
        Create container using docker-py.
        """
        return self.client.create_container(
            name=self.name,
            labels=self.all_labels,
            volumes_from=self.volumes_from,
            host_config=self.client.create_host_config(
                links=self.links,
                network_mode=self.net.mode)
        )

    @classmethod
    def from_container(cls, container, client):
        """
        Retrieve this service's information back from container.
        :param container: `Container`
        :param client: `Client`
        """
        return Service(container.labels[LABEL_SERVICE_NAME],
                       container.labels[LABEL_APP_NAME],
                       client,
                       json.loads(container.labels[LABEL_LINKS]),
                       json.loads(container.labels[LABEL_VOLUMES_FROM]),
                       container.labels[LABEL_NET])

    @property
    def labels(self):
        """
        Return labels to filter on.
        """
        return [
            '{0}={1}'.format(LABEL_APP_NAME, self.app_name),
            '{0}={1}'.format(LABEL_SERVICE_NAME, self.name)
        ]

    @property
    def all_labels(self):
        """
        Return labels to apply to container.
        """
        return [
            '{0}={1}'.format(LABEL_APP_NAME, self.app_name),
            '{0}={1}'.format(LABEL_SERVICE_NAME, self.name),
            '{0}={1}'.format(LABEL_LINKS, json.dumps(self.links)),
            '{0}={1}'.format(LABEL_VOLUMES_FROM, json.dumps(self.volumes_from)),
            '{0}={1}'.format(LABEL_NET, self.net.mode),
        ]


class Net(object):
    """
    Net mode can be:

    * bridge: creates a new network stack for the container on the docker bridge
    * none: no networking for this container
    * host: use the host network stack inside the container
    * container:<name|id>: reuses another container network stack
    """

    mode = None
    from_container = None

    def __init__(self, mode):
        self.mode = mode

        if mode.startswith('container:'):
            self.from_container = mode.split(':')[-1]

    @property
    def is_from_container(self):
        return self.from_container is not None
