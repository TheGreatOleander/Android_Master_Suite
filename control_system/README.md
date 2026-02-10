# MasterControl 🎮

**Unified Interface for XDA Master Toolkit**

The central hub that orchestrates all 7 tools in the XDA Master Toolkit suite, providing guided workflows, safety checks, and seamless tool integration.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 What Is MasterControl?

MasterControl is the **unified interface** that ties together all tools in the XDA Master Toolkit:

1. **PartitionGuardian** - Partition backup/recovery
2. **RecoveryManager** - Custom recovery management
3. **DeviceProbe** - Device fingerprinting
4. **BootGuardian** - Bootloader management
5. **ROMValidator** - Pre-flash validation
6. **FlashAuditor** - Modification tracking
7. **EDL Rescue** - Emergency download mode

Instead of running 7 separate tools, you run **one command** and get:
- Interactive menus
- Guided workflows
- Safety checkpoints
- Automatic tool chaining
- Beautiful terminal UI

---

## ✨ Key Features

### 🚀 Quick Actions (Beginner Mode)
- **First Time Setup** - Complete guided workflow for new users
- **Install Custom Recovery** - Step-by-step recovery installation
- **Backup Everything** - One-click complete device backup
- **Validate ROM** - Check compatibility before flashing

### 🛠️ Individual Tool Access
- Launch any of the 7 tools from one interface
- Auto-detect tool availability
- Seamless integration with shared configurations

### 📊 Real-Time Dashboard
- Device connection status (ADB/Fastboot)
- Device information display
- Tool availability tracking
- Quick status overview

### 🎓 Two Modes

**Beginner Mode:**
- Guided workflows with step-by-step instructions
- Safety prompts and warnings
- Recommended actions highlighted
- Perfect for first-time users

**Advanced Mode:**
- Direct tool access
- Fewer confirmations
- Command-line style efficiency
- For experienced users

### 🛡️ Safety Features
- Comprehensive safety checklist
- Pre-operation validation
- Automatic backup prompts
- Clear risk warnings
- Device status verification

---

## 📋 Requirements

### System Requirements
- **Python:** 3.7 or higher
- **OS:** Linux, macOS, Windows (WSL recommended)
- **Tools:** ADB, Fastboot installed and in PATH

### Device Requirements
- Android device with USB debugging enabled
- USB cable (high quality recommended)
- Unlocked bootloader (for most operations)

### Tool Requirements
MasterControl works best with all 7 tools installed:
- PartitionGuardian
- RecoveryManager
- DeviceProbe
- BootGuardian
- ROMValidator
- FlashAuditor
- EDL Rescue

*Tools are detected automatically - missing tools will be marked unavailable.*

---

## 🚀 Installation

### Step 1: Install Python Dependencies
```bash
# MasterControl has ZERO external dependencies!
# Uses only Python standard library
```

### Step 2: Download MasterControl
```bash
# Clone the repository
git clone https://github.com/XDA-Master-Toolkit/MasterControl.git
cd MasterControl

# Make executable
chmod +x master_control.py
```

### Step 3: Install Other Tools (Optional)
```bash
# Install the 7 tools to unlock full functionality
cd ~/xda-toolkit

# Clone each tool
git clone https://github.com/XDA-Master-Toolkit/PartitionGuardian.git
git clone https://github.com/XDA-Master-Toolkit/RecoveryManager.git
git clone https://github.com/XDA-Master-Toolkit/DeviceProbe.git
git clone https://github.com/XDA-Master-Toolkit/BootGuardian.git
git clone https://github.com/XDA-Master-Toolkit/ROMValidator.git
git clone https://github.com/XDA-Master-Toolkit/FlashAuditor.git
git clone https://github.com/XDA-Master-Toolkit/EDL-Rescue.git
```

### Step 4: Verify ADB/Fastboot
```bash
# Check ADB
adb version

# Check Fastboot
fastboot --version

# If not installed:
# Ubuntu/Debian: sudo apt install android-tools-adb android-tools-fastboot
# macOS: brew install android-platform-tools
# Windows: Download from Google SDK Platform Tools
```

---

## 📖 Quick Start

### Launch MasterControl
```bash
python3 master_control.py
```

### First Time User Workflow
1. Launch MasterControl
2. Select **"1. First Time Setup"**
3. Follow the guided wizard:
   - Device detection
   - Safety checklist
   - Partition backup
   - Bootloader check
