# 🔵 Circle Code System

A revolutionary circular alternative to QR codes that uses concentric circles, lines, and dots to encode data. Unlike traditional square-based QR codes, Circle Codes offer a unique aesthetic and efficient data encoding system.

## 🌟 Features

- **Circular Design**: Beautiful circular patterns instead of square grids
- **Layered Architecture**: 1-5 layers for scalable data capacity
- **Error Correction**: Multiple error correction levels (L, M, Q, H)
- **Camera Integration**: Real-time scanning with webcam support
- **Multiple Data Types**: Support for text, URLs, JSON, and binary data
- **Production Ready**: Robust encoding/decoding with checksums
- **Cross-Platform**: Works on macOS, Linux, and Windows

## 📊 Data Capacity

| Layer | Radius | Segments | Capacity (bytes) | Sample Text Length |
|-------|--------|----------|------------------|-------------------|
| 1     | 50     | 8        | 16               | 8 chars           |
| 2     | 75     | 12       | 64               | 32 chars          |
| 3     | 100    | 16       | 256              | 128 chars         |
| 4     | 125    | 20       | 1024             | 512 chars         |
| 5     | 150    | 24       | 4096             | 2048 chars        |
| 6     | 175    | 28       | 8192             | 4096 chars        |
| 7     | 200    | 32       | 16384            | 8192 chars        |
| 8     | 225    | 36       | 32768            | 16384 chars       |
| 9     | 250    | 40       | 65536            | 32768 chars       |
| 10    | 275    | 44       | 131072           | 65536 chars       |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/circle-code.git
cd circle-code

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from circle_code import create_circle_code, decode_circle_code

# Generate a Circle Code
code = create_circle_code(
    data="Hello Circle Code!",
    layers=3,
    size=512,
    output_path="my_circle_code.png"
)

# Decode a Circle Code
decoded_data = decode_circle_code("my_circle_code.png")
print(decoded_data)  # "Hello Circle Code!"
```

### Command Line Interface

```bash
# Generate a Circle Code
python cli.py generate "Hello World" --layers 3 --output hello.png

# Decode a Circle Code
python cli.py decode hello.png

# Show system information
python cli.py info

# Interactive mode
python cli.py interactive
```

## 📖 Examples

### Basic Example

```python
#!/usr/bin/env python3
from circle_code import CircleCodeGenerator

# Create generator with 3 layers and medium error correction
generator = CircleCodeGenerator(layers=3, error_correction='M')

# Generate Circle Code
code = generator.generate(
    data="Welcome to the future of circular codes!",
    output_path="welcome.png",
    size=512
)

# Decode the code
decoded = generator.decode("welcome.png")
print(f"Decoded: {decoded}")
```

### Advanced Example

```python
#!/usr/bin/env python3
import json
from circle_code import CircleCodeGenerator

# Create generator with maximum capacity
generator = CircleCodeGenerator(layers=5, error_correction='H')

# Complex data structure
data = {
    "name": "Circle Code",
    "version": "1.0.0",
    "features": ["circular", "layered", "scannable"],
    "url": "https://github.com/circlecode/circlecode",
    "timestamp": 1234567890
}

# Generate code with JSON data
code = generator.generate(
    data=json.dumps(data),
    output_path="complex_data.png",
    size=512
)
```

## 🎯 Use Cases

- **Business Cards**: Elegant circular codes for contact information
- **Product Packaging**: Aesthetic codes for product details
- **Event Tickets**: Unique circular tickets
- **Digital Art**: Artistic data encoding
- **Mobile Apps**: Alternative to QR codes in apps
- **IoT Devices**: Compact circular identifiers

## 🔧 Technical Details

### Architecture

The Circle Code system uses:
- **Concentric Circles**: Multiple layers for data capacity
- **Segmented Encoding**: Angular segments for bit storage
- **Alignment Markers**: Cardinal direction markers for orientation
- **Error Correction**: Reed-Solomon-like error correction
- **Checksums**: MD5-based data integrity verification

### Error Correction Levels

- **L (Low)**: 7% data recovery
- **M (Medium)**: 15% data recovery (default)
- **Q (Quartile)**: 25% data recovery
- **H (High)**: 30% data recovery

### Color Scheme

- **Background**: White (255, 255, 255)
- **Foreground**: Black (0, 0, 0)
- **Alignment**: Gray (128, 128, 128)

## 📱 Camera Integration

```python
#!/usr/bin/env python3
import cv2
from circle_code import CircleCodeGenerator

# Initialize camera
cap = cv2.VideoCapture(0)
generator = CircleCodeGenerator()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display frame
    cv2.imshow('Circle Code Scanner', frame)
    
    # Try to decode (press 's' to scan)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        try:
            decoded = generator.decoder.decode_data(frame)
            print(f"Scanned: {decoded}")
        except Exception as e:
            print(f"Scan failed: {e}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 🧪 Testing

Run the example scripts to test the system:

```bash
# Basic functionality test
python examples/basic_usage.py

# Advanced features test
python examples/advanced_features.py
```

## 📁 Project Structure

```
circle-code/
├── circle_code/
│   ├── __init__.py
│   └── core.py              # Main implementation
├── examples/
│   ├── basic_usage.py       # Basic examples
│   └── advanced_features.py # Advanced features
├── cli.py                   # Command line interface
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by traditional QR codes but with a circular twist
- Built with modern Python libraries (OpenCV, NumPy, Pillow)
- Designed for production-ready applications

## 🔮 Future Enhancements

- [ ] Color Circle Codes
- [ ] Animated Circle Codes
- [ ] 3D Circle Codes
- [ ] Mobile SDKs (iOS/Android)
- [ ] Web-based generator
- [ ] Advanced error correction algorithms
- [ ] Custom styling options

---

**Circle Code System** - Where data meets elegance in perfect circles! 🔵 