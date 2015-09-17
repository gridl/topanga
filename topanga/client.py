# -*- coding: utf-8 -*-

import sys
import ssl

from docker import AutoVersionClient
from docker.utils import kwargs_from_env


def get_client(timeout=None):
    """
    Create and return docker-py client instance.
    :param timeout: int seconds
    :return: `AutoVersionClient`
    """
    if sys.platform.startswith('darwin') \
            or sys.platform.startswith('win32'):
            # mac or win
        kwargs = kwargs_from_env()
        # hack from here:
        # http://docker-py.readthedocs.org/en/latest/boot2docker/
        # See also: https://github.com/docker/docker-py/issues/406
        if 'tls' in kwargs:
            kwargs['tls'].assert_hostname = False
        kwargs['timeout'] = timeout
        return AutoVersionClient(**kwargs)
    else:
        # unix-based
        kwargs = kwargs_from_env(ssl_version=ssl.PROTOCOL_TLSv1,
                                 assert_hostname=False)
        kwargs['timeout'] = timeout
        return AutoVersionClient(**kwargs)
