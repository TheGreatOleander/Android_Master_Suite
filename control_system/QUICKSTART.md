# MasterControl - Quick Start Guide ⚡

**Get Started in 5 Minutes**

---

## 🎯 What Is This?

MasterControl is the **unified hub** for all XDA Master Toolkit tools. One interface, 7 tools, infinite possibilities.

---

## 🚀 Installation (30 Seconds)

```bash
# 1. Download
git clone https://github.com/XDA-Master-Toolkit/MasterControl.git
cd MasterControl

# 2. Make executable
chmod +x master_control.py

# 3. Run
python3 master_control.py
```

**That's it!** Zero dependencies, pure Python standard library.

---

## 📱 Connect Your Device

### Enable USB Debugging
1. Go to **Settings → About Phone**
2. Tap **Build Number** 7 times (enables Developer Options)
3. Go to **Settings → Developer Options**
4. Enable **USB Debugging**
5. Connect device via USB
6. Accept the prompt on your device

### Verify Connection
```bash
# Check ADB connection
adb devices

# Should show:
# List of devices attached
# ABC123456    device
```

---

## 🎮 First Run

### Launch MasterControl
```bash
python3 master_control.py
```

You'll see:
```
╔══════════════════════════════════════════════════════════════╗
║              XDA MASTER TOOLKIT - MASTERCONTROL              ║
║          Unified Interface for Android Modification          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎓 For Beginners: Your First Time

### Step 1: First Time Setup (Recommended)
Select option **1** from the main menu.

This wizard will:
1. ✅ Detect your device
2. ✅ Run safety checklist
3. ✅ Create partition backup
4. ✅ Check bootloader status
5. ✅ Set up audit logging

**Follow all prompts carefully!**

### Step 2: What's Next?

After setup, you can:
- **Install custom recovery** (option 2)
- **Create complete backup** (option 3)
- **Validate a ROM** (option 4)

---

## 🔥 For Advanced Users

### Direct Tool Access

Select from options 5-11 to launch tools directly:

- **5** - PartitionGuardian
- **6** - RecoveryManager
- **7** - DeviceProbe
- **8** - BootGuardian
- **9** - ROMValidator
- **10** - FlashAuditor
- **11** - EDL Rescue

### Switch to Advanced Mode

Select option **12** to toggle between modes:
- **Beginner:** Guided workflows with safety prompts
- **Advanced:** Direct access, fewer confirmations

---

## 🎯 Common Tasks

### Task 1: Install TWRP Recovery

```
1. Launch MasterControl
2. Select "2. Install Custom Recovery"
3. Confirm bootloader unlocked
4. Choose TWRP
5. Confirm backup creation
6. Wait for installation
7. Reboot to recovery to verify
```

### Task 2: Validate a ROM Before Flashing

```
1. Launch MasterControl
2. Select "4. Validate ROM Before Flash"
3. Enter path to ROM zip file
4. Wait for validation checks
5. Review results
6. Flash if all checks pass ✅
```

### Task 3: Create Complete Backup

```
1. Launch MasterControl
2. Select "3. Backup Everything"
3. Confirm backup location
4. Wait for backup completion
5. Store backup safely!
```

### Task 4: Profile Your Device

```
1. Launch MasterControl
2. Select "7. DeviceProbe"
3. Review device information
4. Export profile (optional)
```

---

## ⚠️ Critical Safety Rules

### BEFORE You Start

✅ **Must Have:**
- Battery above 50%
- Important data backed up
- Stock ROM downloaded
- USB cable in good condition

❌ **Never Do:**
- Flash files for different device
- Skip backups
- Proceed if unsure
- Use untrusted sources

### Golden Rule
**When in doubt, STOP and ask for help!**

---

## 🎨 Understanding the Interface

### Status Indicators
- ✓ **Green** - Available, success, confirmed
- ⚠ **Yellow** - Warning, caution required
- ✗ **Red** - Error, unavailable, failed
- ○ **Gray** - Not installed, inactive

### Menu Navigation
- Type the **number** of your choice
- Press **Enter** to confirm
- Type **0** to exit or go back
- Press **Ctrl+C** to exit safely anytime

---

## 📊 Dashboard Explained

```
📊 Device Status Dashboard
────────────────────────────────────────────────────────────────

Connection:
  ● Connected (ADB Mode)          ← Your device status

Device Information:
  Model: OnePlus 9 Pro            ← Auto-detected
  Codename: lemonadep
  Android: 14
  Bootloader: Unlocked            ← Critical info!

