"""Compatibility shim for api package."""

from csip.api.server import app
from csip.api.client import InferenceMonitoringClient

__all__ = ["app", "InferenceMonitoringClient"]