4. Device is ready for safe modification!

### Install Custom Recovery
1. Select **"2. Install Custom Recovery"**
2. Choose your recovery (TWRP, OrangeFox, LineageOS)
3. Confirm bootloader unlocked
4. Create safety backup
5. Flash recovery
6. Verify installation

### Create Complete Backup
1. Select **"3. Backup Everything"**
2. Confirm backup location
3. Wait for backup to complete
4. Store backup safely

### Validate ROM Before Flashing
1. Select **"4. Validate ROM Before Flash"**
2. Provide ROM zip path
3. Review compatibility checks
4. Get go/no-go decision

---

## 🎮 Usage Guide

### Main Menu Navigation

```
╔══════════════════════════════════════════════════════════════╗
║              XDA MASTER TOOLKIT - MASTERCONTROL              ║
║          Unified Interface for Android Modification          ║
╚══════════════════════════════════════════════════════════════╝

📊 Device Status Dashboard
────────────────────────────────────────────────────────────────

Connection:
  ● Connected (ADB Mode)

Device Information:
  Model: OnePlus 9 Pro
  Codename: lemonadep
  Android: 14
  Bootloader: Unlocked

Available Tools:
  ✓ PartitionGuardian
  ✓ RecoveryManager
  ✓ DeviceProbe
  ✓ BootGuardian
  ✓ ROMValidator
  ✓ FlashAuditor
  ✓ EDL Rescue

  (7/7 tools available)

────────────────────────────────────────────────────────────────

Main Menu

🚀 Quick Actions (Guided)
  ✓ 1. First Time Setup [RECOMMENDED]
     Guided workflow for new users
  ✓ 2. Install Custom Recovery
     Step-by-step recovery installation
  ✓ 3. Backup Everything
     Create complete device backup
  ✓ 4. Validate ROM Before Flash
     Check ROM compatibility & safety

🛠️  Individual Tools
  ✓ 5. PartitionGuardian
     Backup/restore partition tables
  ✓ 6. RecoveryManager
     Install & manage custom recoveries
  ✓ 7. DeviceProbe
     Profile & fingerprint device
  ✓ 8. BootGuardian
     Manage bootloader & boot chain
  ✓ 9. ROMValidator
     Validate ROM compatibility
  ✓ 10. FlashAuditor
      Track & audit modifications
  ✓ 11. EDL Rescue
      Emergency download mode recovery

⚙️  Settings & Information
  ✓ 12. Toggle Mode
     Switch to Advanced mode
  ✓ 13. Safety Checklist
     Review safety before modifications
  ✓ 14. About & Help
     Documentation & support

  ✓ 0. Exit
     Close MasterControl

────────────────────────────────────────────────────────────────
Select an option:
```

### Beginner Mode Features

#### 1. First Time Setup Wizard
Comprehensive 5-step guided setup:
1. **Device Detection** - Auto-detect and profile device
2. **Safety Checkpoint** - Verify all safety requirements
3. **Partition Backup** - Create critical partition backup
4. **Bootloader Check** - Verify bootloader status
5. **Setup Complete** - Ready for modifications

#### 2. Install Custom Recovery
Step-by-step recovery installation:
- Pre-installation checks
- Bootloader verification
- Automatic partition backup
- Recovery selection (TWRP/OrangeFox/LineageOS)
- Installation with verification
- Post-install instructions

#### 3. Backup Everything
Complete device backup:
- Partition table
- Boot partition
- Recovery partition
- EFS/modem (device-specific)
- Timestamped backup directories
- Size estimation

#### 4. Validate ROM Before Flash
Pre-flash safety validation:
- File integrity check
- Device compatibility
- Android version match
- Partition scheme verification
- Bootloader version check
- Signature verification

### Advanced Mode Features

**Direct Tool Access:**
- Quick launch any tool
- Fewer confirmation prompts
- Command-line style efficiency
- Assumes user knowledge

**Toggle Between Modes:**
- Switch anytime via settings
- Preferences saved automatically
- Choose what fits your skill level

---

## 🛡️ Safety Checklist

Before modifying your device, MasterControl ensures you've covered:

### Preparation
- [ ] Battery charged above 50%
- [ ] All important data backed up
- [ ] Stock ROM downloaded
- [ ] Know emergency recovery method
- [ ] Working USB cable and PC ready

