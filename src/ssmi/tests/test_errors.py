
from twisted.trial.unittest import TestCase
from ssmi.errors import SSMIError, SSMIRemoteServerError


class SSMIRemoteServerErrorTestCase(TestCase):
    def test_subclasses_ssmierror(self):
        self.assertTrue(isinstance(SSMIRemoteServerError("Test"),
                                   SSMIError))
