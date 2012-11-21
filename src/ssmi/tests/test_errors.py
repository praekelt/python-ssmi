# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8 ai ts=4 sts=4 et sw=4
# Copyright 2011 Praekelt Foundation <dev@praekeltfoundation.org>
# BSD - see LICENSE for details

from twisted.trial.unittest import TestCase
from ssmi.errors import SSMIError, SSMIRemoteServerError


class SSMIRemoteServerErrorTestCase(TestCase):
    def test_subclasses_ssmierror(self):
        self.assertTrue(isinstance(SSMIRemoteServerError("Test"),
                                   SSMIError))
