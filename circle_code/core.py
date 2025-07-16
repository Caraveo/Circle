"""
Circle Code System - A circular alternative to QR codes
Uses concentric circles, lines, and dots to encode data
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw
import math
import hashlib
from typing import List, Tuple, Optional, Dict
import json
import base64
import zlib
import time


class CircleCodeStandard:
    """Defines the standard specifications for Circle Codes"""
    
    # Layer configurations: (radius, segments, data_capacity_bytes)
    LAYER_SPECS = {
        1: (50, 8, 16),        # 1 layer: 50px radius, 8 segments, 16 bytes
        2: (75, 12, 64),       # 2 layers: 75px radius, 12 segments, 64 bytes  
        3: (100, 16, 256),     # 3 layers: 100px radius, 16 segments, 256 bytes
        4: (125, 20, 1024),    # 4 layers: 125px radius, 20 segments, 1024 bytes
        5: (150, 24, 4096),    # 5 layers: 150px radius, 24 segments, 4096 bytes
        6: (175, 28, 8192),    # 6 layers: 175px radius, 28 segments, 8192 bytes
        7: (200, 32, 16384),   # 7 layers: 200px radius, 32 segments, 16384 bytes
        8: (225, 36, 32768),   # 8 layers: 225px radius, 36 segments, 32768 bytes
        9: (250, 40, 65536),   # 9 layers: 250px radius, 40 segments, 65536 bytes
        10: (275, 44, 131072), # 10 layers: 275px radius, 44 segments, 131072 bytes
    }
    
    # Error correction levels
    ERROR_CORRECTION = {
        'L': 0.07,  # 7% recovery
        'M': 0.15,  # 15% recovery
        'Q': 0.25,  # 25% recovery
        'H': 0.30,  # 30% recovery
    }
    
    # Color scheme
    COLORS = {
        'background': (255, 255, 255),  # White
        'foreground': (0, 0, 0),        # Black
        'accent': (128, 128, 128),      # Gray for alignment
    }


class CircleCodeEncoder:
    """Encodes data into Circle Code format"""
    
    def __init__(self, layers: int = 3, error_correction: str = 'M'):
        """
        Initialize encoder
        
        Args:
            layers: Number of concentric circles (1-5)
            error_correction: Error correction level ('L', 'M', 'Q', 'H')
        """
        if layers not in CircleCodeStandard.LAYER_SPECS:
            raise ValueError(f"Layers must be 1-5, got {layers}")
        if error_correction not in CircleCodeStandard.ERROR_CORRECTION:
            raise ValueError(f"Invalid error correction level: {error_correction}")
            
        self.layers = layers
        self.error_correction = error_correction
        self.radius, self.segments, self.max_data_bytes = CircleCodeStandard.LAYER_SPECS[layers]
        
    def encode_data(self, data: str) -> np.ndarray:
        """
        Encode data into Circle Code format
        
        Args:
            data: String data to encode
            
        Returns:
            numpy array representing the Circle Code
        """
        # Convert data to bytes
        data_bytes = data.encode('utf-8')
        
        # Check data size
        if len(data_bytes) > self.max_data_bytes:
            raise ValueError(f"Data too large. Max {self.max_data_bytes} bytes, got {len(data_bytes)}")
        
        # Add metadata and error correction
        encoded_data = self._prepare_data(data_bytes)
        
        # Print bit stream and bytes for debug
        data_bits = ''.join(format(byte, '08b') for byte in encoded_data)
        print(f"ENCODE bits: {data_bits[:128]} ... total {len(data_bits)} bits")
        print(f"ENCODE bytes: {[b for b in encoded_data[:16]]}")
        
        # Create the Circle Code matrix
        code_matrix = self._create_code_matrix(encoded_data)
        
        return code_matrix
    
    def _prepare_data(self, data_bytes: bytes) -> bytes:
        """Prepare data with metadata and error correction"""
        # Create metadata header
        metadata = {
            'version': 1,
            'layers': self.layers,
            'error_correction': self.error_correction,
            'data_length': len(data_bytes),
            'timestamp': int(time.time())
        }
        
        metadata_bytes = json.dumps(metadata).encode('utf-8')
        metadata_length = len(metadata_bytes).to_bytes(2, 'big')
        
        # Combine all data
        combined_data = metadata_length + metadata_bytes + data_bytes
        
        # Add padding to fill capacity
        padding_needed = self.max_data_bytes - len(combined_data)
        if padding_needed > 0:
            combined_data += b'\x00' * padding_needed
        
        # Add simple checksum
        checksum = hashlib.md5(combined_data).digest()[:4]
        combined_data += checksum
        
        return combined_data
    
    def _create_code_matrix(self, data: bytes) -> np.ndarray:
        upscale = 4
        matrix_size = ((self.radius * 2 + 20) * 2) * upscale
        matrix = np.zeros((matrix_size, matrix_size), dtype=np.uint8)
        center = matrix_size // 2
        dot_exclusion = int((self.radius + 18) * upscale)
        data_bits = ''.join(format(byte, '08b') for byte in data)
        dot_bits = data_bits[:4].ljust(4, '0')
        segment_bits = data_bits[4:]
        total_segments = 0
        for layer in range(self.layers):
            layer_segments = self.segments * (layer + 1) // self.layers
            if layer_segments in [8, 12, 16, 20, 24, 28, 32, 36, 40, 44]:
                total_segments += layer_segments - 4
            else:
                total_segments += layer_segments
        segment_bits = segment_bits[:total_segments].ljust(total_segments, '0')
        full_bits = dot_bits + segment_bits
        if len(full_bits) % 8 != 0:
            full_bits = full_bits.ljust((len(full_bits) + 7) // 8 * 8, '0')
        print(f"ENCODE bits: {full_bits[:128]} ... total {len(full_bits)} bits")
        print(f"ENCODE bytes: {[b for b in int(full_bits, 2).to_bytes(len(full_bits)//8, 'big')][:16]}")
        bit_index = 0
        for layer in range(self.layers):
            layer_radius = self.radius * (layer + 1) // self.layers * upscale
            if abs(layer_radius - dot_exclusion) < int(12 * upscale):
                continue
            layer_segments = self.segments * (layer + 1) // self.layers
            if layer_segments in [8, 12, 16, 20, 24, 28, 32, 36, 40, 44]:
                cardinal_indices = [0, layer_segments//4, layer_segments//2, 3*layer_segments//4]
            else:
                cardinal_indices = []
            for segment in range(layer_segments):
                if segment in cardinal_indices:
                    continue
                if bit_index < len(segment_bits):
                    start_angle = (2 * math.pi * segment) / layer_segments
                    end_angle = (2 * math.pi * (segment + 1)) / layer_segments
                    bit_value = int(segment_bits[bit_index])
                    self._draw_segment(matrix, center, layer_radius, start_angle, end_angle, bit_value, upscale, dot_exclusion)
                    bit_index += 1
        self._add_data_dots(matrix, center, upscale, dot_bits)
        cv2.circle(matrix, (center, center), int(10 * upscale), 255, -1, lineType=cv2.LINE_AA)
        final_size = (self.radius * 2 + 20) * 2
        matrix_small = cv2.resize(matrix, (final_size, final_size), interpolation=cv2.INTER_AREA)
        return matrix_small

    def _draw_segment(self, matrix: np.ndarray, center: int, radius: int, 
                     start_angle: float, end_angle: float, value: int, upscale: int = 1, dot_exclusion: int = 0):
        """Draw a thick, anti-aliased segment in the circle using polylines, avoiding dot overlap."""
        if value == 0:
            return
        # Avoid drawing inside dot exclusion radius
        if abs(radius - dot_exclusion) < int(12 * upscale):
            return
        num_points = max(12, int(32 * (end_angle - start_angle) / (2 * math.pi)))
        thickness = int(8 * upscale)
        # Shorten arc so it doesn't enter dot areas (leave a gap at cardinal points)
        gap_angle = math.radians(18)  # ~18 degree gap
        # For each segment, if it is at a cardinal direction, shrink the arc
        cardinal_angles = [0, math.pi/2, math.pi, 3*math.pi/2]
        for ca in cardinal_angles:
            if (start_angle < ca < end_angle) or (start_angle < ca+2*math.pi < end_angle):
                if end_angle - start_angle > 2*gap_angle:
                    start_angle += gap_angle
                    end_angle -= gap_angle
        points = []
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            x = int(center + radius * math.cos(angle))
            y = int(center + radius * math.sin(angle))
            points.append((x, y))
        points = np.array(points, dtype=np.int32)
        cv2.polylines(matrix, [points], isClosed=False, color=255, thickness=thickness, lineType=cv2.LINE_AA)

    def _add_data_dots(self, matrix: np.ndarray, center: int, upscale: int, dot_bits: str):
        """Draw four data dots (top, bottom, left, right) based on the first four bits of the data."""
        marker_radius_outer = int((self.radius + 10) * upscale)
        marker_radius_dot = int(10 * upscale)
        marker_positions = [
            (center, center - marker_radius_outer),  # Top
            (center, center + marker_radius_outer),  # Bottom
            (center - marker_radius_outer, center),  # Left
            (center + marker_radius_outer, center),  # Right
        ]
        for i, (x, y) in enumerate(marker_positions):
            if dot_bits[i] == '1' and 0 <= x < matrix.shape[1] and 0 <= y < matrix.shape[0]:
                cv2.circle(matrix, (x, y), marker_radius_dot, 255, -1, lineType=cv2.LINE_AA)


class CircleCodeDecoder:
    """Decodes Circle Code format back to data"""
    
    def __init__(self):
        self.standard = CircleCodeStandard()
    
    def decode_data(self, image: np.ndarray) -> str:
        """
        Decode Circle Code from image
        
        Args:
            image: numpy array of the Circle Code image
            
        Returns:
            Decoded string data
        """
        # Preprocess image
        processed_image = self._preprocess_image(image)
        
        # Detect circle and center
        center, detected_radius = self._detect_circle(processed_image)
        
        # Read the four data dots as the first four bits
        dot_bits = self._read_data_dots(processed_image, center, detected_radius)
        # Try all plausible (layers, segments) combinations
        for layers, (radius_val, segments, max_data_bytes) in CircleCodeStandard.LAYER_SPECS.items():
            # Use the maximum possible encoded length for this layer
            # 2 bytes for metadata length, 4 for checksum, 64 for metadata overhead
            total_bytes = max_data_bytes + 2 + 4 + 64
            total_bits_needed = total_bytes * 8
            all_bits = self._extract_data_bits(image, center, detected_radius, layers, segments)
            segment_bits = all_bits[4:]
            segment_bits = segment_bits[:total_bits_needed - 4].ljust(total_bits_needed - 4, '0')
            n = len(segment_bits)
            for shift in range(n):
                rotated_bits = segment_bits[shift:] + segment_bits[:shift]
                data_bits = dot_bits + rotated_bits
                if len(data_bits) % 8 != 0:
                    data_bits = data_bits.ljust((len(data_bits) + 7) // 8 * 8, '0')
                data_bytes = self._bits_to_bytes(data_bits)
                try:
                    self._parse_data(data_bytes)
                    return self._parse_data(data_bytes)
                except Exception:
                    continue
        # Fallback: try default extraction
        all_bits = self._extract_data_bits(image, center, detected_radius, 3, 16)
        segment_bits = all_bits[4:]
        total_bytes = 16 + 2 + 4 + 64
        total_bits_needed = total_bytes * 8
        segment_bits = segment_bits[:total_bits_needed - 4].ljust(total_bits_needed - 4, '0')
        full_bits = dot_bits + segment_bits
        if len(full_bits) % 8 != 0:
            full_bits = full_bits.ljust((len(full_bits) + 7) // 8 * 8, '0')
        data_bytes = self._bits_to_bytes(full_bits)
        return self._parse_data(data_bytes)

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better circle detection and decoding"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        # Apply threshold
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        return thresh

    def _detect_circle(self, image: np.ndarray) -> tuple:
        """Detect the main circle and its center using Hough Transform or fallback to image center."""
        circles = cv2.HoughCircles(
            image, cv2.HOUGH_GRADIENT, 1, 20,
            param1=50, param2=30, minRadius=20, maxRadius=200
        )
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            largest_circle = max(circles, key=lambda x: x[2])
            center_x, center_y, radius = largest_circle
            return (center_x, center_y), radius
        else:
            center = (image.shape[1] // 2, image.shape[0] // 2)
            radius = min(image.shape) // 4
            return center, radius

    def _extract_segment_bits_rotation_invariant(self, image: np.ndarray, center: tuple, radius: int) -> str:
        """Extract segment bits (excluding dots) and return as a bit string."""
        # Use default layers/segments for initial extraction
        default_layers = 3
        default_segments = 16
        bits = self._extract_data_bits(image, center, radius, default_layers, default_segments)
        # Remove the first four bits (reserved for dots)
        return bits[4:]

    def _extract_data_bits(self, image: np.ndarray, center: tuple, radius: int, layers: int, segments: int) -> str:
        """
        Extract data bits from circle segments using given layers and segments, skipping dot positions in each layer.
        """
        center_x, center_y = center
        data_bits = ""
        for layer in range(layers):
            layer_radius = radius * (layer + 1) // layers
            # Skip the four cardinal directions (dot positions)
            if segments in [8, 12, 16, 20, 24, 28, 32, 36, 40, 44]:
                cardinal_indices = [0, segments//4, segments//2, 3*segments//4]
            else:
                cardinal_indices = []
            for segment in range(segments):
                if segment in cardinal_indices:
                    continue
                angle = (2 * math.pi * segment) / segments
                sample_x = int(center_x + layer_radius * math.cos(angle))
                sample_y = int(center_y + layer_radius * math.sin(angle))
                if (0 <= sample_x < image.shape[1] and 0 <= sample_y < image.shape[0]):
                    pixel_value = image[sample_y, sample_x]
                    bit_value = '1' if pixel_value > 127 else '0'
                    data_bits += bit_value
        return data_bits
    
    def _bits_to_bytes(self, bits: str) -> bytes:
        """Convert bit string to bytes"""
        # Pad to multiple of 8
        while len(bits) % 8 != 0:
            bits += '0'
        
        # Convert to bytes
        bytes_list = []
        for i in range(0, len(bits), 8):
            byte_bits = bits[i:i+8]
            byte_value = int(byte_bits, 2)
            bytes_list.append(byte_value)
        
        return bytes(bytes_list)
    
    def _parse_data(self, data_bytes: bytes) -> str:
        """Parse metadata and extract original data"""
        try:
            # Extract metadata length
            metadata_length = int.from_bytes(data_bytes[:2], 'big')
            
            # Extract metadata
            metadata_bytes = data_bytes[2:2+metadata_length]
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            
            # Extract original data
            data_start = 2 + metadata_length
            data_length = metadata['data_length']
            original_data_bytes = data_bytes[data_start:data_start+data_length]
            
            # Verify checksum
            checksum_start = data_start + data_length
            expected_checksum = data_bytes[checksum_start:checksum_start+4]
            
            data_for_checksum = data_bytes[:checksum_start]
            actual_checksum = hashlib.md5(data_for_checksum).digest()[:4]
            
            if expected_checksum != actual_checksum:
                raise ValueError("Checksum verification failed")
            
            return original_data_bytes.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Failed to parse data: {e}")

    def _read_data_dots(self, image: np.ndarray, center: tuple, detected_radius: int) -> str:
        """Read the four data dots (top, bottom, left, right) as the first four bits, using detected radius."""
        upscale = 1  # Image is already downscaled
        center_x, center_y = center
        marker_radius_outer = int((detected_radius + 10) * upscale)
        marker_positions = [
            (center_x, center_y - marker_radius_outer),  # Top
            (center_x, center_y + marker_radius_outer),  # Bottom
            (center_x - marker_radius_outer, center_y),  # Left
            (center_x + marker_radius_outer, center_y),  # Right
        ]
        bits = ''
        for x, y in marker_positions:
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                region = image[max(0, y-2):y+3, max(0, x-2):x+3]
                mean_val = region.mean() if region.size > 0 else 0
                bits += '1' if mean_val > 127 else '0'
            else:
                bits += '0'
        return bits


class CircleCodeGenerator:
    """High-level interface for generating Circle Codes"""
    
    def __init__(self, layers: int = 3, error_correction: str = 'M'):
        self.encoder = CircleCodeEncoder(layers, error_correction)
        self.decoder = CircleCodeDecoder()
    
    def generate(self, data: str, output_path: str = None, 
                size: int = 512) -> np.ndarray:
        """
        Generate Circle Code from data
        
        Args:
            data: Data to encode
            output_path: Optional path to save the image
            size: Output image size
            
        Returns:
            numpy array of the Circle Code
        """
        # Encode data
        code_matrix = self.encoder.encode_data(data)
        
        # Resize to desired size
        resized = cv2.resize(code_matrix, (size, size), interpolation=cv2.INTER_NEAREST)
        
        # Save if path provided
        if output_path:
            cv2.imwrite(output_path, resized)
        
        return resized
    
    def decode(self, image_path: str) -> str:
        """
        Decode Circle Code from image file
        
        Args:
            image_path: Path to the Circle Code image
            
        Returns:
            Decoded data
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        return self.decoder.decode_data(image)


# Utility functions
def create_circle_code(data: str, layers: int = 3, size: int = 512, 
                      output_path: str = None) -> np.ndarray:
    """Convenience function to create Circle Code"""
    generator = CircleCodeGenerator(layers)
    return generator.generate(data, output_path, size)


def decode_circle_code(image_path: str) -> str:
    """Convenience function to decode Circle Code"""
    generator = CircleCodeGenerator()
    return generator.decode(image_path) 