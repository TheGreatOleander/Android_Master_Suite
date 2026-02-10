# KernelForge Quick Start Guide 🚀

**Get started with kernel extraction and analysis in 5 minutes!**

---

## ⚡ Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** installed
- **Android boot image** (boot.img) to analyze
- **Linux/macOS/WSL** (recommended, but works on Windows too)

Optional but recommended:
```bash
# Install kernel tools
sudo apt-get install -y abootimg android-tools-mkbootimg file gzip
```

---

## 🎯 Installation

### Option 1: Quick Install
```bash
# Download the tool
curl -O https://raw.githubusercontent.com/XDA-Master-Toolkit/KernelForge/main/kernel_forge.py

# Make it executable
chmod +x kernel_forge.py

# Verify installation
python3 kernel_forge.py --help
```

### Option 2: Clone Repository
```bash
git clone https://github.com/XDA-Master-Toolkit/KernelForge.git
cd KernelForge
chmod +x kernel_forge.py
```

---

## 🚀 Your First Kernel Analysis

### Step 1: Extract Boot Image (1 minute)

```bash
# Extract and analyze boot image in one command
python3 kernel_forge.py extract boot.img
```

**What this does:**
- ✅ Extracts kernel from boot.img
- ✅ Extracts ramdisk and other components
- ✅ Automatically analyzes the kernel
- ✅ Generates detailed reports
- ✅ Saves everything to `kernel_workspace/`

**Output:**
```
📦 Extracting boot image: boot.img
🔧 Using abootimg for extraction...
🔍 Analyzing kernel: kernel_workspace/extracted/boot/kernel
✅ Extraction complete!
📁 Extract directory: kernel_workspace/extracted/boot
```

### Step 2: View Analysis Results (30 seconds)

```bash
# Navigate to extracted files
cd kernel_workspace/extracted/boot/

# View extracted components
ls -lh
# kernel          - Kernel binary
# ramdisk.img     - Ramdisk
# bootimg.cfg     - Boot configuration
# dtb             - Device tree (if present)

# View kernel analysis
cat ../kernel_analysis.json
```

**Analysis includes:**
- Kernel version (e.g., "5.15.41-android13-9-00006-g0e7c139da09b")
- Architecture (arm64, arm, x86_64, etc.)
- Compression type (gzip, xz, lz4, etc.)
- Security features (SELinux, dm-verity, Seccomp, KASLR)
- Kernel configuration features
- Detected filesystems and drivers

### Step 3: Generate Human-Readable Report (30 seconds)

```bash
# Generate markdown report
python3 kernel_forge.py report kernel_workspace/extracted/extraction_info.json

# View the report
cat kernel_workspace/output/kernel_report.md
```

**Sample Report:**
```markdown
# Kernel Analysis Report

Generated: 2026-02-10 14:30:00

## Kernel Information

**Version:** Linux version 5.15.41-android13...
**Kernel Version:** 5.15.41
**Architecture:** arm64
**Compression:** gzip
**Size:** 12,582,912 bytes
**SHA256:** a1b2c3d4e5f6...

## Security Features

- **SELINUX:** ✅ Enabled
- **DM_VERITY:** ✅ Enabled
- **SECCOMP:** ✅ Enabled
- **KASLR:** ✅ Enabled

## Kernel Configuration Features

### Security
- SELinux enabled
- dm-verity enabled
- Seccomp enabled

### Networking
- IPv6 support
- Netfilter support
- BBR congestion control

### Filesystem
- ext4 filesystem
- f2fs filesystem
- exFAT filesystem
```

---

## 🎓 Common Tasks

### Task 1: Analyze Just the Kernel

If you already have a kernel file:

```bash
python3 kernel_forge.py analyze kernel.img
```

### Task 2: Extract from Custom Location

```bash
python3 kernel_forge.py extract /path/to/boot.img -w my_workspace
```

### Task 3: Check Kernel Version Quickly

```bash
python3 kernel_forge.py extract boot.img | grep "Kernel version"
```

### Task 4: Repack Boot Image

After modifying kernel or ramdisk:

```bash
python3 kernel_forge.py repack \
    --kernel modified_kernel.img \
    --ramdisk kernel_workspace/extracted/boot/ramdisk.img \
    --config kernel_workspace/extracted/boot/bootimg.cfg \
    --output new_boot.img
```

### Task 5: Flash to Device

**⚠️ WARNING**: Only if you know what you're doing!

```bash
# Put device in fastboot mode first
adb reboot bootloader

# Flash the kernel
python3 kernel_forge.py flash new_boot.img

# Device will automatically reboot
```

---

## 🔍 Understanding the Output

### Directory Structure

After extraction, you'll have:

```
kernel_workspace/
├── extracted/
│   ├── boot/                    # Extracted boot.img components
│   │   ├── kernel              # Kernel binary
│   │   ├── ramdisk.img         # Ramdisk
│   │   ├── bootimg.cfg         # Boot config (addresses, cmdline)
│   │   └── dtb                 # Device tree (if present)
│   ├── extraction_info.json    # Full extraction metadata
│   └── kernel_analysis.json    # Detailed kernel analysis
├── build/                       # (Future) Build directory
└── output/
    └── kernel_report.md        # Human-readable report
```

### Key Files Explained

**extraction_info.json** - Complete extraction metadata:
```json
{
  "boot_image": "boot.img",
  "timestamp": "2026-02-10T14:30:00",
  "method": "abootimg",
  "components": {
    "kernel": "kernel_workspace/extracted/boot/kernel",
    "ramdisk": "kernel_workspace/extracted/boot/ramdisk.img"
  },
  "boot_config": {
    "cmdline": "console=ttyMSM0,115200n8...",
    "kernel_addr": "0x00008000"
  }
}
```

