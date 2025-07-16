#!/usr/bin/env python3
"""
Basic usage example for Circle Code system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circle_code import create_circle_code, decode_circle_code, CircleCodeGenerator
import cv2
import numpy as np


def main():
    """Demonstrate basic Circle Code functionality"""
    
    print("🔵 Circle Code System Demo")
    print("=" * 50)
    
    # Test data
    test_data = "Hello Circle Code! This is a test message."
    
    print(f"📝 Original data: {test_data}")
    print(f"📊 Data size: {len(test_data)} characters")
    
    # Create Circle Code with different layers
    print("\n🔄 Generating Circle Codes...")
    
    # Layer 1 (smallest capacity)
    print("\n📱 Layer 1 Circle Code (16 bytes capacity):")
    try:
        code_1 = create_circle_code(
            data="Short msg", 
            layers=1, 
            size=256,
            output_path="examples/circle_code_layer1.png"
        )
        print("✅ Layer 1 code generated successfully")
    except Exception as e:
        print(f"❌ Layer 1 failed: {e}")
    
    # Layer 2
    print("\n📱 Layer 2 Circle Code (64 bytes capacity):")
    try:
        code_2 = create_circle_code(
            data=test_data, 
            layers=2, 
            size=256,
            output_path="examples/circle_code_layer2.png"
        )
        print("✅ Layer 2 code generated successfully")
    except Exception as e:
        print(f"❌ Layer 2 failed: {e}")
    
    # Layer 3 (default)
    print("\n📱 Layer 3 Circle Code (256 bytes capacity):")
    try:
        code_3 = create_circle_code(
            data=test_data, 
            layers=3, 
            size=512,
            output_path="examples/circle_code_layer3.png"
        )
        print("✅ Layer 3 code generated successfully")
    except Exception as e:
        print(f"❌ Layer 3 failed: {e}")
    
    # Layer 4
    print("\n📱 Layer 4 Circle Code (1024 bytes capacity):")
    try:
        code_4 = create_circle_code(
            data=test_data * 10,  # More data
            layers=4, 
            size=512,
            output_path="examples/circle_code_layer4.png"
        )
        print("✅ Layer 4 code generated successfully")
    except Exception as e:
        print(f"❌ Layer 4 failed: {e}")
    
    # Layer 5 (largest capacity)
    print("\n📱 Layer 5 Circle Code (4096 bytes capacity):")
    try:
        large_data = test_data * 50  # Much more data
        code_5 = create_circle_code(
            data=large_data, 
            layers=5, 
            size=512,
            output_path="examples/circle_code_layer5.png"
        )
        print("✅ Layer 5 code generated successfully")
    except Exception as e:
        print(f"❌ Layer 5 failed: {e}")
    
    # Test decoding
    print("\n🔍 Testing decoding...")
    try:
        decoded_data = decode_circle_code("examples/circle_code_layer3.png")
        print(f"✅ Decoded data: {decoded_data}")
        print(f"✅ Decoding successful: {decoded_data == test_data}")
    except Exception as e:
        print(f"❌ Decoding failed: {e}")
    
    print("\n🎉 Demo completed!")
    print("📁 Generated files saved in 'examples/' directory")


if __name__ == "__main__":
    main() 