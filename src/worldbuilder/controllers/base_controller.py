"""Base controller class for MVC pattern."""
from abc import ABC
from PyQt6.QtCore import QObject


class BaseController(QObject):
    """Base controller class implementing MVC pattern."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view = None
        self._model = None
    
    @property
    def view(self):
        """Get associated view."""
        return self._view
    
    @view.setter
    def view(self, view):
        """Set associated view."""
        self._view = view
    
    @property
    def model(self):
        """Get associated model/service."""
        return self._model
    
    @model.setter
    def model(self, model):
        """Set associated model/service."""
        self._model = model
