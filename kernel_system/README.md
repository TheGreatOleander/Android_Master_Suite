# KernelForge 🔨

**Kernel Unpacking, Analysis & Customization Tool**  
*Part of the XDA Master Toolkit*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![XDA](https://img.shields.io/badge/XDA-Master%20Toolkit-orange.svg)](https://github.com/XDA-Master-Toolkit)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Usage](#detailed-usage)
- [Architecture](#architecture)
- [Integration](#integration)
- [Safety Features](#safety-features)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**KernelForge** is a comprehensive toolkit for working with Android kernel images. It provides professional-grade tools for extracting, analyzing, modifying, and repacking kernels from boot images. Whether you're a ROM developer, kernel enthusiast, or security researcher, KernelForge gives you deep insight into kernel internals and the ability to customize them safely.

### What KernelForge Does

- **📦 Extract kernels** from boot images (boot.img, recovery.img)
- **🔍 Analyze kernel** binaries and extract detailed information
- **⚙️ Parse kernel** configurations and detect features
- **🔧 Detect security** features (SELinux, dm-verity, KASLR, etc.)
- **📊 Generate reports** with comprehensive kernel analysis
- **🔨 Repack boot images** with modified components
- **📱 Flash kernels** to devices safely
- **🛡️ Verify integrity** with checksum validation

### Why KernelForge?

**Problem:** Kernel modification is complex and risky. Most users:
- Don't know what's in their kernel
- Can't easily extract or analyze kernel images
- Risk bricking devices with improper modifications
- Lack tools to understand kernel security features

**Solution:** KernelForge provides:
- ✅ Safe, automated kernel extraction
- ✅ Comprehensive kernel analysis
- ✅ Clear documentation of kernel features
- ✅ Professional-grade tooling
- ✅ Integration with the XDA Master Toolkit ecosystem

---

## ✨ Features

### Core Capabilities

#### 1. Boot Image Extraction
- Extract kernel from Android boot images
- Support for multiple extraction methods (abootimg, manual parsing)
- Extract ramdisk, second stage, DTB
- Parse boot image headers
- Save boot configuration

#### 2. Kernel Analysis
- **Version Detection**: Extract Linux version strings
- **Architecture Detection**: Identify ARM, ARM64, x86, x86_64
- **Compression Detection**: Detect gzip, xz, bzip2, lz4, lzo, zstd
- **Automatic Decompression**: Decompress compressed kernels
- **Config Extraction**: Extract embedded kernel configuration (IKCONFIG)
- **String Analysis**: Categorize filesystems, drivers, security features
- **Security Analysis**: Detect SELinux, dm-verity, Seccomp, KASLR

#### 3. Configuration Analysis
Parse and analyze kernel configuration for:
- **Security Features**: SELinux, AppArmor, Seccomp, dm-verity
- **Networking**: IPv6, Netfilter, iptables, BBR congestion control
- **Filesystems**: ext4, f2fs, exFAT, NTFS support
- **Performance**: SMP, preemption, CPU frequency scaling
- **Power Management**: CPU idle, suspend, hibernation

#### 4. Boot Image Repacking
- Repack boot images from components
- Support for mkbootimg and abootimg
- Preserve boot configuration
- Custom kernel integration
- DTB and ramdisk handling

#### 5. Kernel Flashing
- Flash via fastboot
- Safety checks before flashing
- Device detection
- Automatic reboot handling

#### 6. Reporting
- Generate detailed markdown reports
- JSON export of analysis data
- Human-readable summaries
- Feature categorization

### Advanced Features

- **Multi-method Extraction**: Falls back to manual parsing if tools unavailable
- **Comprehensive String Analysis**: Categorizes thousands of kernel strings
- **Feature Detection**: Automatically identifies kernel capabilities
- **Hash Verification**: SHA256 checksums for integrity
- **Workspace Management**: Organized file structure
- **Tool Detection**: Auto-detects available system tools
- **Error Recovery**: Graceful handling of extraction failures

---

## 🚀 Installation

### Prerequisites

**Required:**
- Python 3.7 or higher
- Linux, macOS, or Windows (WSL recommended for Windows)

**Recommended Tools:**
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    abootimg \
    android-tools-mkbootimg \
    android-tools-fastboot \
    file \
    gzip \
    xz-utils \
    bzip2 \
    lz4

# On macOS (using Homebrew)
brew install android-platform-tools
brew install coreutils
```

### Install KernelForge

#### Option 1: Clone Repository (Recommended)
```bash
git clone https://github.com/XDA-Master-Toolkit/KernelForge.git
cd KernelForge
chmod +x kernel_forge.py
```

#### Option 2: Direct Download
```bash
curl -O https://raw.githubusercontent.com/XDA-Master-Toolkit/KernelForge/main/kernel_forge.py
chmod +x kernel_forge.py
```

### Verify Installation

```bash
python3 kernel_forge.py --help
```

You should see the KernelForge help message.

---

## 🎬 Quick Start

### 5-Minute Getting Started Guide

#### 1. Extract and Analyze a Boot Image

```bash
# Extract boot image
python3 kernel_forge.py extract boot.img

# This will:
# - Extract kernel, ramdisk, DTB, etc.
# - Analyze kernel version and features
# - Generate detailed analysis
# - Save everything to kernel_workspace/
```

#### 2. View Analysis Results

```bash
# Check the extraction directory
cd kernel_workspace/extracted/boot/

# View kernel analysis
cat ../../extracted/kernel_analysis.json

# View extraction info
cat ../../extracted/extraction_info.json
```

#### 3. Generate a Report

```bash
# Generate markdown report
python3 kernel_forge.py report kernel_workspace/extracted/extraction_info.json

# View the report
cat kernel_workspace/output/kernel_report.md
```

#### 4. Repack Boot Image (Optional)

```bash
# Repack with modified kernel
python3 kernel_forge.py repack \
    --kernel kernel_workspace/extracted/boot/kernel \
    --ramdisk kernel_workspace/extracted/boot/ramdisk.img \
    --config kernel_workspace/extracted/boot/bootimg.cfg \
    --output custom_boot.img
```

#### 5. Flash to Device (Optional - Requires Unlocked Bootloader)

```bash
# Put device in fastboot mode, then:
python3 kernel_forge.py flash custom_boot.img
```

---

## 📖 Detailed Usage

### Command Reference

#### Extract Boot Image

Extract kernel and components from a boot image:

```bash
python3 kernel_forge.py extract <boot_image> [options]

Options:
  -w, --workspace DIR    Working directory (default: kernel_workspace)

Examples:
  python3 kernel_forge.py extract boot.img
  python3 kernel_forge.py extract recovery.img -w my_workspace
```

**What it extracts:**
- Kernel binary
- Ramdisk (initrd)
- Second stage bootloader (if present)
- Device tree blob (DTB, if present)
- Boot configuration (addresses, cmdline, etc.)

**Output structure:**
```
kernel_workspace/
├── extracted/
│   ├── boot/
│   │   ├── kernel          # Kernel binary
│   │   ├── ramdisk.img     # Ramdisk
│   │   ├── bootimg.cfg     # Boot config
│   │   └── dtb             # Device tree (if present)
│   ├── extraction_info.json
│   └── kernel_analysis.json
```

#### Analyze Kernel

Analyze a kernel binary in detail:

```bash
python3 kernel_forge.py analyze <kernel_file> [options]

Options:
  -w, --workspace DIR    Working directory (default: kernel_workspace)

Examples:
  python3 kernel_forge.py analyze kernel.img
  python3 kernel_forge.py analyze kernel_workspace/extracted/boot/kernel
```

**Analysis includes:**
- Kernel version and build info
- Architecture (ARM, ARM64, x86, x86_64)
- Compression type
- Decompressed analysis
- Embedded kernel config (if present)
- Security features
- String analysis (filesystems, drivers, etc.)
- SHA256 checksum

**Output:**
```json
{
  "path": "kernel",
  "size": 12582912,
  "sha256": "a1b2c3d4...",
  "kernel_version": "5.15.41",
  "architecture": "arm64",
  "compression": "gzip",
  "security_features": {
    "selinux": true,
    "dm_verity": true,
    "seccomp": true,
    "kaslr": true
  },
  "config_features": {
    "security": ["SELinux enabled", "dm-verity enabled"],
    "networking": ["IPv6 support", "BBR congestion control"],
    "filesystem": ["ext4 filesystem", "f2fs filesystem"]
  }
}
```

#### Repack Boot Image

Repack boot image from components:

```bash
python3 kernel_forge.py repack [options]

Required:
  -k, --kernel FILE      Kernel file

Optional:
  -r, --ramdisk FILE     Ramdisk file
  -s, --second FILE      Second stage file
  -d, --dtb FILE         Device tree blob file
  -c, --config FILE      Boot config file
  -o, --output FILE      Output boot image (default: new_boot.img)
  -w, --workspace DIR    Working directory (default: kernel_workspace)

Examples:
  # Repack with kernel only
  python3 kernel_forge.py repack -k kernel.img -o boot.img
  
  # Repack with all components
  python3 kernel_forge.py repack \
      -k kernel.img \
      -r ramdisk.img \
      -d dtb \
      -c bootimg.cfg \
      -o custom_boot.img
```

**Requirements:**
- At minimum, a kernel file is required
- Other components are optional
- Uses mkbootimg or abootimg (must be installed)

#### Generate Report

Generate a comprehensive analysis report:

```bash
python3 kernel_forge.py report <analysis_json> [options]

Options:
  -o, --output FILE      Output report path
  -w, --workspace DIR    Working directory (default: kernel_workspace)

Examples:
  python3 kernel_forge.py report kernel_workspace/extracted/extraction_info.json
  python3 kernel_forge.py report analysis.json -o my_report.md
```

**Report includes:**
- Kernel version and build information
- Architecture and compression
- Security features status
- Configuration features by category
- Detected components and strings
- File hashes and sizes

#### Flash Kernel

Flash boot image to device:

```bash
python3 kernel_forge.py flash <boot_image> [options]

Options:
  -m, --mode MODE        Flash mode: fastboot or adb (default: fastboot)
  -w, --workspace DIR    Working directory (default: kernel_workspace)

Examples:
  python3 kernel_forge.py flash custom_boot.img
  python3 kernel_forge.py flash boot.img -m fastboot
```

**Safety requirements:**
- Device must be in fastboot mode
- Bootloader must be unlocked
- Confirms device is connected before flashing
- Automatically reboots after flash

⚠️ **WARNING**: Only flash kernels you trust! Always backup your device first.

---

## 🏗️ Architecture

### Core Components

```
KernelForge/
├── kernel_forge.py          # Main application
├── README.md                # This file
├── QUICKSTART.md           # 5-minute guide
├── examples/               # Usage examples
│   ├── example_basic.py
│   ├── example_analysis.py
│   └── example_custom.py
└── docs/                   # Extended documentation
```

### Data Flow

```
Boot Image (boot.img)
        ↓
   [Extract]
        ↓
Kernel + Ramdisk + DTB + Config
        ↓
   [Analyze]
        ↓
Version + Security + Config + Strings
        ↓
   [Report]
        ↓
Comprehensive Analysis Report
        ↓
   [Modify] (Optional)
        ↓
   [Repack]
        ↓
Custom Boot Image
        ↓
   [Flash]
        ↓
Device with Custom Kernel
```

### Extraction Methods

KernelForge supports multiple extraction methods and automatically falls back:

1. **abootimg** (Preferred): Uses abootimg tool if available
2. **Manual Android**: Parses Android boot image header directly
3. **Raw extraction**: Attempts to find gzip-compressed kernel in raw binary

### Analysis Pipeline

```python
1. Read kernel file
2. Calculate SHA256 hash
3. Detect compression (gzip, xz, bzip2, lz4, etc.)
4. Decompress if compressed
5. Extract version string
6. Detect architecture (ARM, ARM64, x86)
7. Extract embedded kernel config (IKCONFIG)
8. Analyze config features
9. Extract interesting strings
10. Detect security features
11. Generate comprehensive report
```

---

## 🔗 Integration

### Integration with XDA Master Toolkit

KernelForge integrates seamlessly with other XDA Master Toolkit components:

#### With BootGuardian
```python
from boot_guardian import BootGuardian
from kernel_forge import KernelForge

# Extract boot image
boot = BootGuardian()
boot_info = boot.get_boot_info()

# Analyze kernel
forge = KernelForge()
kernel_analysis = forge.analyze_kernel(boot_info['boot_partition'])
```

#### With DeviceProbe
```python
from device_probe import DeviceProbe
from kernel_forge import KernelForge

# Get device info
probe = DeviceProbe()
device_info = probe.get_full_profile()

# Pull boot image
probe.pull_partition('boot', 'boot.img')

# Analyze
forge = KernelForge()
analysis = forge.extract_boot_image('boot.img')
```

#### With FlashAuditor
```python
from flash_auditor import FlashAuditor
from kernel_forge import KernelForge

# Analyze kernel before flashing
forge = KernelForge()
analysis = forge.analyze_kernel('custom_kernel.img')

# Log to auditor
auditor = FlashAuditor()
auditor.log_operation('kernel_flash', 'boot', analysis)

# Flash
forge.flash_kernel('custom_kernel.img')
```

### Programmatic API

Use KernelForge in your Python scripts:

```python
from kernel_forge import KernelForge

# Initialize
forge = KernelForge(working_dir='my_workspace')

# Extract boot image
extraction = forge.extract_boot_image('boot.img')
print(f"Kernel: {extraction['components']['kernel']}")

# Analyze kernel
analysis = forge.analyze_kernel(extraction['components']['kernel'])
print(f"Version: {analysis['kernel_version']}")
print(f"Security: {analysis['security_features']}")

# Generate report
report = forge.generate_report(analysis, 'kernel_report.md')

# Repack with modifications
components = {
    'kernel': 'modified_kernel.img',
    'ramdisk': extraction['components']['ramdisk'],
    'config': extraction['components']['config']
}
new_boot = forge.repack_boot_image(components, 'new_boot.img')

# Flash to device
forge.flash_kernel(new_boot, 'fastboot')
```

---

## 🛡️ Safety Features

### Built-in Protections

1. **Hash Verification**: SHA256 checksums for all files
2. **Device Detection**: Confirms device before flashing
3. **Bootloader Check**: Warns if bootloader is locked
4. **Backup Prompts**: Encourages backups before modifications
5. **Validation**: Checks file integrity before operations
6. **Error Handling**: Graceful failures with clear messages

### Best Practices

✅ **DO:**
- Always backup your current boot image first
- Verify checksums after download
- Test on non-critical devices first
- Read all warnings carefully
- Keep stock boot images for recovery

❌ **DON'T:**
- Flash kernels for different devices
- Skip verification steps
- Flash on locked bootloaders
- Ignore error messages
- Modify without understanding

### Recovery Plan

If something goes wrong:

1. **Boot to Recovery**: Hold Power + Volume Down during boot
2. **Flash Stock Boot**: Use fastboot to flash original boot.img
3. **Use EDL Mode**: Last resort for Qualcomm devices
4. **Seek Help**: XDA forums have device-specific help

---

## 💡 Examples

See the [examples directory](examples/) for complete usage examples:

### Basic Extraction and Analysis
```python
# examples/example_basic.py
from kernel_forge import KernelForge

forge = KernelForge()

# Extract
info = forge.extract_boot_image('boot.img')

# Analyze
analysis = forge.analyze_kernel(info['components']['kernel'])

# Report
forge.generate_report(analysis)
```

### Custom Kernel Building
```python
# examples/example_custom.py
from kernel_forge import KernelForge

forge = KernelForge()

# Extract base
base = forge.extract_boot_image('stock_boot.img')

# Modify kernel config
modifications = {
    'overclock': True,
    'scheduler': 'bfq',
    'tcp_congestion': 'bbr'
}

# Create custom kernel (requires source/toolchain)
custom = forge.create_custom_kernel(
    base['components']['kernel'],
    modifications
)

# Repack
new_boot = forge.repack_boot_image({
    'kernel': custom,
    'ramdisk': base['components']['ramdisk'],
    'config': base['components']['config']
}, 'custom_boot.img')
```

### Security Audit
```python
# examples/example_security.py
from kernel_forge import KernelForge

forge = KernelForge()

# Analyze multiple kernels
kernels = ['stock_kernel.img', 'custom_kernel.img', 'downloaded_kernel.img']

for kernel in kernels:
    analysis = forge.analyze_kernel(kernel)
    
    print(f"\n{kernel}:")
    print(f"SELinux: {analysis['security_features']['selinux']}")
    print(f"dm-verity: {analysis['security_features']['dm_verity']}")
    print(f"Seccomp: {analysis['security_features']['seccomp']}")
```

---

## 🔧 Troubleshooting

### Common Issues

#### "No boot image tools available"

**Problem**: mkbootimg or abootimg not found

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install abootimg android-tools-mkbootimg

# Or build from source
git clone https://android.googlesource.com/platform/system/tools/mkbootimg
cd mkbootimg
python3 setup.py install
```

#### "Could not extract kernel"

**Problem**: Boot image format not recognized

**Solutions**:
1. Verify it's actually a boot image: `file boot.img`
2. Try manual extraction: Look for gzip magic bytes
3. Check if it's encrypted or packed differently
4. Consult device-specific XDA thread

#### "Device not found in fastboot"

**Problem**: Device not in fastboot mode or drivers missing

**Solutions**:
1. Reboot to fastboot: `adb reboot bootloader`
2. Check connection: `fastboot devices`
3. Install ADB/Fastboot drivers (Windows)
4. Try different USB cable/port

#### "Flash failed: remote: Locked bootloader"

**Problem**: Bootloader is still locked

**Solution**:
1. Enable OEM unlocking in Developer Options
2. Unlock bootloader: `fastboot oem unlock` or `fastboot flashing unlock`
3. ⚠️ This will wipe your device!

### Debug Mode

Enable verbose output for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from kernel_forge import KernelForge
forge = KernelForge()
# Now see detailed debug output
```

### Getting Help

- **GitHub Issues**: https://github.com/XDA-Master-Toolkit/KernelForge/issues
- **XDA Thread**: [Coming Soon]
- **Documentation**: Check docs/ directory
- **Examples**: See examples/ directory

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

### Ways to Contribute

1. **Report Bugs**: Open GitHub issues with details
2. **Suggest Features**: Propose new capabilities
3. **Submit Code**: Pull requests for improvements
4. **Documentation**: Improve guides and examples
5. **Testing**: Test on different devices
6. **Share Knowledge**: Help others in discussions

### Development Setup

```bash
# Clone repository
git clone https://github.com/XDA-Master-Toolkit/KernelForge.git
cd KernelForge

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Check code style
pylint kernel_forge.py
black kernel_forge.py
```

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure backward compatibility
- Add examples for new functionality

---

## 📜 License

KernelForge is licensed under the MIT License:

```
MIT License

Copyright (c) 2026 XDA Master Toolkit Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Thanks To

- **XDA Developers Community**: For years of knowledge sharing
- **Kernel Developers**: ElementalX, Franco, flar2, and countless others
- **Tool Creators**: mkbootimg, abootimg, and all the great tools we build on
- **Android Open Source Project**: For providing the foundation
- **Contributors**: Everyone who helps improve this tool

### Related Tools

- **abootimg**: Android boot image tool
- **mkbootimg**: Android boot image creation tool
- **Android Image Kitchen**: Boot/recovery image tools
- **osm0sis's tools**: AnyKernel and other utilities

---

## 🎯 Project Status

**Current Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: February 2026

### Roadmap

- [x] Basic extraction and analysis
- [x] Security feature detection
- [x] Kernel config parsing
- [x] Boot image repacking
- [x] Fastboot flashing
- [ ] GUI interface
- [ ] Kernel building from source
- [ ] Advanced patching system
- [ ] Automated testing framework
- [ ] Cloud-based analysis

---

## 📞 Contact

- **GitHub**: https://github.com/XDA-Master-Toolkit/KernelForge
- **XDA Thread**: [Coming Soon]
- **Email**: [Coming Soon]
- **Discord**: [Coming Soon]

---

**Made with ❤️ by the XDA community, for the XDA community**

*Part of the XDA Master Toolkit - Making Android modification safe for everyone*

---

**⚠️ IMPORTANT DISCLAIMER**

This tool is provided for educational and development purposes. Modifying your device's kernel can:
- Void your warranty
- Brick your device if done incorrectly
- Cause data loss
- Create security vulnerabilities

Always:
- Backup your device first
- Understand what you're doing
- Use on devices you're willing to risk
- Follow device-specific guides
- Keep stock images for recovery

**Use at your own risk. We are not responsible for bricked devices.**

---

*Last Updated: February 2026*  
*XDA Master Toolkit v1.0*
