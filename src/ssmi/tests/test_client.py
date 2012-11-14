
from twisted.trial.unittest import TestCase
from src.ssmi.client import *


class SSMIClientTestCase(TestCase):

    def setUp(self):
        self.callback_populated_list = []
        self.ssmi_client = SSMIClient()
        self.ssmi_client.app_setup(
                'user',
                'pass',
                self.ussd_test_callback,
                None,
                None)

    def ussd_test_callback(self, msisdn, ussd_type, phase, message,
                                                    genfields=None):
        if genfields is None:
            genfields = {}
        self.callback_populated_list.append({
            "msisdn": '27831112222',
            "ussd_type": '1',
            "phase": '0',
            "message": '*156#<cr>',
            "genfields": genfields})

    def test_dataRecieved_111(self):
        self.ssmi_client.dataReceived(
                'SSMI,111,27831112222,1,0,655011234567890:1::,*156#<cr>')
        self.assertTrue(len(self.callback_populated_list) > 0)
        list_0 = self.callback_populated_list[0]
        self.assertEqual(list_0['msisdn'], '27831112222')
        self.assertEqual(list_0['ussd_type'], '1')
        self.assertEqual(list_0['phase'], '0')
        self.assertEqual(list_0['message'], '*156#<cr>')
        genfields = list_0['genfields']
        self.assertEqual(genfields['IMSI'], '655011234567890')
        self.assertEqual(genfields['Subscriber type'], '1')
        self.assertEqual(genfields['OperatorID'], '')
        self.assertEqual(genfields['SessionID'], '')
        self.assertEqual(genfields['ValiPort'], '')

    def test_dataRecieved_110(self):
        self.ssmi_client.dataReceived('SSMI,110,27831112222,1,0,*156#<cr>')
        self.assertTrue(len(self.callback_populated_list) > 0)
        list_0 = self.callback_populated_list[0]
        self.assertEqual(list_0['msisdn'], '27831112222')
        self.assertEqual(list_0['ussd_type'], '1')
        self.assertEqual(list_0['phase'], '0')
        self.assertEqual(list_0['message'], '*156#<cr>')
        self.assertEqual(list_0['genfields'], {})
