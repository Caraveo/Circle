#!/usr/bin/env python3
"""
Data Types Demo - Show all types of data that can be encoded in Circle Codes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circle_code import CircleCodeGenerator, CircleCodeStandard
import json
import base64
import pickle
import hashlib
import time
import cv2
import numpy as np


def demo_text_data():
    """Demonstrate encoding different types of text data"""
    print("\n📝 Text Data Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=4)
    
    # Simple text
    simple_text = "Hello Circle Code World!"
    print(f"📄 Simple Text: {simple_text}")
    generator.generate(simple_text, "examples/text_simple.png", 512)
    
    # Long text
    long_text = "This is a much longer text that demonstrates the capacity of Circle Codes. " * 5
    print(f"📄 Long Text: {len(long_text)} characters")
    generator.generate(long_text, "examples/text_long.png", 512)
    
    # Multi-language text
    multilingual = "Hello 世界! Bonjour le monde! ¡Hola mundo! Привет мир!"
    print(f"🌍 Multi-language: {multilingual}")
    generator.generate(multilingual, "examples/text_multilingual.png", 512)


def demo_json_data():
    """Demonstrate encoding JSON data structures"""
    print("\n📋 JSON Data Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=5)
    
    # Contact information
    contact_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-123-4567",
        "company": "Circle Code Inc.",
        "website": "https://circlecode.dev",
        "address": {
            "street": "123 Innovation Ave",
            "city": "Tech City",
            "state": "CA",
            "zip": "90210"
        }
    }
    print(f"👤 Contact Info: {contact_info['name']} - {contact_info['email']}")
    generator.generate(json.dumps(contact_info), "examples/json_contact.png", 512)
    
    # Product information
    product_info = {
        "id": "CC-001",
        "name": "Circle Code Generator",
        "version": "1.0.0",
        "features": ["circular", "layered", "scannable", "rotation-invariant"],
        "specs": {
            "max_layers": 10,
            "max_capacity": "128KB",
            "error_correction": ["L", "M", "Q", "H"]
        },
        "price": 99.99,
        "in_stock": True
    }
    print(f"📦 Product Info: {product_info['name']} v{product_info['version']}")
    generator.generate(json.dumps(product_info), "examples/json_product.png", 512)


def demo_binary_data():
    """Demonstrate encoding binary data"""
    print("\n🔢 Binary Data Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=6)
    
    # Binary data as base64
    binary_data = b"This is binary data that can contain any bytes including \x00\x01\x02\x03"
    base64_data = base64.b64encode(binary_data).decode('utf-8')
    print(f"🔢 Binary (Base64): {len(binary_data)} bytes -> {len(base64_data)} chars")
    generator.generate(base64_data, "examples/binary_base64.png", 512)
    
    # Hash data
    hash_data = hashlib.sha256(b"Circle Code is awesome!").hexdigest()
    print(f"🔐 Hash: {hash_data}")
    generator.generate(hash_data, "examples/binary_hash.png", 512)


def demo_urls_and_links():
    """Demonstrate encoding URLs and web links"""
    print("\n🌐 URL and Link Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=3)
    
    # Simple URL
    url = "https://github.com/circlecode/circlecode"
    print(f"🌐 URL: {url}")
    generator.generate(url, "examples/url_simple.png", 512)
    
    # URL with parameters
    url_with_params = "https://circlecode.dev/generate?data=hello&layers=5&size=512"
    print(f"🌐 URL with params: {url_with_params}")
    generator.generate(url_with_params, "examples/url_params.png", 512)
    
    # WiFi credentials
    wifi_config = {
        "ssid": "CircleCode_WiFi",
        "password": "SecurePassword123!",
        "security": "WPA2",
        "hidden": False
    }
    wifi_string = f"WIFI:S:{wifi_config['ssid']};T:{wifi_config['security']};P:{wifi_config['password']};;"
    print(f"📶 WiFi: {wifi_config['ssid']}")
    generator.generate(wifi_string, "examples/wifi_config.png", 512)


def demo_structured_data():
    """Demonstrate encoding structured data formats"""
    print("\n📊 Structured Data Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=7)
    
    # CSV-like data
    csv_data = "name,age,city\nJohn,30,New York\nJane,25,Los Angeles\nBob,35,Chicago"
    print(f"📊 CSV Data: {len(csv_data.split('\n'))} rows")
    generator.generate(csv_data, "examples/structured_csv.png", 512)
    
    # XML-like data
    xml_data = """<person>
