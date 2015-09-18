# -*- coding: utf-8 -*-


def test_ctor(application):
    """
    Test creating an empty application.
    :param application:
    :return:
    """
    assert application.name == 'test'
    assert application.services == {}
