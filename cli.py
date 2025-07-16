#!/usr/bin/env python3
"""
Command Line Interface for Circle Code System
"""

import argparse
import sys
import os
from circle_code import create_circle_code, decode_circle_code, CircleCodeGenerator, CircleCodeStandard


def generate_code(args):
    """Generate a Circle Code"""
    try:
        print(f"🔄 Generating Circle Code...")
        print(f"📝 Data: {args.data[:50]}{'...' if len(args.data) > 50 else ''}")
        print(f"📊 Layers: {args.layers}")
        print(f"🛡️ Error Correction: {args.error_correction}")
        print(f"📏 Size: {args.size}x{args.size}")
        
        # Check data size
        max_capacity = CircleCodeStandard.LAYER_SPECS[args.layers][2]
        data_size = len(args.data.encode('utf-8'))
        
        if data_size > max_capacity:
            print(f"⚠️  Warning: Data size ({data_size} bytes) exceeds capacity ({max_capacity} bytes)")
            print(f"   Consider using more layers or shorter data")
        
        # Generate code
        code = create_circle_code(
            data=args.data,
            layers=args.layers,
            size=args.size,
            output_path=args.output
        )
        
        print(f"✅ Circle Code generated successfully!")
        print(f"📁 Saved to: {args.output}")
        
        # Show file size
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"📦 File size: {file_size} bytes")
        
    except Exception as e:
        print(f"❌ Error generating Circle Code: {e}")
        sys.exit(1)


def decode_code(args):
    """Decode a Circle Code"""
    try:
        print(f"🔍 Decoding Circle Code...")
        print(f"📁 File: {args.input}")
        
        # Check if file exists
        if not os.path.exists(args.input):
            print(f"❌ File not found: {args.input}")
            sys.exit(1)
        
        # Decode
        decoded_data = decode_circle_code(args.input)
        
        print(f"✅ Decoded successfully!")
        print(f"📝 Data: {decoded_data}")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(decoded_data)
            print(f"📁 Decoded data saved to: {args.output}")
        
    except Exception as e:
        print(f"❌ Error decoding Circle Code: {e}")
        sys.exit(1)


def show_info(args):
    """Show system information and specifications"""
    print("🔵 Circle Code System Information")
    print("=" * 50)
    
    print(f"📦 Version: 1.0.0")
    print(f"🐍 Python: {sys.version}")
    
    print("\n📊 Layer Specifications:")
    print("Layer | Radius | Segments | Capacity (bytes) | Sample Text Length")
    print("-" * 70)
    
    specs = CircleCodeStandard.LAYER_SPECS
    for layer, (radius, segments, capacity) in specs.items():
        sample_length = capacity // 2  # Rough estimate for UTF-8
        print(f"  {layer}  |   {radius:3d}  |    {segments:2d}   |      {capacity:4d}      | {sample_length:3d} chars")
    
    print("\n🛡️ Error Correction Levels:")
    for level, recovery in CircleCodeStandard.ERROR_CORRECTION.items():
        print(f"  {level}: {recovery*100:.0f}% data recovery")
    
    print("\n🎨 Color Scheme:")
    for color_name, rgb in CircleCodeStandard.COLORS.items():
        print(f"  {color_name}: RGB{rgb}")


def interactive_mode(args):
    """Interactive mode for generating and testing Circle Codes"""
    print("🔵 Circle Code Interactive Mode")
    print("=" * 40)
    print("Type 'help' for commands, 'quit' to exit")
    
    while True:
        try:
            command = input("\n🔵 Circle Code> ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command.lower() == 'help':
                print("""
Available commands:
  generate <data> [options]  - Generate a Circle Code
  decode <file>              - Decode a Circle Code
  info                       - Show system information
  quit                       - Exit interactive mode
  
Generate options:
     --layers <1-10>            - Number of layers (default: 3)
  --error-correction <L|M|Q|H> - Error correction level (default: M)
  --size <pixels>            - Output size (default: 512)
  --output <file>            - Output file (default: circle_code.png)
                """)
            elif command.lower() == 'info':
                show_info(None)
            elif command.startswith('generate '):
                # Parse generate command
                parts = command.split()
                if len(parts) < 2:
                    print("❌ Usage: generate <data> [options]")
                    continue
                
                data = parts[1]
                layers = 3
                error_correction = 'M'
                size = 512
                output = 'circle_code.png'
                
                # Parse options
                i = 2
                while i < len(parts):
                    if parts[i] == '--layers' and i + 1 < len(parts):
                        layers = int(parts[i + 1])
                        i += 2
                    elif parts[i] == '--error-correction' and i + 1 < len(parts):
                        error_correction = parts[i + 1]
                        i += 2
                    elif parts[i] == '--size' and i + 1 < len(parts):
                        size = int(parts[i + 1])
                        i += 2
                    elif parts[i] == '--output' and i + 1 < len(parts):
                        output = parts[i + 1]
                        i += 2
                    else:
                        i += 1
                
                # Generate code
                try:
                    create_circle_code(data, layers, size, output)
                    print(f"✅ Generated: {output}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif command.startswith('decode '):
                # Parse decode command
                parts = command.split()
                if len(parts) < 2:
                    print("❌ Usage: decode <file>")
                    continue
                
                file_path = parts[1]
                try:
                    decoded = decode_circle_code(file_path)
                    print(f"✅ Decoded: {decoded}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Circle Code System - Generate and decode circular codes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate "Hello World" --layers 3 --output hello.png
  %(prog)s decode hello.png
  %(prog)s info
  %(prog)s interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a Circle Code')
    gen_parser.add_argument('data', help='Data to encode')
    gen_parser.add_argument('--layers', type=int, default=3, choices=range(1, 11),
                           help='Number of layers (1-10, default: 3)')
    gen_parser.add_argument('--error-correction', default='M', 
                           choices=['L', 'M', 'Q', 'H'],
                           help='Error correction level (default: M)')
    gen_parser.add_argument('--size', type=int, default=512,
                           help='Output image size in pixels (default: 512)')
    gen_parser.add_argument('--output', default='circle_code.png',
                           help='Output file path (default: circle_code.png)')
    gen_parser.set_defaults(func=generate_code)
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode a Circle Code')
    decode_parser.add_argument('input', help='Input image file')
    decode_parser.add_argument('--output', help='Output file for decoded data')
    decode_parser.set_defaults(func=decode_code)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show system information')
    info_parser.set_defaults(func=show_info)
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', 
                                              help='Start interactive mode')
    interactive_parser.set_defaults(func=interactive_mode)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main() 