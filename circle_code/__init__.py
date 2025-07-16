"""
Circle Code System - A circular alternative to QR codes
"""

from .core import (
    CircleCodeStandard,
    CircleCodeEncoder,
    CircleCodeDecoder,
    CircleCodeGenerator,
    create_circle_code,
    decode_circle_code
)

__version__ = "1.0.0"
__author__ = "Circle Code Team"

__all__ = [
    "CircleCodeStandard",
    "CircleCodeEncoder", 
    "CircleCodeDecoder",
    "CircleCodeGenerator",
    "create_circle_code",
    "decode_circle_code"
] 