
from twisted.trial.unittest import TestCase
from ssmi.client import SSMIClient
from ssmi.errors import SSMIRemoteServerError


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
            "msisdn": msisdn,
            "ussd_type": ussd_type,
            "phase": phase,
            "message": message,
            "genfields": genfields})

    def test_dataRecieved_111(self):
        self.ssmi_client.dataReceived(
            'SSMI,111,27831112222,1,0,655011234567890:1::,*156#\r')
        self.assertTrue(len(self.callback_populated_list) > 0)
        list_0 = self.callback_populated_list[0]
        self.assertEqual(list_0['msisdn'], '27831112222')
        self.assertEqual(list_0['ussd_type'], '1')
        self.assertEqual(list_0['phase'], '0')
        self.assertEqual(list_0['message'], '*156#')
        genfields = list_0['genfields']
        self.assertEqual(genfields['IMSI'], '655011234567890')
        self.assertEqual(genfields['Subscriber type'], '1')
        self.assertEqual(genfields['OperatorID'], '')
        self.assertEqual(genfields['SessionID'], '')
        self.assertEqual(genfields['ValiPort'], '')

    def test_dataRecieved_110(self):
        self.ssmi_client.dataReceived('SSMI,110,27831112222,1,0,*156#\r')
        self.assertTrue(len(self.callback_populated_list) > 0)
        list_0 = self.callback_populated_list[0]
        self.assertEqual(list_0['msisdn'], '27831112222')
        self.assertEqual(list_0['ussd_type'], '1')
        self.assertEqual(list_0['phase'], '0')
        self.assertEqual(list_0['message'], '*156#')
        self.assertEqual(list_0['genfields'], {})

    def test_multi_line_receive(self):
        lines = ('SSMI,110,27831112222,1,0,*156#\r'
                 'SSMI,110,27831112222,1,0,*157#\r')
        self.ssmi_client.dataReceived(lines)
        list_0, list_1 = self.callback_populated_list
        self.assertEqual(list_0['message'], '*156#')
        self.assertEqual(list_1['message'], '*157#')

    def test_split_line_receive(self):
        self.ssmi_client.dataReceived('SSMI,110,27831112222')
        self.ssmi_client.dataReceived(',1,0,*156#\r')
        [list_0] = self.callback_populated_list
        self.assertEqual(list_0['message'], '*156#')

    def test_bad_line_receive(self):
        self.ssmi_client.dataReceived('Garbage\r')
        [err] = self.flushLoggedErrors(SSMIRemoteServerError)
        self.assertEqual(err.value.args, ("No SSMI header. Skipping bad line"
                         " 'Garbage'",))
