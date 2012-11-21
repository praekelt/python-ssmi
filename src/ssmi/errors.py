# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8 ai ts=4 sts=4 et sw=4
# Copyright 2011 Praekelt Foundation <dev@praekeltfoundation.org>
# BSD - see LICENSE for details

"""Exception classes for SSMI."""


class SSMIError(Exception):
    """Base exception class for the ssmi library."""


class SSMIRemoteServerError(SSMIError):
    """Bad behaviour detected from remote SSMI server."""
