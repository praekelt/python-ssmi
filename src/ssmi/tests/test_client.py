
from twisted.trial.unittest import TestCase
from src.ssmi.client import *


class SSMIClientTestCase(TestCase):

    def setUp(self):
        self.ssmi_client = SSMIClient()
        self.ssmi_client.app_setup(
                'user',
                'pass',
                self.ussd_test_callback,
                None,
                None)

    def tearDown(self):
        self.ssmi_client = None

    def ussd_test_callback(self, msisdn, ussd_type, phase, message, genfields={}):
        self.assertEqual(msisdn, '27831112222')
        self.assertEqual(ussd_type, '1')
        self.assertEqual(phase, '0')
        self.assertEqual(message, '*156#<cr>')
        self.assertEqual(genfields['IMSI'], '655011234567890')
        self.assertEqual(genfields['Subscriber type'], '1')
        self.assertEqual(genfields['OperatorID'], '')
        self.assertEqual(genfields['SessionID'], '')
        self.assertEqual(genfields['ValiPort'], '')

    def test_dataRecieved(self):
        self.ssmi_client.dataReceived('SSMI,111,27831112222,1,0,655011234567890:1::,*156#<cr>')