### Knowledge
- [ ] Understand what you're modifying
- [ ] Read complete guide
- [ ] Know recovery vs ROM vs kernel
- [ ] Understand bootloader unlock risks
- [ ] Familiar with ADB/Fastboot

### Risks Acknowledged
- [ ] Bootloader unlock wipes data
- [ ] Wrong ROM can brick device
- [ ] Warranty may be voided
- [ ] Banking apps may break
- [ ] OTA updates won't work

### Safety Tools Used
- [ ] Partition backup created
- [ ] Boot/recovery backed up
- [ ] FlashAuditor logging enabled
- [ ] Stock firmware available
- [ ] Recovery tested

---

## 🎨 Interface Features

### Color-Coded UI
- **Green** ✓ - Success, available, confirmed
- **Yellow** ⚠ - Warnings, caution, input prompts
- **Red** ✗ - Errors, failures, critical warnings
- **Cyan** 🔹 - Headers, tool names, information
- **Purple** 🔸 - Settings, configuration
- **Gray** - Secondary info, separators

### Visual Elements
- Dashboard with real-time device status
- Progress indicators with animations
- Clear section separators
- Menu item formatting with icons
- Status indicators throughout

### User Experience
- **Clear Navigation** - Number-based menu selection
- **Input Validation** - Only accept valid choices
- **Confirmations** - Double-check risky operations
- **Loading Animations** - Visual feedback during operations
- **Help Text** - Contextual guidance throughout

---

## 🔗 Tool Integration

### How MasterControl Orchestrates Tools

```
┌─────────────────────────────────────────┐
│         MASTERCONTROL (Hub)             │
│  • Unified Interface                    │
│  • Workflow Orchestration               │
│  • Safety Checkpoints                   │
└─────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Partition│ │Recovery│ │Device  │
│Guardian│ │Manager │ │Probe   │
└────────┘ └────────┘ └────────┘
    │         │         │
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Boot    │ │ROM     │ │Flash   │
│Guardian│ │Validator│ │Auditor │
└────────┘ └────────┘ └────────┘
              │
              ▼
         ┌────────┐
         │EDL     │
         │Rescue  │
         └────────┘
```

### Workflow Examples

**Example 1: First Time Setup**
```
MasterControl
    ↓
DeviceProbe (detect device)
    ↓
Safety Checklist (manual verification)
    ↓
PartitionGuardian (backup partition table)
    ↓
BootGuardian (check bootloader)
    ↓
FlashAuditor (initialize logging)
    ↓
Setup Complete!
```

**Example 2: Install Recovery**
```
MasterControl
    ↓
Check ADB/Fastboot connection
    ↓
Verify bootloader unlocked (BootGuardian)
    ↓
Create partition backup (PartitionGuardian)
    ↓
Install recovery (RecoveryManager)
    ↓
Log operation (FlashAuditor)
    ↓
Installation Complete!
```

**Example 3: ROM Validation**
```
MasterControl
    ↓
Get ROM file path
    ↓
Extract ROM metadata (ROMValidator)
    ↓
Compare with device profile (DeviceProbe)
    ↓
Check compatibility (ROMValidator)
    ↓
Verify bootloader requirements (BootGuardian)
    ↓
Go/No-Go Decision!
```

---

## 📁 File Structure

```
MasterControl/
├── master_control.py          # Main application
├── README.md                   # This file
├── QUICKSTART.md              # Quick reference guide
├── LICENSE                     # MIT License
├── examples/
│   ├── example_beginner.py    # Beginner mode examples
│   ├── example_advanced.py    # Advanced mode examples
│   └── example_workflow.py    # Custom workflow examples
└── docs/
    ├── ARCHITECTURE.md        # Technical architecture
    ├── WORKFLOWS.md           # Workflow documentation
    └── CUSTOMIZATION.md       # Customization guide
```

### Configuration Files

MasterControl stores configuration in:
```
~/xda-toolkit/
├── master_config.json         # User preferences
├── device_history.json        # Device modification history
└── backups/                   # Backup storage
    └── YYYYMMDD_HHMMSS/      # Timestamped backups
```

---

## 🎯 Use Cases

### Use Case 1: Complete Beginner
**Scenario:** Never modified Android device before

