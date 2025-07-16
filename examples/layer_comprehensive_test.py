#!/usr/bin/env python3
"""
Comprehensive Layer Test for Circle Code System
Encodes and decodes the same Bitcoin address using all 10 layers.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circle_code import CircleCodeGenerator

BITCOIN_ADDRESS = "bitcoin://bc1qg7spg4yyjh8w6sscd506g7dgzayyjtqdam8858"


def test_all_layers(data):
    print("🔵 Circle Code Comprehensive Layer Test")
    print("=" * 50)
    print(f"Test data: {data}")
    print()
    results = []
    for layer in range(1, 11):
        print(f"Layer {layer}:")
        filename = f"examples/layer_test_layer{layer}.png"
        try:
            generator = CircleCodeGenerator(layers=layer)
            generator.generate(data, output_path=filename, size=512)
            print(f"  ✅ Encoded to {filename}")
            decoded = generator.decode(filename)
            if decoded == data:
                print(f"  ✅ Decoded successfully and matches original!")
                results.append((layer, True))
            else:
                print(f"  ❌ Decoded but does NOT match original!")
                print(f"     Decoded: {decoded}")
                results.append((layer, False))
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append((layer, False))
        print()
    print("Summary:")
    for layer, success in results:
        print(f"  Layer {layer}: {'PASS' if success else 'FAIL'}")
    print("\nDone.")

if __name__ == "__main__":
    test_all_layers(BITCOIN_ADDRESS) 