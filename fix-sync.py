#!/usr/bin/env python3
"""
自动修复同步问题
"""
import subprocess
import sys
from datetime import datetime

def run_cmd(cmd, cwd=None, timeout=60):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def fix_github():
    """修复 GitHub 同步"""
    print("📦 正在推送 GitHub...")
    out, err, rc = run_cmd("git push origin main", cwd="/root/.openclaw/workspace/daily-brief")
    if rc == 0:
        print("✅ GitHub 推送成功")
        return True
    else:
        print(f"❌ GitHub 推送失败: {err}")
        return False

def fix_tencent():
    """修复腾讯云同步"""
    print("☁️  正在同步腾讯云...")
    out, err, rc = run_cmd(
        "ssh -i ~/.ssh/tencent_sync -o ConnectTimeout=15 -o StrictHostKeyChecking=no "
        "ubuntu@43.139.1.235 'cd /var/www/daily-brief && git fetch origin && git reset --hard origin/main'",
        timeout=45
    )
    if rc == 0:
        print("✅ 腾讯云同步成功")
        return True
    else:
        print(f"❌ 腾讯云同步失败: {err}")
        return False

def main():
    print(f"=== 自动修复同步问题 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] ===\n")
    
    # 先检查状态
    print("🔍 检查当前状态...")
    out, _, _ = run_cmd("python3 check-sync.py", cwd="/root/.openclaw/workspace/daily-brief")
    print(out)
    
    # 询问是否修复
    print("\n🛠️  开始自动修复...")
    
    github_fixed = fix_github()
    tencent_fixed = fix_tencent()
    
    print("\n=== 修复结果 ===")
    if github_fixed and tencent_fixed:
        print("✅ 所有同步已修复")
        return 0
    else:
        print("❌ 部分修复失败，请手动检查")
        return 1

if __name__ == "__main__":
    exit(main())
