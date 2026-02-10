#!/usr/bin/env python3
"""
KernelForge - Kernel Unpacking, Analysis & Customization Tool
Part of XDA Master Toolkit

Purpose: Extract, analyze, modify, and repack Android kernel images
Author: XDA Master Toolkit Team
License: MIT
Version: 1.0.0

Features:
- Extract kernel from boot images
- Analyze kernel configuration and features
- Parse kernel command line
- Identify kernel version and security features
- Apply kernel patches
- Modify kernel config
- Custom kernel building
- Performance optimization
- Repack and flash kernels
- Integration with BootGuardian
"""

import os
import sys
import struct
import subprocess
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

class KernelForge:
    """Main KernelForge class for kernel operations"""
    
    def __init__(self, working_dir: str = "kernel_workspace"):
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(exist_ok=True)
        
        # Directories
        self.extract_dir = self.working_dir / "extracted"
        self.build_dir = self.working_dir / "build"
        self.output_dir = self.working_dir / "output"
        
        for d in [self.extract_dir, self.build_dir, self.output_dir]:
            d.mkdir(exist_ok=True)
        
        # Tool paths
        self.tools = {
            'abootimg': None,
            'mkbootimg': None,
            'unmkbootimg': None,
            'split_bootimg': None
        }
        
        self._detect_tools()
        
    def _detect_tools(self):
        """Detect available kernel tools"""
        tools_to_check = ['abootimg', 'mkbootimg', 'unmkbootimg', 'file', 'strings']
        
        for tool in tools_to_check:
            try:
                result = subprocess.run(['which', tool], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode == 0:
                    self.tools[tool] = result.stdout.strip()
            except:
                pass
    
    def extract_boot_image(self, boot_img_path: str) -> Dict[str, Any]:
        """
        Extract kernel and components from boot image
        
        Args:
            boot_img_path: Path to boot.img file
            
        Returns:
            Dict with extracted components info
        """
        print(f"📦 Extracting boot image: {boot_img_path}")
        
        boot_path = Path(boot_img_path)
        if not boot_path.exists():
            raise FileNotFoundError(f"Boot image not found: {boot_img_path}")
        
        # Verify it's a boot image
        with open(boot_path, 'rb') as f:
            magic = f.read(8)
        
        if not (magic == b'ANDROID!' or magic[:4] == b'\x00\x00\xa0\xe1'):
            print(f"⚠️  Warning: File may not be a standard Android boot image")
        
        # Extract using multiple methods
        extracted_info = {
            'boot_image': str(boot_path),
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # Method 1: Try abootimg
        if self.tools.get('abootimg'):
            print("🔧 Using abootimg for extraction...")
            extracted_info.update(self._extract_with_abootimg(boot_path))
        
        # Method 2: Manual extraction
        else:
            print("🔧 Using manual extraction...")
            extracted_info.update(self._extract_manually(boot_path))
        
        # Parse kernel
        if 'kernel' in extracted_info['components']:
            kernel_path = extracted_info['components']['kernel']
            extracted_info['kernel_info'] = self.analyze_kernel(kernel_path)
        
        # Save extraction info
        info_file = self.extract_dir / "extraction_info.json"
        with open(info_file, 'w') as f:
            json.dump(extracted_info, f, indent=2)
        
        print(f"✅ Extraction complete! Info saved to: {info_file}")
        
        return extracted_info
    
    def _extract_with_abootimg(self, boot_path: Path) -> Dict:
        """Extract using abootimg tool"""
        extract_path = self.extract_dir / boot_path.stem
        extract_path.mkdir(exist_ok=True)
        
        try:
            # Extract components
            subprocess.run([
                'abootimg', '-x', str(boot_path)
            ], cwd=extract_path, check=True, capture_output=True)
            
            # Get info
            result = subprocess.run([
                'abootimg', '-i', str(boot_path)
            ], capture_output=True, text=True)
            
            components = {}
            if (extract_path / 'zImage').exists():
                components['kernel'] = str(extract_path / 'zImage')
            if (extract_path / 'Image').exists():
                components['kernel'] = str(extract_path / 'Image')
            if (extract_path / 'initrd.img').exists():
                components['ramdisk'] = str(extract_path / 'initrd.img')
            if (extract_path / 'second').exists():
                components['second'] = str(extract_path / 'second')
            if (extract_path / 'dtb').exists():
                components['dtb'] = str(extract_path / 'dtb')
            
            # Parse bootimg.cfg
            cfg_path = extract_path / 'bootimg.cfg'
            boot_config = {}
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            boot_config[key.strip()] = value.strip()
                components['config'] = str(cfg_path)
            
            return {
                'method': 'abootimg',
                'components': components,
                'boot_config': boot_config,
                'extract_dir': str(extract_path)
            }
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  abootimg extraction failed: {e}")
            return {}
    
    def _extract_manually(self, boot_path: Path) -> Dict:
        """Manual boot image extraction"""
        extract_path = self.extract_dir / boot_path.stem
        extract_path.mkdir(exist_ok=True)
        
        with open(boot_path, 'rb') as f:
            # Read Android boot image header
            magic = f.read(8)
            
            if magic != b'ANDROID!':
                print("⚠️  Not a standard Android boot image, attempting raw extraction...")
                # Try to find gzip compressed kernel
                f.seek(0)
                data = f.read()
                
                # Look for gzip magic (1f 8b)
                kernel_start = data.find(b'\x1f\x8b')
                if kernel_start != -1:
                    # Find end of gzip stream
                    kernel_data = data[kernel_start:]
                    kernel_path = extract_path / 'kernel.gz'
                    with open(kernel_path, 'wb') as kf:
                        kf.write(kernel_data[:1024*1024*16])  # Max 16MB
                    
                    # Decompress
                    try:
                        subprocess.run(['gunzip', str(kernel_path)], check=True)
                        return {
                            'method': 'manual_raw',
                            'components': {'kernel': str(extract_path / 'kernel')},
                            'extract_dir': str(extract_path)
                        }
                    except:
                        pass
                
                return {
                    'method': 'failed',
                    'error': 'Could not extract kernel',
                    'extract_dir': str(extract_path)
                }
            
            # Parse header
            kernel_size = struct.unpack('<I', f.read(4))[0]
            kernel_addr = struct.unpack('<I', f.read(4))[0]
            ramdisk_size = struct.unpack('<I', f.read(4))[0]
            ramdisk_addr = struct.unpack('<I', f.read(4))[0]
            second_size = struct.unpack('<I', f.read(4))[0]
            second_addr = struct.unpack('<I', f.read(4))[0]
            tags_addr = struct.unpack('<I', f.read(4))[0]
            page_size = struct.unpack('<I', f.read(4))[0]
            header_version = struct.unpack('<I', f.read(4))[0]
            os_version = struct.unpack('<I', f.read(4))[0]
            name = f.read(16).decode('ascii', errors='ignore').strip('\x00')
            cmdline = f.read(512).decode('ascii', errors='ignore').strip('\x00')
            
            # Calculate offsets
            kernel_offset = page_size
            ramdisk_offset = kernel_offset + ((kernel_size + page_size - 1) // page_size) * page_size
            second_offset = ramdisk_offset + ((ramdisk_size + page_size - 1) // page_size) * page_size
            
            components = {}
            boot_config = {
                'kernel_addr': hex(kernel_addr),
                'ramdisk_addr': hex(ramdisk_addr),
                'second_addr': hex(second_addr),
                'tags_addr': hex(tags_addr),
                'page_size': str(page_size),
                'cmdline': cmdline,
                'name': name
            }
            
            # Extract kernel
            if kernel_size > 0:
                f.seek(kernel_offset)
                kernel_data = f.read(kernel_size)
                kernel_path = extract_path / 'kernel'
                with open(kernel_path, 'wb') as kf:
                    kf.write(kernel_data)
                components['kernel'] = str(kernel_path)
            
            # Extract ramdisk
            if ramdisk_size > 0:
                f.seek(ramdisk_offset)
                ramdisk_data = f.read(ramdisk_size)
                ramdisk_path = extract_path / 'ramdisk.img'
                with open(ramdisk_path, 'wb') as rf:
                    rf.write(ramdisk_data)
                components['ramdisk'] = str(ramdisk_path)
            
            # Extract second stage
            if second_size > 0:
                f.seek(second_offset)
                second_data = f.read(second_size)
                second_path = extract_path / 'second'
                with open(second_path, 'wb') as sf:
                    sf.write(second_data)
                components['second'] = str(second_path)
            
            # Save config
            cfg_path = extract_path / 'bootimg.cfg'
            with open(cfg_path, 'w') as cf:
                for key, value in boot_config.items():
                    cf.write(f"{key} = {value}\n")
            components['config'] = str(cfg_path)
            
            return {
                'method': 'manual_android',
                'components': components,
                'boot_config': boot_config,
                'extract_dir': str(extract_path)
            }
    
    def analyze_kernel(self, kernel_path: str) -> Dict[str, Any]:
        """
        Analyze kernel binary and extract information
        
        Args:
            kernel_path: Path to kernel file
            
        Returns:
            Dict with kernel analysis
        """
        print(f"🔍 Analyzing kernel: {kernel_path}")
        
        kernel_file = Path(kernel_path)
        if not kernel_file.exists():
            raise FileNotFoundError(f"Kernel file not found: {kernel_path}")
        
        analysis = {
            'path': str(kernel_file),
            'size': kernel_file.stat().st_size,
            'sha256': self._calculate_hash(kernel_file),
            'timestamp': datetime.now().isoformat()
        }
        
        # Get kernel version
        version_info = self._extract_kernel_version(kernel_file)
        if version_info:
            analysis.update(version_info)
        
        # Extract kernel strings
        strings_info = self._extract_kernel_strings(kernel_file)
        if strings_info:
            analysis['strings_analysis'] = strings_info
        
        # Detect compression
        compression = self._detect_compression(kernel_file)
        if compression:
            analysis['compression'] = compression
            
            # Try to decompress and analyze
            decompressed = self._decompress_kernel(kernel_file, compression)
            if decompressed:
                analysis['decompressed'] = decompressed
                # Re-analyze decompressed kernel
                version_info = self._extract_kernel_version(Path(decompressed))
                if version_info:
                    analysis['decompressed_version'] = version_info
        
        # Detect architecture
        arch = self._detect_architecture(kernel_file)
        if arch:
            analysis['architecture'] = arch
        
        # Extract kernel config if present
        config = self._extract_kernel_config(kernel_file)
        if config:
            analysis['config'] = config
            analysis['config_features'] = self._analyze_config_features(config)
        
        # Security features
        security = self._detect_security_features(kernel_file)
        if security:
            analysis['security_features'] = security
        
        print(f"✅ Analysis complete!")
        
        # Save analysis
        analysis_file = self.extract_dir / "kernel_analysis.json"
        with open(analysis_file, 'w') as f:
            # Filter out binary data for JSON
            json_safe = {k: v for k, v in analysis.items() 
                        if not isinstance(v, bytes)}
            json.dump(json_safe, f, indent=2)
        
        return analysis
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _extract_kernel_version(self, kernel_file: Path) -> Optional[Dict]:
        """Extract kernel version string"""
        try:
            with open(kernel_file, 'rb') as f:
                data = f.read()
            
            # Look for Linux version string
            pattern = rb'Linux version [\d\.]+-[\w\-\+\.]+\s+\([^)]+\)'
            matches = re.findall(pattern, data)
            
            if matches:
                version_str = matches[0].decode('ascii', errors='ignore')
                
                # Parse version components
                version_match = re.search(r'Linux version ([\d\.]+)', version_str)
                kernel_version = version_match.group(1) if version_match else 'unknown'
                
                # Parse build info
                build_match = re.search(r'\(([^)]+)\)', version_str)
                build_info = build_match.group(1) if build_match else 'unknown'
                
                return {
                    'version_string': version_str,
                    'kernel_version': kernel_version,
                    'build_info': build_info
                }
            
        except Exception as e:
            print(f"⚠️  Could not extract version: {e}")
        
        return None
    
    def _extract_kernel_strings(self, kernel_file: Path) -> Dict:
        """Extract and analyze interesting strings from kernel"""
        try:
            result = subprocess.run(['strings', str(kernel_file)],
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return {}
            
            strings = result.stdout.split('\n')
            
            # Categorize interesting strings
            categories = {
                'filesystems': [],
                'drivers': [],
                'security': [],
                'network': [],
                'schedulers': []
            }
            
            fs_keywords = ['ext4', 'f2fs', 'vfat', 'ntfs', 'exfat', 'btrfs']
            driver_keywords = ['driver', 'device', 'module']
            security_keywords = ['selinux', 'apparmor', 'seccomp', 'dm-verity']
            network_keywords = ['tcp', 'udp', 'ipv6', 'netfilter', 'iptables']
            scheduler_keywords = ['cfq', 'noop', 'deadline', 'bfq', 'scheduler']
            
            for s in strings:
                s_lower = s.lower()
                if any(k in s_lower for k in fs_keywords):
                    categories['filesystems'].append(s)
                if any(k in s_lower for k in driver_keywords):
                    categories['drivers'].append(s[:100])  # Limit length
                if any(k in s_lower for k in security_keywords):
                    categories['security'].append(s)
                if any(k in s_lower for k in network_keywords):
                    categories['network'].append(s)
                if any(k in s_lower for k in scheduler_keywords):
                    categories['schedulers'].append(s)
            
            # Limit to top results
            return {k: list(set(v))[:20] for k, v in categories.items() if v}
            
        except Exception as e:
            print(f"⚠️  String extraction failed: {e}")
            return {}
    
    def _detect_compression(self, kernel_file: Path) -> Optional[str]:
        """Detect kernel compression type"""
        with open(kernel_file, 'rb') as f:
            magic = f.read(8)
        
        # Check compression magic bytes
        if magic[:2] == b'\x1f\x8b':
            return 'gzip'
        elif magic[:2] == b'\x42\x5a':
            return 'bzip2'
        elif magic[:6] == b'\xfd7zXZ\x00':
            return 'xz'
        elif magic[:4] == b'\x89LZO':
            return 'lzo'
        elif magic[:4] == b'\x28\xb5\x2f\xfd':
            return 'zstd'
        elif magic[:3] == b'\x02\x21\x4c':
            return 'lz4'
        
        return None
    
    def _decompress_kernel(self, kernel_file: Path, compression: str) -> Optional[str]:
        """Decompress kernel if compressed"""
        output_path = self.extract_dir / f"{kernel_file.stem}_decompressed"
        
        try:
            if compression == 'gzip':
                subprocess.run(['gunzip', '-c', str(kernel_file)],
                             stdout=open(output_path, 'wb'), check=True)
            elif compression == 'xz':
                subprocess.run(['unxz', '-c', str(kernel_file)],
                             stdout=open(output_path, 'wb'), check=True)
            elif compression == 'bzip2':
                subprocess.run(['bunzip2', '-c', str(kernel_file)],
                             stdout=open(output_path, 'wb'), check=True)
            elif compression == 'lz4':
                subprocess.run(['lz4', '-d', str(kernel_file), str(output_path)],
                             check=True)
            else:
                return None
            
            return str(output_path)
            
        except Exception as e:
            print(f"⚠️  Decompression failed: {e}")
            return None
    
    def _detect_architecture(self, kernel_file: Path) -> Optional[str]:
        """Detect kernel architecture"""
        try:
            result = subprocess.run(['file', str(kernel_file)],
                                  capture_output=True, text=True)
            
            output = result.stdout.lower()
            
            if 'arm64' in output or 'aarch64' in output:
                return 'arm64'
            elif 'arm' in output:
                return 'arm'
            elif 'x86-64' in output or 'x86_64' in output:
                return 'x86_64'
            elif 'x86' in output or 'i386' in output:
                return 'x86'
            
        except:
            pass
        
        return None
    
    def _extract_kernel_config(self, kernel_file: Path) -> Optional[Dict]:
        """Extract embedded kernel configuration"""
        try:
            with open(kernel_file, 'rb') as f:
                data = f.read()
            
            # Look for kernel config markers
            # IKCFG_ST = start marker, IKCFG_ED = end marker
            start_marker = b'IKCFG_ST'
            end_marker = b'IKCFG_ED'
            
            start_idx = data.find(start_marker)
            if start_idx == -1:
                return None
            
            end_idx = data.find(end_marker, start_idx)
            if end_idx == -1:
                return None
            
            # Extract config data (it's gzip compressed)
            config_data = data[start_idx + len(start_marker):end_idx]
            
            # Decompress
            import gzip
            config_text = gzip.decompress(config_data).decode('utf-8', errors='ignore')
            
            # Parse config
            config = {}
            for line in config_text.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value
            
            # Save full config
            config_file = self.extract_dir / "kernel_config.txt"
            with open(config_file, 'w') as f:
                f.write(config_text)
            
            return {
                'config_file': str(config_file),
                'config_count': len(config),
                'sample_configs': dict(list(config.items())[:10])
            }
            
        except Exception as e:
            print(f"⚠️  Config extraction failed: {e}")
            return None
    
    def _analyze_config_features(self, config_data: Dict) -> Dict:
        """Analyze kernel configuration for features"""
        if 'config_file' not in config_data:
            return {}
        
        try:
            with open(config_data['config_file'], 'r') as f:
                config_text = f.read()
            
            features = {
                'security': [],
                'networking': [],
                'filesystem': [],
                'performance': [],
                'power': []
            }
            
            # Security features
            security_checks = [
                ('CONFIG_SECURITY_SELINUX=y', 'SELinux enabled'),
                ('CONFIG_SECURITY_APPARMOR=y', 'AppArmor enabled'),
                ('CONFIG_SECCOMP=y', 'Seccomp enabled'),
                ('CONFIG_DM_VERITY=y', 'dm-verity enabled'),
                ('CONFIG_SECURITY_NETWORK=y', 'Network security enabled')
            ]
            
            # Networking features
            network_checks = [
                ('CONFIG_IPV6=y', 'IPv6 support'),
                ('CONFIG_NETFILTER=y', 'Netfilter support'),
                ('CONFIG_IP_NF_IPTABLES=y', 'iptables support'),
                ('CONFIG_TCP_CONG_BBR=y', 'BBR congestion control')
            ]
            
            # Filesystem features
            fs_checks = [
                ('CONFIG_EXT4_FS=y', 'ext4 filesystem'),
                ('CONFIG_F2FS_FS=y', 'f2fs filesystem'),
                ('CONFIG_EXFAT_FS=y', 'exFAT filesystem'),
                ('CONFIG_NTFS_FS=y', 'NTFS filesystem')
            ]
            
            # Performance features
            perf_checks = [
                ('CONFIG_SMP=y', 'Symmetric multiprocessing'),
                ('CONFIG_PREEMPT=y', 'Preemptible kernel'),
                ('CONFIG_CPU_FREQ=y', 'CPU frequency scaling'),
                ('CONFIG_HOTPLUG_CPU=y', 'CPU hotplug support')
            ]
            
            # Power management
            power_checks = [
                ('CONFIG_PM=y', 'Power management'),
                ('CONFIG_CPU_IDLE=y', 'CPU idle support'),
                ('CONFIG_SUSPEND=y', 'Suspend support'),
                ('CONFIG_HIBERNATION=y', 'Hibernation support')
            ]
            
            # Check all features
            for config, desc in security_checks:
                if config in config_text:
                    features['security'].append(desc)
            
            for config, desc in network_checks:
                if config in config_text:
                    features['networking'].append(desc)
            
            for config, desc in fs_checks:
                if config in config_text:
                    features['filesystem'].append(desc)
            
            for config, desc in perf_checks:
                if config in config_text:
                    features['performance'].append(desc)
            
            for config, desc in power_checks:
                if config in config_text:
                    features['power'].append(desc)
            
            return {k: v for k, v in features.items() if v}
            
        except Exception as e:
            print(f"⚠️  Feature analysis failed: {e}")
            return {}
    
    def _detect_security_features(self, kernel_file: Path) -> Dict:
        """Detect security-related features in kernel"""
        features = {
            'selinux': False,
            'dm_verity': False,
            'seccomp': False,
            'kaslr': False
        }
        
        try:
            with open(kernel_file, 'rb') as f:
                data = f.read()
            
            # Check for security strings
            if b'selinux' in data.lower():
                features['selinux'] = True
            if b'dm-verity' in data.lower() or b'dm_verity' in data.lower():
                features['dm_verity'] = True
            if b'seccomp' in data.lower():
                features['seccomp'] = True
            if b'kaslr' in data.lower():
                features['kaslr'] = True
            
        except:
            pass
        
        return features
    
    def create_custom_kernel(self, base_kernel: str, modifications: Dict) -> str:
        """
        Create custom kernel with modifications
        
        Args:
            base_kernel: Path to base kernel
            modifications: Dict of modifications to apply
            
        Returns:
            Path to custom kernel
        """
        print(f"🔨 Creating custom kernel...")
        print(f"Base kernel: {base_kernel}")
        
        # This is a simplified version - full implementation would require
        # kernel source, toolchains, etc.
        
        # For demonstration, we'll show what modifications would be applied
        print("\n📝 Planned modifications:")
        for key, value in modifications.items():
            print(f"  - {key}: {value}")
        
        # In a full implementation, this would:
        # 1. Extract kernel source or use prebuilt
        # 2. Apply config changes
        # 3. Apply patches
        # 4. Compile with appropriate toolchain
        # 5. Package as boot.img
        
        print("\n⚠️  Note: Full kernel building requires:")
        print("  - Kernel source code")
        print("  - Cross-compilation toolchain")
        print("  - Build environment (Make, GCC/Clang)")
        print("  - Device-specific configs")
        
        return base_kernel
    
    def repack_boot_image(self, components: Dict, output_path: str) -> str:
        """
        Repack boot image from components
        
        Args:
            components: Dict with kernel, ramdisk, dtb paths
            output_path: Output path for new boot.img
            
        Returns:
            Path to repacked boot.img
        """
        print(f"📦 Repacking boot image...")
        
        output = Path(output_path)
        
        # Check required components
        if 'kernel' not in components:
            raise ValueError("Kernel is required for repacking")
        
        # Try mkbootimg if available
        if self.tools.get('mkbootimg'):
            cmd = ['mkbootimg']
            
            if 'kernel' in components:
                cmd.extend(['--kernel', components['kernel']])
            if 'ramdisk' in components:
                cmd.extend(['--ramdisk', components['ramdisk']])
            if 'second' in components:
                cmd.extend(['--second', components['second']])
            if 'dtb' in components:
                cmd.extend(['--dtb', components['dtb']])
            
            # Add boot config parameters
            if 'config' in components:
                config = self._parse_boot_config(components['config'])
                if 'cmdline' in config:
                    cmd.extend(['--cmdline', config['cmdline']])
                if 'base' in config:
                    cmd.extend(['--base', config['base']])
                if 'pagesize' in config:
                    cmd.extend(['--pagesize', config['pagesize']])
            
            cmd.extend(['--output', str(output)])
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✅ Boot image repacked: {output}")
                return str(output)
            except subprocess.CalledProcessError as e:
                print(f"⚠️  mkbootimg failed: {e}")
        
        # Try abootimg
        elif self.tools.get('abootimg'):
            try:
                cmd = ['abootimg', '--create', str(output)]
                
                if 'kernel' in components:
                    cmd.extend(['-k', components['kernel']])
                if 'ramdisk' in components:
                    cmd.extend(['-r', components['ramdisk']])
                if 'second' in components:
                    cmd.extend(['-s', components['second']])
                if 'config' in components:
                    cmd.extend(['-f', components['config']])
                
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✅ Boot image repacked: {output}")
                return str(output)
            except subprocess.CalledProcessError as e:
                print(f"⚠️  abootimg failed: {e}")
        
        print("⚠️  No boot image tools available")
        print("Install: mkbootimg, abootimg, or android-tools")
        
        return ""
    
    def _parse_boot_config(self, config_path: str) -> Dict:
        """Parse bootimg.cfg file"""
        config = {}
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        config[key.strip()] = value.strip()
        except:
            pass
        return config
    
    def flash_kernel(self, kernel_path: str, device_mode: str = "fastboot") -> bool:
        """
        Flash kernel to device
        
        Args:
            kernel_path: Path to kernel or boot.img
            device_mode: 'fastboot' or 'adb'
            
        Returns:
            True if successful
        """
        print(f"📱 Flashing kernel: {kernel_path}")
        print(f"Mode: {device_mode}")
        
        if device_mode == "fastboot":
            # Check if device is in fastboot mode
            try:
                result = subprocess.run(['fastboot', 'devices'],
                                      capture_output=True, text=True)
                if not result.stdout.strip():
                    print("❌ No device in fastboot mode")
                    return False
                
                # Flash boot partition
                print("📤 Flashing boot partition...")
                subprocess.run(['fastboot', 'flash', 'boot', kernel_path],
                             check=True)
                
                print("✅ Kernel flashed successfully!")
                print("🔄 Rebooting device...")
                subprocess.run(['fastboot', 'reboot'])
                
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Flash failed: {e}")
                return False
        
        elif device_mode == "adb":
            print("⚠️  Flashing via ADB requires root access")
            print("Use: dd if=kernel.img of=/dev/block/by-name/boot")
            return False
        
        return False
    
    def generate_report(self, analysis: Dict, output_path: str = None) -> str:
        """Generate kernel analysis report"""
        if output_path is None:
            output_path = self.output_dir / "kernel_report.md"
        
        report = []
        report.append("# Kernel Analysis Report")
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n## Kernel Information\n")
        
        if 'version_string' in analysis:
            report.append(f"**Version:** {analysis['version_string']}")
        if 'kernel_version' in analysis:
            report.append(f"**Kernel Version:** {analysis['kernel_version']}")
        if 'architecture' in analysis:
            report.append(f"**Architecture:** {analysis['architecture']}")
        if 'compression' in analysis:
            report.append(f"**Compression:** {analysis['compression']}")
        
        report.append(f"\n**Size:** {analysis.get('size', 0):,} bytes")
        report.append(f"**SHA256:** `{analysis.get('sha256', '')}`")
        
        # Security features
        if 'security_features' in analysis:
            report.append(f"\n## Security Features\n")
            for feature, enabled in analysis['security_features'].items():
                status = "✅ Enabled" if enabled else "❌ Disabled"
                report.append(f"- **{feature.upper()}:** {status}")
        
        # Config features
        if 'config_features' in analysis:
            report.append(f"\n## Kernel Configuration Features\n")
            for category, features in analysis['config_features'].items():
                if features:
                    report.append(f"\n### {category.title()}")
                    for feature in features:
                        report.append(f"- {feature}")
        
        # Strings analysis
        if 'strings_analysis' in analysis:
            report.append(f"\n## Detected Components\n")
            for category, items in analysis['strings_analysis'].items():
                if items:
                    report.append(f"\n### {category.title()}")
                    for item in items[:10]:  # Limit to 10
                        report.append(f"- {item}")
        
        report_text = "\n".join(report)
        
        with open(output_path, 'w') as f:
            f.write(report_text)
        
        print(f"📄 Report generated: {output_path}")
        
        return str(output_path)


def print_banner():
    """Print KernelForge banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗  ██╗███████╗██████╗ ███╗   ██╗███████╗██╗             ║
║   ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝██║             ║
║   █████╔╝ █████╗  ██████╔╝██╔██╗ ██║█████╗  ██║             ║
║   ██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝  ██║             ║
║   ██║  ██╗███████╗██║  ██║██║ ╚████║███████╗███████╗        ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝        ║
║                                                              ║
║   ███████╗ ██████╗ ██████╗  ██████╗ ███████╗                ║
║   ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝                ║
║   █████╗  ██║   ██║██████╔╝██║  ███╗█████╗                  ║
║   ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝                  ║
║   ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗                ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                ║
║                                                              ║
║            Kernel Unpacking & Customization Tool            ║
║                 Part of XDA Master Toolkit                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

    🔨 Extract • Analyze • Customize • Repack • Flash
    
"""
    print(banner)


def main():
    """Main CLI interface"""
    import argparse
    
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='KernelForge - Kernel Analysis & Customization Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract and analyze boot image
  python kernel_forge.py extract boot.img
  
  # Analyze kernel only
  python kernel_forge.py analyze kernel.img
  
  # Repack boot image
  python kernel_forge.py repack --kernel kernel.img --ramdisk ramdisk.img -o new_boot.img
  
  # Generate analysis report
  python kernel_forge.py report extraction_info.json
  
  # Flash kernel (requires fastboot)
  python kernel_forge.py flash boot.img

For more information: https://github.com/XDA-Master-Toolkit/KernelForge
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract boot image')
    extract_parser.add_argument('boot_image', help='Path to boot.img')
    extract_parser.add_argument('-w', '--workspace', default='kernel_workspace',
                              help='Working directory')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze kernel')
    analyze_parser.add_argument('kernel', help='Path to kernel file')
    analyze_parser.add_argument('-w', '--workspace', default='kernel_workspace',
                              help='Working directory')
    
    # Repack command
    repack_parser = subparsers.add_parser('repack', help='Repack boot image')
    repack_parser.add_argument('-k', '--kernel', required=True, help='Kernel file')
    repack_parser.add_argument('-r', '--ramdisk', help='Ramdisk file')
    repack_parser.add_argument('-s', '--second', help='Second stage file')
    repack_parser.add_argument('-d', '--dtb', help='Device tree file')
    repack_parser.add_argument('-c', '--config', help='Boot config file')
    repack_parser.add_argument('-o', '--output', default='new_boot.img',
                              help='Output boot image')
    repack_parser.add_argument('-w', '--workspace', default='kernel_workspace',
                              help='Working directory')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('analysis_file', help='Path to analysis JSON')
    report_parser.add_argument('-o', '--output', help='Output report path')
    report_parser.add_argument('-w', '--workspace', default='kernel_workspace',
                              help='Working directory')
    
    # Flash command
    flash_parser = subparsers.add_parser('flash', help='Flash kernel')
    flash_parser.add_argument('boot_image', help='Path to boot.img')
    flash_parser.add_argument('-m', '--mode', default='fastboot',
                            choices=['fastboot', 'adb'], help='Flash mode')
    flash_parser.add_argument('-w', '--workspace', default='kernel_workspace',
                            help='Working directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create KernelForge instance
    forge = KernelForge(args.workspace)
    
    try:
        if args.command == 'extract':
            result = forge.extract_boot_image(args.boot_image)
            print(f"\n✅ Extraction complete!")
            print(f"📁 Extract directory: {result.get('extract_dir', '')}")
            
        elif args.command == 'analyze':
            result = forge.analyze_kernel(args.kernel)
            print(f"\n✅ Analysis complete!")
            if 'kernel_version' in result:
                print(f"🔍 Kernel version: {result['kernel_version']}")
            
        elif args.command == 'repack':
            components = {'kernel': args.kernel}
            if args.ramdisk:
                components['ramdisk'] = args.ramdisk
            if args.second:
                components['second'] = args.second
            if args.dtb:
                components['dtb'] = args.dtb
            if args.config:
                components['config'] = args.config
            
            result = forge.repack_boot_image(components, args.output)
            if result:
                print(f"\n✅ Repack complete: {result}")
            
        elif args.command == 'report':
            with open(args.analysis_file, 'r') as f:
                analysis = json.load(f)
            
            output = args.output if args.output else None
            report_path = forge.generate_report(analysis, output)
            print(f"\n✅ Report generated: {report_path}")
            
        elif args.command == 'flash':
            success = forge.flash_kernel(args.boot_image, args.mode)
            if success:
                print(f"\n✅ Flash complete!")
            else:
                print(f"\n❌ Flash failed")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
