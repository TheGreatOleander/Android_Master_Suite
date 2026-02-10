#!/usr/bin/env python3
"""
Example 1: Basic Kernel Extraction and Analysis

This example demonstrates the basic workflow of:
1. Extracting a boot image
2. Analyzing the kernel
3. Generating a report

Part of XDA Master Toolkit - KernelForge
"""

import sys
import os

# Add parent directory to path to import kernel_forge
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kernel_forge import KernelForge
import json


def main():
    """Basic kernel extraction and analysis example"""
    
    print("=" * 70)
    print("Example 1: Basic Kernel Extraction and Analysis")
    print("=" * 70)
    print()
    
    # Check for boot image argument
    if len(sys.argv) < 2:
        print("Usage: python example_basic.py <boot.img>")
        print()
        print("Example:")
        print("  python example_basic.py boot.img")
        print("  python example_basic.py /path/to/recovery.img")
        sys.exit(1)
    
    boot_image_path = sys.argv[1]
    
    # Verify file exists
    if not os.path.exists(boot_image_path):
        print(f"❌ Error: Boot image not found: {boot_image_path}")
        sys.exit(1)
    
    print(f"📱 Boot Image: {boot_image_path}")
    print(f"📁 Size: {os.path.getsize(boot_image_path):,} bytes")
    print()
    
    # Initialize KernelForge
    print("🔧 Initializing KernelForge...")
    forge = KernelForge(working_dir="example_workspace")
    print("✅ KernelForge initialized")
    print()
    
    # Step 1: Extract boot image
    print("=" * 70)
    print("STEP 1: Extracting Boot Image")
    print("=" * 70)
    print()
    
    try:
        extraction_info = forge.extract_boot_image(boot_image_path)
        print()
        print("✅ Extraction successful!")
        print()
        
        # Display extracted components
        print("📦 Extracted Components:")
        for component, path in extraction_info.get('components', {}).items():
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"  - {component:15} {path}")
                print(f"    {'':15} Size: {size:,} bytes")
        print()
        
        # Display boot configuration
        if 'boot_config' in extraction_info:
            print("⚙️  Boot Configuration:")
            for key, value in extraction_info['boot_config'].items():
                print(f"  - {key:15} {value}")
            print()
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 2: Analyze kernel
    print("=" * 70)
    print("STEP 2: Analyzing Kernel")
    print("=" * 70)
    print()
    
    kernel_path = extraction_info['components'].get('kernel')
    if not kernel_path:
        print("❌ No kernel found in extraction")
        sys.exit(1)
    
    try:
        kernel_analysis = forge.analyze_kernel(kernel_path)
        print()
        print("✅ Analysis complete!")
        print()
        
        # Display key information
        print("🔍 Kernel Information:")
        if 'kernel_version' in kernel_analysis:
            print(f"  - Version:      {kernel_analysis['kernel_version']}")
        if 'architecture' in kernel_analysis:
            print(f"  - Architecture: {kernel_analysis['architecture']}")
        if 'compression' in kernel_analysis:
            print(f"  - Compression:  {kernel_analysis['compression']}")
        print(f"  - Size:         {kernel_analysis.get('size', 0):,} bytes")
        print(f"  - SHA256:       {kernel_analysis.get('sha256', '')[:16]}...")
        print()
        
        # Display security features
        if 'security_features' in kernel_analysis:
            print("🛡️  Security Features:")
            for feature, enabled in kernel_analysis['security_features'].items():
                status = "✅ Enabled " if enabled else "❌ Disabled"
                print(f"  - {feature.upper():15} {status}")
            print()
        
        # Display config features
        if 'config_features' in kernel_analysis:
            print("⚙️  Configuration Features:")
            for category, features in kernel_analysis['config_features'].items():
                if features:
                    print(f"  {category.title()}:")
                    for feature in features[:3]:  # Show first 3
                        print(f"    - {feature}")
                    if len(features) > 3:
                        print(f"    ... and {len(features) - 3} more")
            print()
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 3: Generate report
    print("=" * 70)
    print("STEP 3: Generating Report")
    print("=" * 70)
    print()
    
    try:
        report_path = forge.generate_report(
            kernel_analysis,
            "example_workspace/output/kernel_report.md"
        )
        print("✅ Report generated successfully!")
        print()
        print(f"📄 Report Location: {report_path}")
        print()
        
        # Display sample of report
        with open(report_path, 'r') as f:
            lines = f.readlines()
            print("📋 Report Preview (first 20 lines):")
            print("-" * 70)
            for line in lines[:20]:
                print(line.rstrip())
            if len(lines) > 20:
                print(f"... and {len(lines) - 20} more lines")
            print("-" * 70)
        print()
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("✅ Extraction: Success")
    print("✅ Analysis:   Success")
    print("✅ Report:     Success")
    print()
    print("📁 All files saved to: example_workspace/")
    print()
    print("Next steps:")
    print("  1. Review the generated report")
    print("  2. Examine extracted components")
    print("  3. Try example_analysis.py for advanced analysis")
    print("  4. Try example_repack.py to repack the boot image")
    print()
    print("🎉 Example complete!")


if __name__ == '__main__':
    main()
