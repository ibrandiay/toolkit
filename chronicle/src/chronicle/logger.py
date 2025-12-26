"""
A lightweight wrapper around Rerun for structured logging of events, metrics, and data streams.
@Author: Ibra Ndiaye
"""

import rerun as rr
import numpy as np
from typing import Optional, Dict, Any, Union, List
import contextlib
import json

class Logger:
    """
    A lightweight wrapper around Rerun for structured logging of events, metrics, and data streams.
    """
    
    def __init__(self, application_id: str, entity_prefix: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Chronicle Logger.

        Args:
            application_id: Unique identifier for the application
            entity_prefix: Optional prefix for all entity paths (e.g. "experiment_01")
            config: Configuration dictionary. 
                    - spawn_viewer (bool): Whether to spawn the Rerun viewer. Default True.
                    - save_path (str): Path to save logs. Default None.
        """
        self.application_id = application_id
        self.entity_prefix = entity_prefix or ""
        self.config = config or {}
        
        spawn = self.config.get("spawn_viewer", True)
        save_path = self.config.get("save_path")
        
        rr.init(application_id, spawn=spawn)
        
        if save_path:
            rr.save(save_path)

    def _get_path(self, path: str) -> str:
        if self.entity_prefix:
            # Handle cases where path might already be prefixed or user passes simple name
            return f"{self.entity_prefix}/{path}".strip("/")
        return path

    def info(self, message: str):
        """Log an informational message."""
        rr.log(self._get_path("logs/info"), rr.TextLog(message, level="INFO"))

    def warning(self, message: str):
        """Log a warning message."""
        rr.log(self._get_path("logs/warning"), rr.TextLog(message, level="WARN"))

    def debug(self, message: str):
        """Log a debug message."""
        rr.log(self._get_path("logs/debug"), rr.TextLog(message, level="DEBUG"))
    
    def error(self, message: str):
        """Log an error message."""
        rr.log(self._get_path("logs/error"), rr.TextLog(message, level="ERROR"))

    def critical(self, message: str):
        """Log a critical issue."""
        rr.log(self._get_path("logs/critical"), rr.TextLog(message, level="CRITICAL"))

    def log_scalar(self, path: str, value: float, step: Optional[int] = None):
        """
        Log a numerical scalar value.
        
        Args:
            path: Entity path for the metric
            value: The numerical value
            step: Optional step number to set on the 'step' timeline
        """
        if step is not None:
             rr.set_time(timeline="step", sequence=step)
        
        rr.log(self._get_path(path), rr.Scalars(value))

    def log_image(self, path: str, image: Any):
        """
        Log an image.
        
        Args:
            path: Entity path for the image
            image: Image data (numpy array, tensor, etc.)
        """
        rr.log(self._get_path(path), rr.Image(image))

    def log_dict(self, path: str, dictionary: Dict[str, Any]):
        """
        Log a dictionary as structured data (TextDocument).
        """
        try:
            content = json.dumps(dictionary, indent=2, default=str)
        except Exception:
            content = str(dictionary)
        
        rr.log(self._get_path(path), rr.TextDocument(content, media_type="text/markdown"))

    def set_time_sequence(self, timeline: str, step: int):
        """Set the current time for a sequence timeline."""
        rr.set_time(timeline=timeline, sequence=step)

    def set_time_seconds(self, timeline: str, time: float):
        """Set the current time for a seconds-based timeline (timestamp)."""
        rr.set_time(timeline=timeline, timestamp=time)

    @contextlib.contextmanager
    def batch(self):
        """
        Context manager for batch logging. 
        Currently a placeholder for future batch optimizations.
        """
        yield

    @contextlib.contextmanager
    def context(self, path_prefix: str):
        """
        Context manager to temporarily append a prefix to all log paths.
        
        Usage:
            with logger.context("training/epoch_5"):
                logger.log_scalar("loss", 0.5) # Logs to "original_prefix/training/epoch_5/loss"
        """
        old_prefix = self.entity_prefix
        
        if self.entity_prefix:
            self.entity_prefix = f"{self.entity_prefix}/{path_prefix}"
        else:
            self.entity_prefix = path_prefix
            
        try:
            yield
        finally:
            self.entity_prefix = old_prefix
