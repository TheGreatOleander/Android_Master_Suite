#!/usr/bin/env python3
"""
Example 3: Boot Image Repacking

This example demonstrates:
1. Extracting a boot image
2. Modifying components (optional)
3. Repacking into a new boot image
4. Verifying the repacked image

Part of XDA Master Toolkit - KernelForge
"""

import sys
import os
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kernel_forge import KernelForge


def modify_kernel_cmdline(config_path: str, modifications: dict) -> bool:
    """
    Modify kernel command line in boot config
    
    Example modifications:
    - Add/remove androidboot parameters
    - Change console settings
    - Modify init parameters
    """
    try:
        # Read current config
        with open(config_path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                
                # Apply modifications
                if key == 'cmdline' and 'cmdline' in modifications:
                    new_cmdline = modifications['cmdline']
                    print(f"  ✏️  Modified cmdline")
                    print(f"      Old: {value.strip()[:60]}...")
                    print(f"      New: {new_cmdline[:60]}...")
                    new_lines.append(f"{key} = {new_cmdline}\n")
                elif key in modifications:
                    new_lines.append(f"{key} = {modifications[key]}\n")
                    print(f"  ✏️  Modified {key}: {modifications[key]}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Write modified config
        with open(config_path, 'w') as f:
            f.writelines(new_lines)
        
        return True
        
    except Exception as e:
        print(f"⚠️  Config modification failed: {e}")
        return False


def create_test_modifications(extract_dir: Path) -> dict:
    """
    Create example modifications to boot image components
    
    In practice, you would:
    - Replace kernel with custom-compiled version
    - Modify ramdisk init scripts
    - Update device tree
    - Change boot parameters
    """
    modifications = {}
    
    # Check what components we have
    kernel_path = extract_dir / "kernel"
    ramdisk_path = extract_dir / "ramdisk.img"
    config_path = extract_dir / "bootimg.cfg"
    
    if kernel_path.exists():
        # In real usage, you'd replace with your custom kernel
        # For this example, we'll just use the same kernel
        modifications['kernel'] = str(kernel_path)
        print(f"  ℹ️  Using extracted kernel (no modifications)")
    
    if ramdisk_path.exists():
        # In real usage, you'd modify ramdisk contents
        modifications['ramdisk'] = str(ramdisk_path)
        print(f"  ℹ️  Using extracted ramdisk (no modifications)")
    
    if config_path.exists():
        modifications['config'] = str(config_path)
        print(f"  ℹ️  Using extracted config")
    
    return modifications


def verify_boot_image(boot_path: str, forge: KernelForge) -> bool:
    """Verify repacked boot image"""
    try:
        print("🔍 Verifying repacked boot image...")
        
        # Extract and analyze
        verification = forge.extract_boot_image(boot_path)
        
        if not verification.get('components'):
            print("  ❌ Verification failed: Could not extract components")
            return False
        
        print("  ✅ Boot image structure is valid")
        
        # Check kernel
        if 'kernel' in verification['components']:
            kernel_path = verification['components']['kernel']
            kernel_size = Path(kernel_path).stat().st_size
            print(f"  ✅ Kernel present: {kernel_size:,} bytes")
        
        # Check ramdisk
        if 'ramdisk' in verification['components']:
            ramdisk_path = verification['components']['ramdisk']
            ramdisk_size = Path(ramdisk_path).stat().st_size
            print(f"  ✅ Ramdisk present: {ramdisk_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Verification failed: {e}")
        return False


def main():
    """Boot image repacking example"""
    
    print("=" * 70)
    print("Example 3: Boot Image Repacking")
    print("=" * 70)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python example_repack.py <boot.img> [output.img]")
        print()
        print("Examples:")
        print("  python example_repack.py boot.img")
        print("  python example_repack.py boot.img custom_boot.img")
        print()
        print("This will:")
        print("  1. Extract the boot image")
        print("  2. Optionally modify components")
        print("  3. Repack into a new boot image")
        print("  4. Verify the new image")
        sys.exit(1)
    
    boot_image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "repacked_boot.img"
    
    # Verify input file
    if not os.path.exists(boot_image_path):
        print(f"❌ Error: Boot image not found: {boot_image_path}")
        sys.exit(1)
    
    print(f"📱 Input:  {boot_image_path}")
    print(f"💾 Output: {output_path}")
    print()
    
    # Initialize
    print("🔧 Initializing KernelForge...")
    forge = KernelForge(working_dir="repack_workspace")
    print("✅ Initialized")
    print()
    
    # Step 1: Extract original boot image
    print("=" * 70)
    print("STEP 1: Extract Original Boot Image")
    print("=" * 70)
    print()
    
    try:
        extraction = forge.extract_boot_image(boot_image_path)
        extract_dir = Path(extraction['extract_dir'])
        
        print("✅ Extraction complete")
        print()
        print("📦 Extracted components:")
        for component, path in extraction['components'].items():
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"  - {component:12} {size:12,} bytes  {path}")
        print()
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 2: Prepare components for repacking
    print("=" * 70)
    print("STEP 2: Prepare Components")
    print("=" * 70)
    print()
    
    print("📝 Preparing components for repacking...")
    modifications = create_test_modifications(extract_dir)
    print()
    
    # Optional: Modify boot config
    if 'config' in modifications:
        print("⚙️  Boot configuration available")
        
        # Example: You could modify cmdline here
        # modify_kernel_cmdline(modifications['config'], {
        #     'cmdline': 'your_custom_cmdline_here'
        # })
        
        print("  ℹ️  No modifications applied (example)")
        print()
    
    # Ensure we have at least a kernel
    if 'kernel' not in modifications:
        print("❌ Error: No kernel available for repacking")
        sys.exit(1)
    
    print("✅ Components ready for repacking")
    print()
    
    # Step 3: Repack boot image
    print("=" * 70)
    print("STEP 3: Repack Boot Image")
    print("=" * 70)
    print()
    
    try:
        print("🔨 Repacking boot image...")
        repacked_path = forge.repack_boot_image(
            modifications,
            output_path
        )
        
        if not repacked_path or not os.path.exists(repacked_path):
            print("❌ Repacking failed")
            print()
            print("Troubleshooting:")
            print("  1. Install boot image tools:")
            print("     sudo apt-get install abootimg android-tools-mkbootimg")
            print("  2. Check if components are valid")
            print("  3. Review error messages above")
            sys.exit(1)
        
        print()
        print("✅ Repacking successful!")
        print()
        
        # Show file info
        original_size = os.path.getsize(boot_image_path)
        repacked_size = os.path.getsize(repacked_path)
        
        print(f"📊 Size Comparison:")
        print(f"  Original: {original_size:12,} bytes")
        print(f"  Repacked: {repacked_size:12,} bytes")
        
        size_diff = repacked_size - original_size
        if size_diff > 0:
            print(f"  Diff:     +{size_diff:11,} bytes ({size_diff/original_size*100:+.1f}%)")
        else:
            print(f"  Diff:     {size_diff:12,} bytes ({size_diff/original_size*100:.1f}%)")
        print()
        
    except Exception as e:
        print(f"❌ Repacking failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 4: Verify repacked image
    print("=" * 70)
    print("STEP 4: Verify Repacked Image")
    print("=" * 70)
    print()
    
    verification_success = verify_boot_image(repacked_path, forge)
    print()
    
    if not verification_success:
        print("⚠️  Verification had issues - review the image before flashing")
        print()
    
    # Step 5: Compare original and repacked
    print("=" * 70)
    print("STEP 5: Compare Images")
    print("=" * 70)
    print()
    
    try:
        # Extract repacked for comparison
        print("🔍 Analyzing repacked image...")
        repacked_extraction = forge.extract_boot_image(repacked_path)
        
        print()
        print("📊 Component Comparison:")
        print()
        
        # Compare kernels
        if ('kernel' in extraction['components'] and 
            'kernel' in repacked_extraction['components']):
            orig_kernel = Path(extraction['components']['kernel'])
            new_kernel = Path(repacked_extraction['components']['kernel'])
            
            orig_size = orig_kernel.stat().st_size
            new_size = new_kernel.stat().st_size
            
            print("Kernel:")
            print(f"  Original: {orig_size:,} bytes")
            print(f"  Repacked: {new_size:,} bytes")
            if orig_size == new_size:
                print("  Status:   ✅ Identical")
            else:
                print(f"  Status:   ⚠️  Different ({new_size - orig_size:+,} bytes)")
            print()
        
        # Compare ramdisks
        if ('ramdisk' in extraction['components'] and 
            'ramdisk' in repacked_extraction['components']):
            orig_ramdisk = Path(extraction['components']['ramdisk'])
            new_ramdisk = Path(repacked_extraction['components']['ramdisk'])
            
            orig_size = orig_ramdisk.stat().st_size
            new_size = new_ramdisk.stat().st_size
            
            print("Ramdisk:")
            print(f"  Original: {orig_size:,} bytes")
            print(f"  Repacked: {new_size:,} bytes")
            if orig_size == new_size:
                print("  Status:   ✅ Identical")
            else:
                print(f"  Status:   ⚠️  Different ({new_size - orig_size:+,} bytes)")
            print()
        
    except Exception as e:
        print(f"⚠️  Comparison failed: {e}")
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("✅ Successfully repacked boot image!")
    print()
    print(f"📁 Output file:  {os.path.abspath(repacked_path)}")
    print(f"📁 Workspace:    {os.path.abspath('repack_workspace')}/")
    print()
    print("⚠️  BEFORE FLASHING:")
    print("  1. Backup your current boot partition")
    print("  2. Verify the repacked image thoroughly")
    print("  3. Test on a non-critical device first")
    print("  4. Know how to restore from recovery")
    print()
    print("To flash (if you know what you're doing):")
    print(f"  adb reboot bootloader")
    print(f"  fastboot flash boot {repacked_path}")
    print(f"  fastboot reboot")
    print()
    print("Or use:")
    print(f"  python kernel_forge.py flash {repacked_path}")
    print()


if __name__ == '__main__':
    main()