**kernel_analysis.json** - Kernel details:
```json
{
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
    "filesystem": ["ext4 filesystem", "f2fs filesystem"]
  }
}
```

---

## 💡 Pro Tips

### Tip 1: Analyze Multiple Boot Images

```bash
# Create a script to analyze all boot images
for img in *.img; do
    echo "Analyzing $img..."
    python3 kernel_forge.py extract "$img" -w "workspace_$img"
done
```

### Tip 2: Compare Kernels

```bash
# Extract stock kernel
python3 kernel_forge.py extract stock_boot.img -w stock

# Extract custom kernel
python3 kernel_forge.py extract custom_boot.img -w custom

# Compare the analysis files
diff stock/extracted/kernel_analysis.json custom/extracted/kernel_analysis.json
```

### Tip 3: Quick Security Audit

```bash
# Extract and check security features
python3 kernel_forge.py extract boot.img
cat kernel_workspace/extracted/kernel_analysis.json | grep -A5 "security_features"
```

### Tip 4: Backup Before Modifying

```bash
# Always backup current boot
adb shell su -c "dd if=/dev/block/by-name/boot of=/sdcard/boot_backup.img"
adb pull /sdcard/boot_backup.img

# Now you can safely experiment
```

---

## ⚠️ Safety Checklist

Before flashing any kernel:

- [ ] ✅ Boot image is for YOUR device (check codename)
- [ ] ✅ Bootloader is unlocked
- [ ] ✅ You have a backup of stock boot.img
- [ ] ✅ Battery is >50% charged
- [ ] ✅ You understand what the kernel does
- [ ] ✅ You know how to restore from recovery
- [ ] ✅ You're willing to risk your device

**NEVER:**
- ❌ Flash kernels for different devices
- ❌ Flash without backups
- ❌ Flash on locked bootloader
- ❌ Flash without understanding
- ❌ Flash critical production devices

---

## 🆘 Troubleshooting

### Problem: "No such file or directory: boot.img"

**Solution**: Provide the full path to your boot image
```bash
python3 kernel_forge.py extract /path/to/boot.img
```

### Problem: "No boot image tools available"

**Solution**: Install kernel tools
```bash
sudo apt-get install abootimg android-tools-mkbootimg
```

### Problem: "Could not extract kernel"

**Solutions**:
1. Verify it's a boot image: `file boot.img`
2. Try with a different boot.img
3. Check if the image is encrypted
4. Consult your device's XDA thread

### Problem: "Device not found" when flashing

**Solutions**:
1. Enable USB debugging
2. Check USB cable and port
3. Install ADB/Fastboot drivers
4. Run: `fastboot devices` to verify connection

---

## 📚 Next Steps

Now that you can extract and analyze kernels:

1. **Learn More**: Read the full [README.md](README.md)
2. **See Examples**: Check the [examples/](examples/) directory
3. **Integration**: Use with other XDA Master Toolkit tools
4. **Customize**: Modify kernels for your needs
5. **Contribute**: Help improve KernelForge

### Recommended Reading

- [Full Documentation](README.md)
- [Boot Image Structure](docs/boot-image-format.md)
- [Kernel Security Features](docs/security-features.md)
- [Custom Kernel Guide](docs/custom-kernels.md)

---

## 🎯 Common Use Cases

### Use Case 1: Security Research
```bash
# Audit kernel for security features
python3 kernel_forge.py extract boot.img
python3 kernel_forge.py report kernel_workspace/extracted/extraction_info.json
# Review security_features section
```

### Use Case 2: ROM Development
```bash
# Extract kernel from working ROM
python3 kernel_forge.py extract lineage_boot.img -w lineage
# Extract from your custom ROM
python3 kernel_forge.py extract myrom_boot.img -w myrom
# Compare configurations
```

### Use Case 3: Kernel Porting
```bash
# Extract kernel from donor device
python3 kernel_forge.py extract donor_boot.img -w donor
# Analyze architecture and features
cat donor/extracted/kernel_analysis.json
# Use analysis to guide porting
```

### Use Case 4: Performance Tuning
```bash
# Extract custom kernel
python3 kernel_forge.py extract performance_boot.img
# Check for performance features
grep -i "scheduler\|governor\|freq" kernel_workspace/extracted/kernel_analysis.json
```

---

## 🔗 Quick Links

- **Full README**: [README.md](README.md)
- **GitHub Repo**: https://github.com/XDA-Master-Toolkit/KernelForge
- **Report Issues**: https://github.com/XDA-Master-Toolkit/KernelForge/issues
- **XDA Master Toolkit**: https://github.com/XDA-Master-Toolkit
- **Examples**: [examples/](examples/)

---

## ✅ Quick Reference

### Essential Commands

```bash
# Extract boot image
python3 kernel_forge.py extract boot.img

# Analyze kernel only
python3 kernel_forge.py analyze kernel.img

# Generate report
python3 kernel_forge.py report extraction_info.json

# Repack boot image
python3 kernel_forge.py repack -k kernel.img -r ramdisk.img -o new.img

# Flash to device
python3 kernel_forge.py flash new_boot.img
```

### File Locations

```bash
# Extracted kernel
kernel_workspace/extracted/boot/kernel

# Kernel analysis
kernel_workspace/extracted/kernel_analysis.json

# Boot config
kernel_workspace/extracted/boot/bootimg.cfg

# Generated report
kernel_workspace/output/kernel_report.md
```

---

**🎉 You're now ready to use KernelForge!**

For detailed information, see the [full README](README.md).

For help, open an issue on [GitHub](https://github.com/XDA-Master-Toolkit/KernelForge/issues).

---

*Part of the XDA Master Toolkit - Making Android modification safe for everyone*

*Last Updated: February 2026*