**Workflow:**
1. Launch MasterControl
2. Run "First Time Setup"
3. Follow all prompts carefully
4. Create partition backup
5. Use guided recovery installation
6. Create complete backup before ROM flash
7. Validate ROM before flashing

**Outcome:** Safe, guided experience with maximum hand-holding

---

### Use Case 2: Experienced User
**Scenario:** Flashed many ROMs, knows the process

**Workflow:**
1. Launch MasterControl in Advanced Mode
2. Quick device probe (option 7)
3. Direct launch PartitionGuardian (option 5)
4. Direct launch ROMValidator (option 9)
5. Exit to flash ROM manually

**Outcome:** Quick tool access without unnecessary guidance

---

### Use Case 3: ROM Developer
**Scenario:** Testing new ROM builds

**Workflow:**
1. Use DeviceProbe to verify test device
2. Use ROMValidator to check build compatibility
3. Use FlashAuditor to track test flash history
4. Use BootGuardian to manage A/B slots
5. Quick recovery reinstall via RecoveryManager

**Outcome:** Streamlined testing workflow

---

### Use Case 4: Device Rescue
**Scenario:** Soft-bricked device needs recovery

**Workflow:**
1. Boot device to fastboot/EDL mode
2. Launch MasterControl
3. Use EDL Rescue for emergency recovery
4. Restore partition backup (PartitionGuardian)
5. Reflash stock recovery
6. Restore to working state

**Outcome:** Emergency recovery tools in one place

---

## 🔧 Advanced Usage

### Custom Workflows

Create custom workflows by chaining tools:

```python
from master_control import MasterControl

# Initialize
mc = MasterControl()

# Custom ROM flashing workflow
def safe_rom_flash_workflow(rom_path):
    # 1. Probe device
    mc.launch_tool("DeviceProbe")
    
    # 2. Backup partitions
    mc.launch_tool("PartitionGuardian")
    
    # 3. Validate ROM
    mc.validate_rom_workflow()
    
    # 4. Flash via recovery (manual)
    print("Flash ROM in recovery now...")
    
    # 5. Log the operation
    mc.launch_tool("FlashAuditor")
```

### Mode-Specific Behavior

```python
# Set mode programmatically
mc = MasterControl()
mc.mode = "advanced"  # or "beginner"
mc._save_config()
```

### Dashboard Customization

Extend the dashboard to show custom info:

```python
def show_custom_dashboard(self):
    self.print_header()
    # Add custom status displays
    print("Custom Status: XYZ")
    # ... rest of dashboard
```

---

## 📊 Statistics & Metrics

### Code Metrics
- **Lines of Code:** 1,000+
- **Functions:** 25+
- **UI Elements:** 10+ screens
- **Workflow Chains:** 4 guided workflows
- **Safety Checks:** 15+ validation points

### Feature Coverage
- ✅ Device detection (ADB/Fastboot)
- ✅ Tool availability tracking
- ✅ Configuration persistence
- ✅ Beginner/Advanced modes
- ✅ Interactive menus
- ✅ Safety checklists
- ✅ Guided workflows
- ✅ Tool orchestration
- ✅ Beautiful terminal UI
- ✅ Error handling

---

## 🤝 Integration with Other Tools

### PartitionGuardian Integration
- Auto-backup before risky operations
- Backup verification in workflows
- Emergency restore quick access

### RecoveryManager Integration
- Guided installation workflow
- Pre-installation safety checks
- Post-installation verification

### DeviceProbe Integration
- Auto device detection
- Profile storage for quick lookup
- Compatibility checking

### BootGuardian Integration
- Bootloader status verification
- A/B slot management
- Boot chain validation

### ROMValidator Integration
- Pre-flash validation workflow
- Compatibility checking
- Safety recommendations

### FlashAuditor Integration
- Automatic operation logging
- Modification history tracking
- Audit trail generation

### EDL Rescue Integration
- Emergency mode quick access
- Brick recovery workflows
- Emergency procedures

---

## 🐛 Troubleshooting

### Issue: Device Not Detected

**Symptoms:**
- Dashboard shows "Disconnected"
- Cannot proceed with operations

**Solutions:**
1. Check USB cable connection
2. Enable USB debugging on device
3. Accept USB debugging prompt
4. Try different USB port
5. Restart ADB: `adb kill-server && adb start-server`

