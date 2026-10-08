"""
NeuroSync Protocol Python SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A client library for interacting with the NeuroSync DeSci Oracle and Gas Master Relayer.
"""

from .client import NeuroSyncClient, SleepMetricSubmission, ProofResult

__version__ = "0.1.0"
__all__ = ["NeuroSyncClient", "SleepMetricSubmission", "ProofResult"]