<name>Alice</name>
<age>28</age>
<skills>
<skill>Python</skill>
<skill>Circle Codes</skill>
<skill>Computer Vision</skill>
</skills>
</person>"""
    print(f"📄 XML Data: {len(xml_data)} characters")
    generator.generate(xml_data, "examples/structured_xml.png", 512)


def demo_application_data():
    """Demonstrate encoding application-specific data"""
    print("\n📱 Application Data Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=5)
    
    # Calendar event
    calendar_event = {
        "type": "calendar_event",
        "title": "Circle Code Launch",
        "description": "Launch of the revolutionary Circle Code system",
        "start": "2024-01-15T10:00:00Z",
        "end": "2024-01-15T11:00:00Z",
        "location": "Virtual Event",
        "organizer": "Circle Code Team"
    }
    print(f"📅 Calendar Event: {calendar_event['title']}")
    generator.generate(json.dumps(calendar_event), "examples/app_calendar.png", 512)
    
    # Payment information
    payment_info = {
        "type": "payment_request",
        "amount": 29.99,
        "currency": "USD",
        "description": "Circle Code Pro License",
        "merchant": "Circle Code Inc.",
        "reference": "CC-2024-001"
    }
    print(f"💳 Payment: ${payment_info['amount']} {payment_info['currency']}")
    generator.generate(json.dumps(payment_info), "examples/app_payment.png", 512)


def demo_large_data():
    """Demonstrate encoding large amounts of data"""
    print("\n📈 Large Data Examples")
    print("-" * 30)
    
    # Test with maximum capacity
    max_capacity = CircleCodeStandard.LAYER_SPECS[10][2]  # 10 layers
    print(f"📈 Maximum capacity (10 layers): {max_capacity} bytes")
    
    # Generate large text
    large_text = "Circle Code is amazing! " * (max_capacity // 25)  # Approximate
    print(f"📄 Large text: {len(large_text)} characters")
    
    generator = CircleCodeGenerator(layers=10)
    try:
        generator.generate(large_text, "examples/data_large.png", 512)
        print("✅ Large data encoded successfully!")
    except Exception as e:
        print(f"❌ Large data failed: {e}")


def demo_encoded_formats():
    """Demonstrate encoding data in different formats"""
    print("\n🔧 Encoded Format Examples")
    print("-" * 30)
    
    generator = CircleCodeGenerator(layers=4)
    
    # Pickle-encoded Python object
    python_object = {
        "function": "lambda x: x**2",
        "data": [1, 2, 3, 4, 5],
        "metadata": {"created": time.time()}
    }
    pickle_data = base64.b64encode(pickle.dumps(python_object)).decode('utf-8')
    print(f"🐍 Pickle data: {len(pickle_data)} characters")
    generator.generate(pickle_data, "examples/format_pickle.png", 512)
    
    # Compressed data
    import zlib
    original_data = "This is some data that will be compressed using zlib compression algorithm. " * 10
    compressed_data = base64.b64encode(zlib.compress(original_data.encode())).decode('utf-8')
    print(f"🗜️ Compressed data: {len(original_data)} -> {len(compressed_data)} characters")
    generator.generate(compressed_data, "examples/format_compressed.png", 512)


def main():
    """Run all data type demonstrations"""
    print("🔵 Circle Code - Data Types Demo")
    print("=" * 50)
    print("This demo shows all the different types of data you can encode!")
    
    # Create examples directory
    os.makedirs("examples", exist_ok=True)
    
    # Run all demos
    demo_text_data()
    demo_json_data()
    demo_binary_data()
    demo_urls_and_links()
    demo_structured_data()
    demo_application_data()
    demo_encoded_formats()
    demo_large_data()
    
    print("\n🎉 Data Types Demo Completed!")
    print("📁 Check the 'examples/' directory for all generated Circle Codes")
    print("\n💡 You can encode ANY type of data:")
    print("   • Text (any language)")
    print("   • JSON objects")
    print("   • Binary data (Base64)")
    print("   • URLs and links")
    print("   • WiFi credentials")
    print("   • Contact information")
    print("   • Calendar events")
    print("   • Payment information")
    print("   • Structured data (CSV, XML)")
    print("   • Compressed data")
    print("   • Pickled Python objects")
    print("   • And much more!")


if __name__ == "__main__":
    main() 