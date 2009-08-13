"""Python module for SSMI protocol to send/receive USSD and SMS."""

# Copyright 2009 Praekelt International, all rights reserved

# Imports

from twisted.internet import reactor, protocol
import time

# Constants

HOSTNAME = 'connect.truteq.com'
PORT = 40017
USERNAME = 'praekelt'
PASSWORD = 'morgan'

LINKCHECK_PERIOD = 60.0

SSMI_HEADER = "SSMI"

SSMI_SEND_LOGIN = "1"
SSMI_SEND_SMS = "2"
SSMI_SEND_LINK_CHECK = "3"
SSMI_SEND_BINARY = "4"
SSMI_SEND_LOGOUT = "99"
SSMI_SEND_USSD = "110"

SSMI_RESPONSE_SEQ = "100"
SSMI_RESPONSE_ACK = "101"
SSMI_RESPONSE_NACK = "102"
SSMI_RESPONSE_TEXT_MESSAGE = "103"
SSMI_RESPONSE_DELIVERY_MESSAGE = "104"
SSMI_RESPONSE_FREEFORM_MESSAGE = "105"
SSMI_RESPONSE_BINARY_MESSAGE = "106"
SSMI_RESPONSE_PREMIUMRATED_MESSAGE = "107"
SSMI_RESPONSE_BINARY_PREMIUMRATED_MESSAGE = "108"
SSMI_RESPONSE_USSD = "110"
SSMI_RESPONSE_USSD_EXTENDED = "111"
SSMI_RESPONSE_EXTENDED_RETURN = "113"
SSMI_RESPONSE_EXTENDED_RETURN_BINARY = "116"
SSMI_RESPONSE_EXTENDED_PREMIUMRATED_MESSAGE = "117"
SSMI_RESPONSE_EXTENDED_BINARY_PREMIUMRATED_MESSAGE = "118"
SSMI_RESPONSE_REMOTE_LOGOUT = "199"

SSMI_USSD_TYPE_NEW = "1"
SSMI_USSD_TYPE_EXISTING = "2"
SSMI_USSD_TYPE_END = "3"
SSMI_USSD_TYPE_TIMEOUT = "4"

ack_reason = {
    "1": "Login OK",
    "2": "Link check response",
}

nack_reason = {
    "1": "Invalid username/password combination",
    "2": "Invalid/unknown message type",
    "3": "Could not parse message",
    "4": "Account suspended",
}

class SSMIClient(protocol.Protocol):
    """Client for SSMI"""

    def __init__(self, username, password, callback, errback):
        """init SSMIClient.

        username: string -- username for SSMI service
        password: string -- password for SSMI service
        callback: lambda -- callback for data received
        errback: lambda -- callback for error handling

        """
        self.username = username
        self.password = password
        self.callback = callback
        self.errback = errback
        print 'ran SSMIClient init'

    def connectionMade(self):
        """Handle connection establishment

        Log in
        """
        print 'logging in'
        self.transport.write("%s,%s,%s,%s\r" % (SSMI_HEADER,
                                                SSMI_SEND_LOGIN,
                                                self.username,
                                                self.password))
        self.updateCall = reactor.callLater(LINKCHECK_PERIOD, self.linkcheck)

    def linkcheck(self):
        print "linkcheck: ", time.time()
        self.updateCall = None
        self.transport.write("%s,%s\r" % (SSMI_HEADER,
                                          SSMI_SEND_LINK_CHECK))
        self.updateCall = reactor.callLater(LINKCHECK_PERIOD, self.linkcheck)

    def dataReceived(self, data):
        print "Server said:", data
        response = data.strip().split(',')
        # assumption: response[0] == SSMI_HEADER
        if not response[0] == SSMI_HEADER:
            print 'FAIL: No SSMI header. Aborting'
            reactor.stop()
        response_code = response[1]
        if response_code == SSMI_RESPONSE_ACK:
            reason = response[2]
            print 'ACK', ack_reason[reason]
        elif response_code == SSMI_RESPONSE_NACK:
            reason = response[2]
            print 'NACK', nack_reason[reason]
        elif response_code == SSMI_RESPONSE_USSD:
            msisdn, type, phase, message = response[2:6]
            if type == SSMI_USSD_TYPE_NEW:
                print 'New session'
            elif type == SSMI_USSD_TYPE_EXISTING:
                print 'Existing session'
            elif type == SSMI_USSD_TYPE_END:
                print 'END'
            elif type == SSMI_USSD_TYPE_TIMEOUT:
                print 'TIMEOUT'
            # Call a callback into the app with the message.
            reply = self.callback(msisdn, type, phase, message)
            if reply:
                self.transport.write(
                    "%s,%s,%s,%s,%s\r" %
                    (SSMI_HEADER, SSMI_SEND_USSD, msisdn,
                     SSMI_USSD_TYPE_EXISTING, str(reply)))


# SSMI_RESPONSE_SEQ = "100"
# SSMI_RESPONSE_TEXT_MESSAGE = "103"
# SSMI_RESPONSE_DELIVERY_MESSAGE = "104"
# SSMI_RESPONSE_FREEFORM_MESSAGE = "105"
# SSMI_RESPONSE_BINARY_MESSAGE = "106"
# SSMI_RESPONSE_PREMIUMRATED_MESSAGE = "107"
# SSMI_RESPONSE_BINARY_PREMIUMRATED_MESSAGE = "108"
# SSMI_RESPONSE_USSD = "110"
# SSMI_RESPONSE_USSD_EXTENDED = "111"
# SSMI_RESPONSE_EXTENDED_RETURN = "113"
# SSMI_RESPONSE_EXTENDED_RETURN_BINARY = "116"
# SSMI_RESPONSE_EXTENDED_PREMIUMRATED_MESSAGE = "117"
# SSMI_RESPONSE_EXTENDED_BINARY_PREMIUMRATED_MESSAGE = "118"
# SSMI_RESPONSE_REMOTE_LOGOUT = "199"


    def connectionLost(self, reason):
        if self.updateCall:
            self.updateCall.cancel()
        self.updateCall = None
        print "Connection lost", reason

class SSMIFactory(protocol.ReconnectingClientFactory):
    def __init__(self, username, password, callback=None, errback=None):
        self.__username = username
        self.__password = password
        self.__callback = callback
        self.__errback = errback

    def startConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return SSMIClient(self.__username, self.__password, self.__callback,
                          self.__errback)

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed", reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(
            self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print "Connection lost", reason
        protocol.ReconnectingClientFactory.clientConnectionLost(
            self, connector, reason)


def main():
    f = SSMIFactory(username=USERNAME, password=PASSWORD)
    reactor.connectTCP(HOSTNAME, PORT, f)
    reactor.run()

if __name__ == '__main__':
    main()