---

### Issue: Tools Not Available

**Symptoms:**
- Tools marked with ✗ in menu
- "Tool not available" message

**Solutions:**
1. Install missing tools from GitHub
2. Place tools in `~/xda-toolkit/`
3. Ensure tool scripts are executable
4. Restart MasterControl

---

### Issue: Bootloader Status Unknown

**Symptoms:**
- Cannot verify bootloader state
- Warnings about locked bootloader

**Solutions:**
1. Boot device to fastboot mode
2. Run: `fastboot oem device-info`
3. Check bootloader lock status
4. If locked, consider unlocking (WARNING: wipes data)

---

### Issue: Mode Toggle Not Working

**Symptoms:**
- Mode doesn't change
- Settings not persisting

**Solutions:**
1. Check file permissions on `~/xda-toolkit/`
2. Ensure config file is writable
3. Delete config and restart (resets to beginner mode)

---

## 🚀 Advanced Features

### Keyboard Shortcuts
- `Ctrl+C` - Safe exit at any time
- `0` - Return to menu / Exit
- Number keys - Quick menu selection

### Batch Operations
Run multiple operations in sequence without returning to menu (Advanced Mode)

### Custom Tool Paths
Configure custom tool installation locations:
```json
{
  "tool_paths": {
    "partition_guardian": "/custom/path/partition_guardian.py"
  }
}
```

### Logging
All operations logged to:
```
~/xda-toolkit/logs/mastercontrol_YYYYMMDD.log
```

---

## 📚 Documentation

### Included Documentation
- `README.md` - This file (comprehensive guide)
- `QUICKSTART.md` - Quick reference
- `examples/` - Usage examples
- `docs/` - Extended documentation

### External Resources
- **XDA Thread:** [Coming Soon]
- **GitHub Wiki:** Documentation, FAQs, troubleshooting
- **Video Tutorials:** [Planned]
- **Community Forum:** Questions and support

---

## 🏆 Project Goals

### Achieved ✅
- [x] Unified interface for all 7 tools
- [x] Beginner and advanced modes
- [x] Guided workflows
- [x] Safety checkpoints
- [x] Beautiful terminal UI
- [x] Zero external dependencies
- [x] Configuration persistence
- [x] Tool integration architecture

### In Progress 🔄
- [ ] Video tutorials
- [ ] Community workflow templates
- [ ] Plugin system for custom tools
- [ ] Web-based interface option

### Future Plans 🎯
- [ ] Desktop GUI version
- [ ] Mobile companion app
- [ ] Cloud backup integration
- [ ] Community workflow sharing

---

## 🤝 Contributing

We welcome contributions!

### How to Contribute
1. **Report Bugs** - Open GitHub issue
2. **Suggest Features** - Share your ideas
3. **Improve Docs** - Submit documentation updates
4. **Code Contributions** - Submit pull requests
5. **Share Workflows** - Contribute custom workflows

### Contribution Guidelines
- Follow existing code style
- Add comments for complex logic
- Test on multiple devices
- Update documentation
- Follow safety-first principles

---

## 📄 License

```
MIT License

Copyright (c) 2026 XDA Master Toolkit Contributors

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

### Special Thanks
- XDA Developers community
- All 7 toolkit contributors
- Beta testers and early adopters
- Documentation reviewers
- Everyone who provided feedback

### Powered By
- Python standard library (zero dependencies!)
- ADB/Fastboot (Android Platform Tools)
- The XDA community spirit

---

## 📞 Support & Contact

### Get Help
- **GitHub Issues:** Bug reports and feature requests
- **XDA Thread:** Community discussion
- **Documentation:** Comprehensive guides included
- **Email:** [Coming Soon]

### Links
- **GitHub:** https://github.com/XDA-Master-Toolkit/MasterControl
- **Project Site:** https://github.com/XDA-Master-Toolkit
- **XDA Forum:** [Coming Soon]

---

## 🌟 Star the Project

If MasterControl makes your Android modding safer and easier, please:
- ⭐ Star the repository
- 🔄 Share with the community
- 📝 Contribute improvements
- 💬 Provide feedback

**Together, we're making Android modification safer for everyone!**

---

*Last Updated: February 10, 2026*
*Version: 1.0.0*
*Made with ❤️ by the XDA Community*
