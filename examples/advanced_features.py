#!/usr/bin/env python3
"""
Advanced features example for Circle Code system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circle_code import CircleCodeGenerator, CircleCodeStandard
import cv2
import numpy as np
import json
import base64
import time


def demo_error_correction():
    """Demonstrate error correction capabilities"""
    print("\n🛡️ Error Correction Demo")
    print("-" * 30)
    
    # Test data
    test_data = "This message has error correction!"
    
    # Create codes with different error correction levels
    error_levels = ['L', 'M', 'Q', 'H']
    
    for level in error_levels:
        print(f"\n📊 Error Correction Level: {level}")
        generator = CircleCodeGenerator(layers=3, error_correction=level)
        
        try:
            code = generator.generate(
                data=test_data,
                output_path=f"examples/circle_code_error_{level}.png",
                size=512
            )
            print(f"✅ Generated with {level} error correction")
        except Exception as e:
            print(f"❌ Failed: {e}")


def demo_data_types():
    """Demonstrate encoding different types of data"""
    print("\n📦 Data Types Demo")
    print("-" * 20)
    
    generator = CircleCodeGenerator(layers=4)
    
    # URL
    url_data = "https://github.com/circlecode/circlecode"
    print(f"\n🌐 URL: {url_data}")
    try:
        generator.generate(
            data=url_data,
            output_path="examples/circle_code_url.png",
            size=512
        )
        print("✅ URL encoded successfully")
    except Exception as e:
        print(f"❌ URL encoding failed: {e}")
    
    # JSON data
    json_data = {
        "name": "Circle Code",
        "version": "1.0.0",
        "features": ["circular", "layered", "scannable"],
        "timestamp": time.time()
    }
    json_string = json.dumps(json_data)
    print(f"\n📋 JSON: {json_string[:50]}...")
    try:
        generator.generate(
            data=json_string,
            output_path="examples/circle_code_json.png",
            size=512
        )
        print("✅ JSON encoded successfully")
    except Exception as e:
        print(f"❌ JSON encoding failed: {e}")
    
    # Base64 encoded data
    binary_data = b"Circle Code binary data example"
    base64_data = base64.b64encode(binary_data).decode('utf-8')
    print(f"\n🔢 Base64: {base64_data[:30]}...")
    try:
        generator.generate(
            data=base64_data,
            output_path="examples/circle_code_base64.png",
            size=512
        )
        print("✅ Base64 encoded successfully")
    except Exception as e:
        print(f"❌ Base64 encoding failed: {e}")


def demo_camera_integration():
    """Demonstrate camera integration for scanning"""
    print("\n📷 Camera Integration Demo")
    print("-" * 30)
    
    print("This demo shows how to integrate with camera for scanning.")
    print("Press 'q' to quit, 's' to scan current frame")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open camera")
        return
    
    decoder = CircleCodeGenerator().decoder
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break
        
        # Display frame
        cv2.imshow('Circle Code Scanner', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Try to decode current frame
            try:
                decoded_data = decoder.decode_data(frame)
                print(f"✅ Scanned data: {decoded_data}")
            except Exception as e:
                print(f"❌ Scan failed: {e}")
    
    cap.release()
    cv2.destroyAllWindows()


def demo_capacity_analysis():
    """Analyze data capacity for different configurations"""
    print("\n📊 Capacity Analysis")
    print("-" * 20)
    
    specs = CircleCodeStandard.LAYER_SPECS
    
    print("Layer | Radius | Segments | Capacity (bytes) | Sample Text")
    print("-" * 65)
    
    for layer, (radius, segments, capacity) in specs.items():
        # Calculate sample text length
        sample_length = capacity // 2  # Rough estimate for UTF-8
        sample_text = "A" * sample_length
        
        print(f"  {layer}  |   {radius:3d}  |    {segments:2d}   |      {capacity:4d}      | {sample_text[:20]}...")


def demo_visualization():
    """Create visual comparison of different Circle Codes"""
    print("\n🎨 Visualization Demo")
    print("-" * 20)
    
    # Create a comparison image
    test_data = "Circle Code Demo"
    
    # Generate codes with different layers
    codes = []
    for layer in range(1, 6):
        try:
            generator = CircleCodeGenerator(layers=layer)
            code = generator.generate(data=test_data, size=200)
            codes.append((f"Layer {layer}", code))
        except Exception as e:
            print(f"❌ Layer {layer} failed: {e}")
    
    # Create comparison image
    if codes:
        # Calculate grid size
        cols = 3
        rows = (len(codes) + cols - 1) // cols
        
        # Create canvas
        cell_size = 200
        canvas = np.ones((rows * cell_size, cols * cell_size), dtype=np.uint8) * 255
        
        # Place codes
        for i, (label, code) in enumerate(codes):
            row = i // cols
            col = i % cols
            
            y_start = row * cell_size
            x_start = col * cell_size
            
            # Resize code to fit cell
            resized_code = cv2.resize(code, (cell_size - 20, cell_size - 20))
            
            # Place in center of cell
            y_offset = (cell_size - resized_code.shape[0]) // 2
            x_offset = (cell_size - resized_code.shape[1]) // 2
            
            canvas[y_start + y_offset:y_start + y_offset + resized_code.shape[0],
                   x_start + x_offset:x_start + x_offset + resized_code.shape[1]] = resized_code
        
        # Save comparison
        cv2.imwrite("examples/circle_code_comparison.png", canvas)
        print("✅ Comparison image saved as 'circle_code_comparison.png'")


def main():
    """Run all advanced demos"""
    print("🔵 Circle Code Advanced Features Demo")
    print("=" * 50)
    
    # Create examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    # Run demos
    demo_capacity_analysis()
    demo_error_correction()
    demo_data_types()
    demo_visualization()
    
    # Ask if user wants to try camera demo
    print("\n📷 Would you like to try the camera scanning demo? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            demo_camera_integration()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted")
    
    print("\n🎉 Advanced demo completed!")
    print("📁 Check the 'examples/' directory for generated files")


if __name__ == "__main__":
    main() 