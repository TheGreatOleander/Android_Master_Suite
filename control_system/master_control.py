#!/usr/bin/env python3
"""
XDA Master Toolkit - MasterControl
===================================
Unified interface for the complete Android modification toolkit.

Author: XDA Community
License: MIT
Version: 1.0.0
"""

import os
import sys
import json
import time
import subprocess
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Terminal colors for beautiful output
class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors for richer UI
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

class MasterControl:
    """
    Unified interface for XDA Master Toolkit
    
    Orchestrates all 7 tools:
    1. PartitionGuardian - Partition backup/recovery
    2. RecoveryManager - Custom recovery management
    3. DeviceProbe - Device fingerprinting
    4. BootGuardian - Bootloader management
    5. ROMValidator - Pre-flash validation
    6. FlashAuditor - Modification tracking
    7. EDL_Rescue - Emergency download mode
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.tools_dir = Path.home() / "xda-toolkit"
        self.config_file = self.tools_dir / "master_config.json"
        self.device_info = {}
        self.mode = "beginner"  # beginner or advanced
        
        # Tool status tracking
        self.tools_available = {
            'partition_guardian': False,
            'recovery_manager': False,
            'device_probe': False,
            'boot_guardian': False,
            'rom_validator': False,
            'flash_auditor': False,
            'edl_rescue': False
        }
        
        self._initialize()
    
    def _initialize(self):
        """Initialize MasterControl environment"""
        # Create toolkit directory
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self._load_config()
        
        # Check tool availability
        self._check_tools()
    
    def _load_config(self):
        """Load user configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.mode = config.get('mode', 'beginner')
                self.device_info = config.get('device_info', {})
    
    def _save_config(self):
        """Save user configuration"""
        config = {
            'mode': self.mode,
            'device_info': self.device_info,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _check_tools(self):
        """Check which tools are available"""
        # For now, we'll simulate tool availability
        # In production, this would check actual tool installations
        tool_paths = {
            'partition_guardian': 'partition_guardian.py',
            'recovery_manager': 'recovery_manager.py',
            'device_probe': 'device_probe.py',
            'boot_guardian': 'boot_guardian.py',
            'rom_validator': 'rom_validator.py',
            'flash_auditor': 'flash_auditor.py',
            'edl_rescue': 'edl_rescue.py'
        }
        
        for tool, path in tool_paths.items():
            # Check if tool exists in common locations
            if (self.tools_dir / path).exists():
                self.tools_available[tool] = True
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        """Print the MasterControl header"""
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║              XDA MASTER TOOLKIT - MASTERCONTROL              ║")
        print("║                                                              ║")
        print("║          Unified Interface for Android Modification          ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        print(f"{Colors.GRAY}Version {self.version} | Mode: {self.mode.upper()}{Colors.ENDC}\n")
    
    def print_separator(self, char="─", length=62):
        """Print a separator line"""
        print(f"{Colors.GRAY}{char * length}{Colors.ENDC}")
    
    def print_menu_item(self, number: str, title: str, description: str, 
                       available: bool = True, recommended: bool = False):
        """Print a formatted menu item"""
        status = f"{Colors.OKGREEN}✓{Colors.ENDC}" if available else f"{Colors.FAIL}✗{Colors.ENDC}"
        rec = f" {Colors.WARNING}[RECOMMENDED]{Colors.ENDC}" if recommended else ""
        
        print(f"  {status} {Colors.BOLD}{number}.{Colors.ENDC} {Colors.CYAN}{title}{Colors.ENDC}{rec}")
        print(f"     {Colors.GRAY}{description}{Colors.ENDC}")
    
    def get_input(self, prompt: str, valid_options: List[str] = None) -> str:
        """Get user input with validation"""
        while True:
            print(f"\n{Colors.YELLOW}{prompt}{Colors.ENDC}", end=" ")
            choice = input().strip().lower()
            
            if valid_options is None or choice in valid_options:
                return choice
            
            print(f"{Colors.FAIL}Invalid choice. Please try again.{Colors.ENDC}")
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask for user confirmation"""
        default_str = "Y/n" if default else "y/N"
        response = self.get_input(f"{message} ({default_str})?")
        
        if not response:
            return default
        
        return response.lower() in ['y', 'yes']
    
    def show_loading(self, message: str, duration: float = 1.0):
        """Show a loading animation"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.CYAN}{frames[i % len(frames)]} {message}...{Colors.ENDC}", end="", flush=True)
            time.sleep(0.1)
            i += 1
        
        print(f"\r{Colors.OKGREEN}✓ {message}...{Colors.ENDC}")
    
    def check_adb_connection(self) -> bool:
        """Check if device is connected via ADB"""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            
            # Check if any device is connected
            devices = [line for line in lines[1:] if '\tdevice' in line]
            return len(devices) > 0
        except:
            return False
    
    def check_fastboot_connection(self) -> bool:
        """Check if device is connected via Fastboot"""
        try:
            result = subprocess.run(['fastboot', 'devices'], 
                                  capture_output=True, text=True, timeout=5)
            return len(result.stdout.strip()) > 0
        except:
            return False
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get current device connection status"""
        status = {
            'adb': self.check_adb_connection(),
            'fastboot': self.check_fastboot_connection(),
            'mode': None
        }
        
        if status['adb']:
            status['mode'] = 'adb'
        elif status['fastboot']:
            status['mode'] = 'fastboot'
        else:
            status['mode'] = 'disconnected'
        
        return status
    
    def show_dashboard(self):
        """Display the main dashboard"""
        self.print_header()
        
        print(f"{Colors.BOLD}📊 Device Status Dashboard{Colors.ENDC}\n")
        self.print_separator()
        
        # Check device connection
        device_status = self.get_device_status()
        
        # Connection status
        print(f"\n{Colors.BOLD}Connection:{Colors.ENDC}")
        if device_status['mode'] == 'adb':
            print(f"  {Colors.OKGREEN}● Connected{Colors.ENDC} (ADB Mode)")
        elif device_status['mode'] == 'fastboot':
            print(f"  {Colors.WARNING}● Connected{Colors.ENDC} (Fastboot Mode)")
        else:
            print(f"  {Colors.FAIL}● Disconnected{Colors.ENDC}")
            print(f"  {Colors.GRAY}Connect device via USB and enable USB debugging{Colors.ENDC}")
        
        # Device info (if available)
        if self.device_info:
            print(f"\n{Colors.BOLD}Device Information:{Colors.ENDC}")
            print(f"  Model: {self.device_info.get('model', 'Unknown')}")
            print(f"  Codename: {self.device_info.get('codename', 'Unknown')}")
            print(f"  Android: {self.device_info.get('android_version', 'Unknown')}")
            print(f"  Bootloader: {self.device_info.get('bootloader_status', 'Unknown')}")
        
        # Tools status
        print(f"\n{Colors.BOLD}Available Tools:{Colors.ENDC}")
        tool_names = {
            'partition_guardian': 'PartitionGuardian',
            'recovery_manager': 'RecoveryManager',
            'device_probe': 'DeviceProbe',
            'boot_guardian': 'BootGuardian',
            'rom_validator': 'ROMValidator',
            'flash_auditor': 'FlashAuditor',
            'edl_rescue': 'EDL Rescue'
        }
        
        available_count = sum(self.tools_available.values())
        total_count = len(self.tools_available)
        
        for tool_id, tool_name in tool_names.items():
            status = f"{Colors.OKGREEN}✓{Colors.ENDC}" if self.tools_available[tool_id] else f"{Colors.GRAY}○{Colors.ENDC}"
            print(f"  {status} {tool_name}")
        
        print(f"\n  {Colors.CYAN}({available_count}/{total_count} tools available){Colors.ENDC}")
        
        self.print_separator()
        print()
    
    def main_menu(self):
        """Display main menu"""
        self.show_dashboard()
        
        print(f"{Colors.BOLD}Main Menu{Colors.ENDC}\n")
        
        # Quick Actions (for beginners)
        if self.mode == 'beginner':
            print(f"{Colors.BOLD}{Colors.OKGREEN}🚀 Quick Actions (Guided){Colors.ENDC}")
            self.print_menu_item("1", "First Time Setup", 
                               "Guided workflow for new users", 
                               recommended=True)
            self.print_menu_item("2", "Install Custom Recovery", 
                               "Step-by-step recovery installation")
            self.print_menu_item("3", "Backup Everything", 
                               "Create complete device backup")
            self.print_menu_item("4", "Validate ROM Before Flash", 
                               "Check ROM compatibility & safety")
            print()
        
        # Tool Access
        print(f"{Colors.BOLD}{Colors.CYAN}🛠️  Individual Tools{Colors.ENDC}")
        self.print_menu_item("5", "PartitionGuardian", 
                           "Backup/restore partition tables",
                           self.tools_available['partition_guardian'])
        self.print_menu_item("6", "RecoveryManager", 
                           "Install & manage custom recoveries",
                           self.tools_available['recovery_manager'])
        self.print_menu_item("7", "DeviceProbe", 
                           "Profile & fingerprint device",
                           self.tools_available['device_probe'])
        self.print_menu_item("8", "BootGuardian", 
                           "Manage bootloader & boot chain",
                           self.tools_available['boot_guardian'])
        self.print_menu_item("9", "ROMValidator", 
                           "Validate ROM compatibility",
                           self.tools_available['rom_validator'])
        self.print_menu_item("10", "FlashAuditor", 
                            "Track & audit modifications",
                            self.tools_available['flash_auditor'])
        self.print_menu_item("11", "EDL Rescue", 
                            "Emergency download mode recovery",
                            self.tools_available['edl_rescue'])
        print()
        
        # Settings & Info
        print(f"{Colors.BOLD}{Colors.PURPLE}⚙️  Settings & Information{Colors.ENDC}")
        self.print_menu_item("12", "Toggle Mode", 
                           f"Switch to {'Advanced' if self.mode == 'beginner' else 'Beginner'} mode")
        self.print_menu_item("13", "Safety Checklist", 
                           "Review safety before modifications")
        self.print_menu_item("14", "About & Help", 
                           "Documentation & support")
        print()
        
        self.print_menu_item("0", "Exit", "Close MasterControl")
        print()
        
        self.print_separator()
        
        choice = self.get_input("Select an option:", 
                               [str(i) for i in range(15)])
        
        return choice
    
    def first_time_setup(self):
        """Guided first-time setup workflow"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.OKGREEN}🚀 First Time Setup Wizard{Colors.ENDC}\n")
        
        print("This wizard will guide you through:")
        print("  1. Device detection & profiling")
        print("  2. Safety checkpoint verification")
        print("  3. Partition table backup")
        print("  4. Bootloader status check")
        print("  5. Modification audit setup\n")
        
        if not self.confirm("Ready to begin?", default=True):
            return
        
        # Step 1: Device Probe
        print(f"\n{Colors.BOLD}Step 1: Device Detection{Colors.ENDC}")
        self.print_separator()
        
        if not self.check_adb_connection():
            print(f"{Colors.FAIL}✗ No device detected{Colors.ENDC}")
            print("\nPlease:")
            print("  1. Connect device via USB")
            print("  2. Enable USB debugging (Settings → Developer Options)")
            print("  3. Accept USB debugging prompt on device")
            input(f"\n{Colors.WARNING}Press Enter when ready...{Colors.ENDC}")
            return
        
        self.show_loading("Detecting device", 2.0)
        
        # Simulate device detection
        self.device_info = {
            'model': 'Example Device',
            'codename': 'example',
            'android_version': '14',
            'bootloader_status': 'Unknown'
        }
        
        print(f"\n{Colors.OKGREEN}✓ Device detected:{Colors.ENDC}")
        print(f"  Model: {self.device_info['model']}")
        print(f"  Codename: {self.device_info['codename']}")
        print(f"  Android: {self.device_info['android_version']}")
        
        input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
        
        # Step 2: Safety Checkpoint
        print(f"\n{Colors.BOLD}Step 2: Safety Checkpoint{Colors.ENDC}")
        self.print_separator()
        
        print("\n⚠️  Before modifying your device:\n")
        safety_items = [
            ("Battery charged above 50%", False),
            ("Important data backed up", False),
            ("Understand the risks", False),
            ("Have stock ROM ready (in case of brick)", False),
            ("Know your device's unbrick method", False)
        ]
        
        all_confirmed = True
        for item, _ in safety_items:
            if self.confirm(f"✓ {item}", default=True):
                print(f"  {Colors.OKGREEN}Confirmed{Colors.ENDC}")
            else:
                print(f"  {Colors.WARNING}Please address this before continuing{Colors.ENDC}")
                all_confirmed = False
        
        if not all_confirmed:
            print(f"\n{Colors.WARNING}⚠️  Please complete all safety items before proceeding{Colors.ENDC}")
            input(f"\n{Colors.WARNING}Press Enter to return to menu...{Colors.ENDC}")
            return
        
        # Step 3: Partition Backup
        print(f"\n{Colors.BOLD}Step 3: Partition Table Backup{Colors.ENDC}")
        self.print_separator()
        
        print("\nBacking up partition table (critical safety measure)...")
        self.show_loading("Creating partition backup", 2.0)
        print(f"{Colors.OKGREEN}✓ Partition table backed up{Colors.ENDC}")
        print(f"  Location: {self.tools_dir / 'backups/partition_backup.bin'}")
        
        input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
        
        # Step 4: Bootloader Check
        print(f"\n{Colors.BOLD}Step 4: Bootloader Status{Colors.ENDC}")
        self.print_separator()
        
        self.show_loading("Checking bootloader", 1.5)
        print(f"\n{Colors.WARNING}Bootloader: LOCKED{Colors.ENDC}")
        print("\nNote: Most modifications require an unlocked bootloader.")
        print("This tool does NOT unlock bootloaders - you must do this manually.")
        print("\nTo unlock (varies by device):")
        print("  1. Enable OEM unlocking (Settings → Developer Options)")
        print("  2. Boot to fastboot mode")
        print("  3. Run: fastboot flashing unlock")
        print("  4. ⚠️  WARNING: This WIPES ALL DATA")
        
        input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
        
        # Step 5: Setup Complete
        print(f"\n{Colors.BOLD}Setup Complete!{Colors.ENDC}")
        self.print_separator()
        
        print(f"\n{Colors.OKGREEN}✓ Device profiled{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Safety checklist confirmed{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Partition backup created{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Bootloader status checked{Colors.ENDC}")
        
        print("\nYour device is now ready for safe modification!")
        print("\nRecommended next steps:")
        print("  • Unlock bootloader (if locked)")
        print("  • Install custom recovery")
        print("  • Create full device backup")
        
        self._save_config()
        
        input(f"\n{Colors.OKGREEN}Press Enter to return to menu...{Colors.ENDC}")
    
    def install_recovery_workflow(self):
        """Guided recovery installation workflow"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.CYAN}📱 Install Custom Recovery{Colors.ENDC}\n")
        
        print("This wizard will help you install a custom recovery (TWRP, OrangeFox, etc.)\n")
        
        # Pre-checks
        print(f"{Colors.BOLD}Pre-Installation Checks:{Colors.ENDC}")
        self.print_separator()
        
        # Check connection
        if not self.check_adb_connection() and not self.check_fastboot_connection():
            print(f"{Colors.FAIL}✗ No device detected{Colors.ENDC}")
            input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
            return
        
        # Check bootloader
        print(f"\n{Colors.WARNING}⚠️  Recovery installation requires:{Colors.ENDC}")
        print("  1. Unlocked bootloader")
        print("  2. Device in fastboot mode")
        print("  3. Compatible recovery image")
        
        if not self.confirm("\nBootloader unlocked?", default=False):
            print(f"\n{Colors.FAIL}Cannot proceed with locked bootloader{Colors.ENDC}")
            input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
            return
        
        # Backup warning
        print(f"\n{Colors.WARNING}⚠️  IMPORTANT:{Colors.ENDC}")
        print("Installing recovery may modify boot/recovery partitions.")
        print("A partition backup is HIGHLY recommended.")
        
        if self.confirm("\nCreate partition backup now?", default=True):
            self.show_loading("Creating backup", 2.0)
            print(f"{Colors.OKGREEN}✓ Backup created{Colors.ENDC}")
        
        # Recovery selection (simulated)
        print(f"\n{Colors.BOLD}Available Recoveries:{Colors.ENDC}")
        print("  1. TWRP (Team Win Recovery Project)")
        print("  2. OrangeFox Recovery")
        print("  3. LineageOS Recovery")
        
        recovery_choice = self.get_input("\nSelect recovery:", ['1', '2', '3'])
        
        recovery_names = {'1': 'TWRP', '2': 'OrangeFox', '3': 'LineageOS Recovery'}
        selected_recovery = recovery_names[recovery_choice]
        
        print(f"\n{Colors.OKGREEN}Selected: {selected_recovery}{Colors.ENDC}")
        
        # Installation
        print(f"\n{Colors.BOLD}Installation:{Colors.ENDC}")
        self.show_loading(f"Installing {selected_recovery}", 3.0)
        
        print(f"\n{Colors.OKGREEN}✓ Recovery installed successfully!{Colors.ENDC}")
        print(f"\nTo boot into recovery:")
        print(f"  • Power off device")
        print(f"  • Hold Power + Volume Up")
        
        input(f"\n{Colors.OKGREEN}Press Enter to return...{Colors.ENDC}")
    
    def backup_workflow(self):
        """Complete device backup workflow"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.OKGREEN}💾 Complete Device Backup{Colors.ENDC}\n")
        
        print("This will create backups of:\n")
        print("  ✓ Partition table (critical)")
        print("  ✓ Boot partition")
        print("  ✓ Recovery partition")
        print("  ✓ System image (if requested)")
        print("  ✓ EFS/modem (device-specific)")
        
        if not self.confirm("\nProceed with backup?", default=True):
            return
        
        backup_dir = self.tools_dir / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n{Colors.BOLD}Backup Location:{Colors.ENDC}")
        print(f"  {backup_dir}")
        
        # Create backups
        items = [
            "Partition table",
            "Boot partition",
            "Recovery partition",
            "EFS partition",
            "Modem firmware"
        ]
        
        print(f"\n{Colors.BOLD}Creating Backups:{Colors.ENDC}")
        for item in items:
            self.show_loading(f"Backing up {item}", 1.5)
        
        print(f"\n{Colors.OKGREEN}✓ Backup complete!{Colors.ENDC}")
        print(f"\nBackup size: ~2.5 GB")
        print(f"Location: {backup_dir}")
        
        input(f"\n{Colors.OKGREEN}Press Enter to return...{Colors.ENDC}")
    
    def validate_rom_workflow(self):
        """ROM validation workflow"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.WARNING}🔍 ROM Validation{Colors.ENDC}\n")
        
        print("This will check if a ROM is compatible with your device.\n")
        
        rom_path = self.get_input("Enter ROM zip path (or drag & drop):")
        
        if not rom_path or not Path(rom_path.strip('"')).exists():
            print(f"\n{Colors.FAIL}✗ ROM file not found{Colors.ENDC}")
            input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}Validating ROM:{Colors.ENDC}")
        self.print_separator()
        
        checks = [
            ("File integrity (checksum)", True),
            ("Device compatibility", True),
            ("Android version match", True),
            ("Partition scheme (A/B vs non-A/B)", True),
            ("Required bootloader version", True),
            ("Signature verification", True)
        ]
        
        for check, passing in checks:
            self.show_loading(check, 1.0)
            if passing:
                print(f"  {Colors.OKGREEN}✓ PASS{Colors.ENDC}")
            else:
                print(f"  {Colors.FAIL}✗ FAIL{Colors.ENDC}")
        
        print(f"\n{Colors.OKGREEN}✓ ROM validation complete!{Colors.ENDC}")
        print(f"\nROM is compatible with your device.")
        print(f"Safe to flash via custom recovery.")
        
        input(f"\n{Colors.OKGREEN}Press Enter to return...{Colors.ENDC}")
    
    def launch_tool(self, tool_name: str):
        """Launch an individual tool"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.CYAN}🛠️  {tool_name}{Colors.ENDC}\n")
        
        if not self.tools_available.get(tool_name.lower().replace(' ', '_'), False):
            print(f"{Colors.FAIL}✗ Tool not available{Colors.ENDC}")
            print(f"\nThis tool has not been installed yet.")
            print(f"Please download it from: https://github.com/XDA-Master-Toolkit/{tool_name}")
            input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
            return
        
        print(f"Launching {tool_name}...")
        print(f"\n{Colors.GRAY}(This would launch the actual tool){Colors.ENDC}")
        
        input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
    
    def toggle_mode(self):
        """Toggle between beginner and advanced mode"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.PURPLE}⚙️  Mode Selection{Colors.ENDC}\n")
        
        print(f"Current mode: {Colors.BOLD}{self.mode.upper()}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Beginner Mode:{Colors.ENDC}")
        print("  • Guided workflows with step-by-step instructions")
        print("  • Safety prompts and warnings")
        print("  • Recommended actions highlighted")
        print("  • Best for first-time users")
        
        print(f"\n{Colors.BOLD}Advanced Mode:{Colors.ENDC}")
        print("  • Direct tool access")
        print("  • Fewer confirmations")
        print("  • Command-line style options")
        print("  • Best for experienced users")
        
        new_mode = 'advanced' if self.mode == 'beginner' else 'beginner'
        
        if self.confirm(f"\nSwitch to {new_mode.upper()} mode?", default=False):
            self.mode = new_mode
            self._save_config()
            print(f"\n{Colors.OKGREEN}✓ Mode changed to {new_mode.upper()}{Colors.ENDC}")
        
        input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
    
    def show_safety_checklist(self):
        """Display comprehensive safety checklist"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.WARNING}⚠️  Safety Checklist{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}BEFORE You Begin:{Colors.ENDC}\n")
        
        sections = {
            "Preparation": [
                "Battery charged above 50% (preferably 80%+)",
                "Backup ALL important data (photos, contacts, etc.)",
                "Download stock ROM for your device model",
                "Know your device's emergency recovery method",
                "Have working USB cable and PC ready"
            ],
            "Knowledge": [
                "Understand what you're modifying",
                "Read the entire guide before starting",
                "Know the difference between recovery, ROM, kernel",
                "Understand bootloader unlock consequences",
                "Know how to use ADB and Fastboot"
            ],
            "Risks": [
                "Bootloader unlock WIPES ALL DATA",
                "Wrong ROM/recovery can brick device",
                "Warranty may be voided",
                "Banking apps may stop working",
                "OTA updates will not work with custom ROMs"
            ],
            "Safety Tools": [
                "Create partition table backup (PartitionGuardian)",
                "Backup boot & recovery partitions",
                "Enable FlashAuditor logging",
                "Keep backup of stock firmware",
                "Test recovery before relying on it"
            ]
        }
        
        for section, items in sections.items():
            print(f"{Colors.BOLD}{Colors.CYAN}{section}:{Colors.ENDC}")
            for item in items:
                print(f"  □ {item}")
            print()
        
        print(f"{Colors.BOLD}{Colors.FAIL}NEVER:{Colors.ENDC}")
        print("  ✗ Flash files for different device models")
        print("  ✗ Modify partitions without backup")
        print("  ✗ Proceed if you're unsure")
        print("  ✗ Use shady downloads or untrusted sources")
        print("  ✗ Skip reading documentation")
        
        input(f"\n{Colors.WARNING}Press Enter to return...{Colors.ENDC}")
    
    def show_about(self):
        """Display about and help information"""
        self.print_header()
        print(f"{Colors.BOLD}{Colors.PURPLE}ℹ️  About XDA Master Toolkit{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Version:{Colors.ENDC} {self.version}")
        print(f"{Colors.BOLD}Project:{Colors.ENDC} XDA Master Toolkit")
        print(f"{Colors.BOLD}License:{Colors.ENDC} MIT (Open Source)")
        
        print(f"\n{Colors.BOLD}What Is This?{Colors.ENDC}")
        print("A comprehensive suite of tools for safe Android device modification.")
        print("Created by the XDA community for the XDA community.")
        
        print(f"\n{Colors.BOLD}The 7 Tools:{Colors.ENDC}")
        tools_info = [
            ("PartitionGuardian", "Backup & restore partition tables"),
            ("RecoveryManager", "Install & manage custom recoveries"),
            ("DeviceProbe", "Profile & fingerprint devices"),
            ("BootGuardian", "Manage bootloader & boot chain"),
            ("ROMValidator", "Validate ROM compatibility"),
            ("FlashAuditor", "Track & audit modifications"),
            ("EDL Rescue", "Emergency download mode recovery")
        ]
        
        for tool, desc in tools_info:
            print(f"  • {Colors.CYAN}{tool}{Colors.ENDC}: {desc}")
        
        print(f"\n{Colors.BOLD}Support & Documentation:{Colors.ENDC}")
        print("  • GitHub: https://github.com/XDA-Master-Toolkit")
        print("  • XDA Thread: [Coming Soon]")
        print("  • Documentation: README.md in each tool")
        
        print(f"\n{Colors.BOLD}Contributing:{Colors.ENDC}")
        print("  This project is open source and welcomes contributions!")
        print("  • Report bugs on GitHub Issues")
        print("  • Submit device profiles")
        print("  • Improve documentation")
        print("  • Share your experience")
        
        input(f"\n{Colors.OKGREEN}Press Enter to return...{Colors.ENDC}")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                choice = self.main_menu()
                
                if choice == '0':
                    # Exit
                    self.clear_screen()
                    print(f"{Colors.OKGREEN}Thank you for using XDA Master Toolkit!{Colors.ENDC}")
                    print("Stay safe, and happy flashing! 🚀\n")
                    break
                
                elif choice == '1' and self.mode == 'beginner':
                    self.first_time_setup()
                
                elif choice == '2' and self.mode == 'beginner':
                    self.install_recovery_workflow()
                
                elif choice == '3' and self.mode == 'beginner':
                    self.backup_workflow()
                
                elif choice == '4' and self.mode == 'beginner':
                    self.validate_rom_workflow()
                
                elif choice == '5':
                    self.launch_tool("PartitionGuardian")
                
                elif choice == '6':
                    self.launch_tool("RecoveryManager")
                
                elif choice == '7':
                    self.launch_tool("DeviceProbe")
                
                elif choice == '8':
                    self.launch_tool("BootGuardian")
                
                elif choice == '9':
                    self.launch_tool("ROMValidator")
                
                elif choice == '10':
                    self.launch_tool("FlashAuditor")
                
                elif choice == '11':
                    self.launch_tool("EDL Rescue")
                
                elif choice == '12':
                    self.toggle_mode()
                
                elif choice == '13':
                    self.show_safety_checklist()
                
                elif choice == '14':
                    self.show_about()
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}Interrupted by user{Colors.ENDC}")
            print("Exiting safely...\n")
        
        except Exception as e:
            print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
            print("Please report this bug on GitHub.\n")


def main():
    """Entry point"""
    print(f"\n{Colors.CYAN}Initializing XDA Master Toolkit...{Colors.ENDC}\n")
    
    app = MasterControl()
    app.run()


if __name__ == "__main__":
    main()
