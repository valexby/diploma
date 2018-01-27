#!/usr/bin/env python3

"""Utility methods for SQLAlchemy"""

import logging
log = logging.getLogger(__package__)

class no_autoflush(object):
    """Use session with autoflush off, used e.g. in
    olv control to prevent problems caused by flushing incomplete dbItems
    """
    def __init__(self, session):
        self.session = session
        self.autoflush = session.autoflush

    def __enter__(self):
        self.session.autoflush = False

    def __exit__(self, type, value, traceback):
        self.session.autoflush = self.autoflush
