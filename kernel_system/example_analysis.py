#!/usr/bin/env python3
"""
Example 2: Advanced Kernel Analysis

This example demonstrates advanced analysis including:
1. Detailed security auditing
2. Feature comparison
3. Performance analysis
4. Configuration deep-dive

Part of XDA Master Toolkit - KernelForge
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kernel_forge import KernelForge


def analyze_security_posture(analysis: dict) -> dict:
    """Analyze security posture of kernel"""
    security = analysis.get('security_features', {})
    config = analysis.get('config_features', {})
    
    # Score security features
    score = 0
    max_score = 0
    findings = []
    
    # Critical features (3 points each)
    critical_features = {
        'selinux': 'SELinux mandatory access control',
        'dm_verity': 'dm-verity verified boot',
        'seccomp': 'Seccomp system call filtering',
        'kaslr': 'KASLR address space randomization'
    }
    
    for feature, description in critical_features.items():
        max_score += 3
        if security.get(feature):
            score += 3
            findings.append(f"✅ GOOD: {description} is enabled")
        else:
            findings.append(f"⚠️  WARN: {description} is disabled")
    
    # Additional security configs
    if config and 'security' in config:
        for sec_feature in config['security']:
            findings.append(f"ℹ️  INFO: {sec_feature}")
    
    # Calculate percentage
    percentage = (score / max_score * 100) if max_score > 0 else 0
    
    # Determine rating
    if percentage >= 80:
        rating = "EXCELLENT"
    elif percentage >= 60:
        rating = "GOOD"
    elif percentage >= 40:
        rating = "FAIR"
    else:
        rating = "POOR"
    
    return {
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'rating': rating,
        'findings': findings
    }


def analyze_performance_features(analysis: dict) -> dict:
    """Analyze performance-related features"""
    config = analysis.get('config_features', {})
    strings = analysis.get('strings_analysis', {})
    
    findings = []
    features_found = []
    
    # Check for performance configs
    if config and 'performance' in config:
        for perf_feature in config['performance']:
            features_found.append(perf_feature)
            findings.append(f"✅ {perf_feature}")
    
    # Check for CPU schedulers
    if strings and 'schedulers' in strings:
        schedulers = strings['schedulers']
        if schedulers:
            findings.append(f"📊 CPU Schedulers detected: {', '.join(schedulers[:5])}")
    
    # Check kernel version for performance
    version = analysis.get('kernel_version', '')
    if version:
        major = int(version.split('.')[0]) if '.' in version else 0
        minor = int(version.split('.')[1]) if version.count('.') >= 1 else 0
        
        if major >= 5 and minor >= 15:
            findings.append(f"✅ Modern kernel version ({version}) - good performance baseline")
        elif major >= 4:
            findings.append(f"ℹ️  Older kernel version ({version}) - may lack modern optimizations")
        else:
            findings.append(f"⚠️  Very old kernel version ({version})")
    
    return {
        'features': features_found,
        'findings': findings
    }


def analyze_filesystem_support(analysis: dict) -> dict:
    """Analyze filesystem support"""
    config = analysis.get('config_features', {})
    strings = analysis.get('strings_analysis', {})
    
    filesystems = []
    findings = []
    
    # From config
    if config and 'filesystem' in config:
        filesystems.extend(config['filesystem'])
    
    # From strings
    if strings and 'filesystems' in strings:
        for fs in strings['filesystems']:
            if fs not in str(filesystems):
                filesystems.append(f"Detected: {fs}")
    
    # Check for modern filesystems
    modern_fs = ['f2fs', 'exfat', 'btrfs']
    for fs in modern_fs:
        if any(fs.lower() in str(f).lower() for f in filesystems):
            findings.append(f"✅ Modern filesystem: {fs}")
    
    # Check for essential filesystems
    essential_fs = ['ext4', 'vfat']
    for fs in essential_fs:
        if any(fs.lower() in str(f).lower() for f in filesystems):
            findings.append(f"✅ Essential filesystem: {fs}")
    
    return {
        'filesystems': filesystems[:10],  # Limit to 10
        'findings': findings
    }


def compare_kernels(analyses: list) -> dict:
    """Compare multiple kernel analyses"""
    if len(analyses) < 2:
        return {}
    
    comparison = {
        'versions': [],
        'architectures': [],
        'security_scores': [],
        'differences': []
    }
    
    # Collect basic info
    for i, analysis in enumerate(analyses, 1):
        comparison['versions'].append(
            analysis.get('kernel_version', f'Unknown #{i}')
        )
        comparison['architectures'].append(
            analysis.get('architecture', 'Unknown')
        )
        
        # Security analysis
        sec_analysis = analyze_security_posture(analysis)
        comparison['security_scores'].append(
            f"{sec_analysis['rating']} ({sec_analysis['percentage']:.0f}%)"
        )
    
    # Find differences in security features
    if all('security_features' in a for a in analyses):
        all_features = set()
        for analysis in analyses:
            all_features.update(analysis['security_features'].keys())
        
        for feature in all_features:
            values = [a.get('security_features', {}).get(feature, False) 
                     for a in analyses]
            if len(set(values)) > 1:  # Different values
                comparison['differences'].append(
                    f"Security feature '{feature}': " + 
                    ', '.join([str(v) for v in values])
                )
    
    return comparison


def main():
    """Advanced analysis example"""
    
    print("=" * 70)
    print("Example 2: Advanced Kernel Analysis")
    print("=" * 70)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python example_analysis.py <kernel1.img> [kernel2.img ...]")
        print()
        print("Examples:")
        print("  python example_analysis.py kernel.img")
        print("  python example_analysis.py stock.img custom.img")
        sys.exit(1)
    
    kernel_paths = sys.argv[1:]
    
    # Verify files
    for path in kernel_paths:
        if not os.path.exists(path):
            print(f"❌ Error: File not found: {path}")
            sys.exit(1)
    
    print(f"🔍 Analyzing {len(kernel_paths)} kernel(s)")
    print()
    
    # Initialize
    forge = KernelForge(working_dir="analysis_workspace")
    
    # Analyze all kernels
    analyses = []
    
    for i, kernel_path in enumerate(kernel_paths, 1):
        print("=" * 70)
        print(f"KERNEL {i}/{len(kernel_paths)}: {Path(kernel_path).name}")
        print("=" * 70)
        print()
        
        try:
            analysis = forge.analyze_kernel(kernel_path)
            analyses.append(analysis)
            
            # Basic info
            print("📱 Basic Information:")
            print(f"  Version:      {analysis.get('kernel_version', 'Unknown')}")
            print(f"  Architecture: {analysis.get('architecture', 'Unknown')}")
            print(f"  Compression:  {analysis.get('compression', 'None')}")
            print(f"  Size:         {analysis.get('size', 0):,} bytes")
            print()
            
            # Security analysis
            print("🛡️  Security Analysis:")
            sec_analysis = analyze_security_posture(analysis)
            print(f"  Rating: {sec_analysis['rating']}")
            print(f"  Score:  {sec_analysis['score']}/{sec_analysis['max_score']} " +
                  f"({sec_analysis['percentage']:.1f}%)")
            print()
            print("  Findings:")
            for finding in sec_analysis['findings']:
                print(f"    {finding}")
            print()
            
            # Performance analysis
            print("⚡ Performance Analysis:")
            perf_analysis = analyze_performance_features(analysis)
            for finding in perf_analysis['findings']:
                print(f"  {finding}")
            print()
            
            # Filesystem analysis
            print("💾 Filesystem Support:")
            fs_analysis = analyze_filesystem_support(analysis)
            for finding in fs_analysis['findings']:
                print(f"  {finding}")
            if fs_analysis['filesystems']:
                print()
                print("  Supported Filesystems:")
                for fs in fs_analysis['filesystems'][:5]:
                    print(f"    - {fs}")
            print()
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Comparison (if multiple kernels)
    if len(analyses) > 1:
        print("=" * 70)
        print("KERNEL COMPARISON")
        print("=" * 70)
        print()
        
        comparison = compare_kernels(analyses)
        
        print("📊 Summary:")
        for i, (version, arch, score) in enumerate(zip(
            comparison['versions'],
            comparison['architectures'],
            comparison['security_scores']
        ), 1):
            print(f"  Kernel {i}:")
            print(f"    Version:      {version}")
            print(f"    Architecture: {arch}")
            print(f"    Security:     {score}")
        print()
        
        if comparison['differences']:
            print("⚠️  Key Differences:")
            for diff in comparison['differences']:
                print(f"  - {diff}")
            print()
    
    # Summary
    print("=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    print()
    print(f"✅ Analyzed {len(analyses)} kernel(s)")
    print(f"📁 Results saved to: analysis_workspace/")
    print()
    print("Generated files:")
    print("  - analysis_workspace/extracted/kernel_analysis.json")
    print()
    print("Next steps:")
    print("  1. Review detailed analysis results")
    print("  2. Compare with other kernels")
    print("  3. Try example_repack.py to modify and repack")
    print()


if __name__ == '__main__':
    main()
