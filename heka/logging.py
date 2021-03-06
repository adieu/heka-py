# ***** BEGIN LICENSE BLOCK *****
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Rob Miller (rmiller@mozilla.com)
#   Victor Ng (vng@mozilla.com)
#
# ***** END LICENSE BLOCK *****
from __future__ import absolute_import
import logging

from heka.client import SEVERITY


class HekaHandler(logging.Handler):
    def __init__(self, heka_client):
        logging.Handler.__init__(self)
        self.heka_client = heka_client

    def emit(self, record):
        if record.levelno == logging.DEBUG:
            severity = SEVERITY.DEBUG
        elif record.levelno == logging.INFO:
            severity = SEVERITY.INFORMATIONAL
        elif record.levelno == logging.WARNING:
            severity = SEVERITY.WARNING
        elif record.levelno == logging.ERROR:
            severity = SEVERITY.ERROR
        else:  # critical
            severity = SEVERITY.CRITICAL

        self.heka_client.heka(type='oldstyle', severity=severity,
                                  payload=record.msg)


def hook_logger(logger_name, client):
    """
    Used to hook heka into the Python stdlib logging framework. Registers a
    logging module handler that delegates to a HekaClient for actual message
    delivery.

    :param name: Name of the stdlib logging `logger` object for which the
                 handler should be registered.
    :param client: HekaClient instance that the registered handler will use
                   for actual message delivery.
    """
    logger = logging.getLogger(logger_name)
    # first check to see if we're already registered
    for existing in logger.handlers:
        if (isinstance(existing, HekaHandler) and
            existing.heka_client is client):
            # already done, do nothing
            return
    logger.addHandler(HekaHandler(client))
