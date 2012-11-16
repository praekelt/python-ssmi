"""Exception classes for SSMI."""


class SSMIError(Exception):
    """Base exception class for the ssmi library."""


class SSMIRemoteServerError(SSMIError):
    """Bad behaviour detected from remote SSMI server."""