Available Tools:
  ✓ PartitionGuardian             ← Green = installed
  ✓ RecoveryManager
  ○ DeviceProbe                   ← Gray = not installed

  (2/7 tools available)           ← Installation status
```

---

## 🛠️ The 7 Tools (Quick Reference)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **PartitionGuardian** | Backup partition tables | Before ANY modification |
| **RecoveryManager** | Install custom recovery | Installing TWRP, OrangeFox |
| **DeviceProbe** | Profile device | First time, compatibility checks |
| **BootGuardian** | Manage bootloader | A/B slot management, boot issues |
| **ROMValidator** | Check ROM compatibility | Before flashing ROM |
| **FlashAuditor** | Track modifications | Audit trail, history tracking |
| **EDL Rescue** | Emergency recovery | Hard brick, emergency mode |

---

## 🔥 Quick Commands

### Check Device Connection
```bash
adb devices                    # Check ADB
fastboot devices              # Check Fastboot
```

### Reboot Commands
```bash
adb reboot                    # Normal reboot
adb reboot recovery          # Reboot to recovery
adb reboot bootloader        # Reboot to fastboot
```

### Common Paths
```bash
~/xda-toolkit/               # Tool installation directory
~/xda-toolkit/backups/       # Backup storage
~/xda-toolkit/master_config.json  # MasterControl settings
```

---

## 🐛 Quick Troubleshooting

### Device Not Detected?
```bash
# Kill and restart ADB
adb kill-server
adb start-server
adb devices

# Check USB cable
# Try different USB port
# Ensure USB debugging enabled
```

### Tool Not Available?
```bash
# Install the missing tool
cd ~/xda-toolkit
git clone https://github.com/XDA-Master-Toolkit/[ToolName].git

# Restart MasterControl
```

### Can't Select Option?
- Type the **number** (not the name)
- Press **Enter** after typing
- Check for typos
- Only valid numbers work

---

## 💡 Pro Tips

### Tip 1: Always Backup First
Use **PartitionGuardian** before ANY modification. It's saved countless devices.

### Tip 2: Understand Before Acting
Read the full description of what each action does. Don't blindly click through.

### Tip 3: Keep Backups Safe
Store backups on PC, not just on device. Cloud storage is great too.

### Tip 4: One Modification at a Time
Don't flash ROM + kernel + mods all at once. Flash one, test, then continue.

### Tip 5: Document Your Changes
Use **FlashAuditor** to track what you've done. Makes troubleshooting easier.

---

## 🎓 Learning Path

### Beginner Path (Recommended)
```
1. First Time Setup
   ↓
2. Install Custom Recovery
   ↓
3. Create Complete Backup
   ↓
4. Flash Your First ROM
   ↓
5. Explore Advanced Features
```

### Advanced Path
```
1. Profile Device (DeviceProbe)
   ↓
2. Direct Tool Access as Needed
   ↓
3. Custom Workflows
   ↓
4. Emergency Recovery Skills
```

---

## 📚 Next Steps

### After This Guide
1. **Read Full README** - Comprehensive documentation
2. **Join XDA Thread** - Community support
3. **Try Individual Tools** - Explore each tool's features
4. **Share Experience** - Help others learn

### Resources
- 📖 Full README: `README.md`
- 💻 GitHub: https://github.com/XDA-Master-Toolkit
- 🌐 XDA Thread: [Coming Soon]
- 📝 Individual Tool Docs: Each tool has its own README

---

## ⚡ TL;DR - Absolute Minimum

```bash
# Install
git clone https://github.com/XDA-Master-Toolkit/MasterControl.git
cd MasterControl

# Run
python3 master_control.py

# First Time?
Select option 1 (First Time Setup)

# Done!
```

---

## 🆘 Need Help?

- **GitHub Issues:** Report bugs
- **XDA Forum:** Ask questions
- **Documentation:** Read README.md
- **Community:** Share experiences

---

## ✅ Quick Checklist

Before your first modification:

- [ ] Device connected and detected
- [ ] USB debugging enabled
- [ ] Battery above 50%
- [ ] Important data backed up
- [ ] Stock ROM downloaded
- [ ] Read safety warnings
- [ ] Understand the process
- [ ] Know how to recover if things go wrong

**All checked? You're ready!** 🚀

---

*Happy Modding! Stay Safe!*

*Made with ❤️ by the XDA Community*
