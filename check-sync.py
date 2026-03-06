#!/usr/bin/env python3
"""
每日简报同步状态检查脚本
检查 GitHub 和腾讯云是否同步成功
"""
import subprocess
import json
from datetime import datetime

def run_cmd(cmd, cwd=None):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=30)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def check_github_sync():
    """检查 GitHub 同步状态"""
    # 获取本地最新提交
    local_out, _, _ = run_cmd("git log --oneline -1", cwd="/root/.openclaw/workspace/daily-brief")
    local_hash = local_out.split()[0] if local_out else "unknown"
    local_msg = " ".join(local_out.split()[1:]) if local_out else "unknown"
    
    # 获取远程最新提交
    remote_out, remote_err, rc = run_cmd("git log origin/main --oneline -1", cwd="/root/.openclaw/workspace/daily-brief")
    if rc != 0:
        return False, f"无法获取远程状态: {remote_err}", local_hash, "unknown"
    
    remote_hash = remote_out.split()[0] if remote_out else "unknown"
    
    # 比较
    if local_hash == remote_hash:
        return True, "已同步", local_hash, remote_hash
    else:
        return False, f"未同步 - 本地: {local_hash}, 远程: {remote_hash}", local_hash, remote_hash

def check_tencent_sync():
    """检查腾讯云同步状态"""
    # 获取本地最新提交
    local_out, _, _ = run_cmd("git log --oneline -1", cwd="/root/.openclaw/workspace/daily-brief")
    local_hash = local_out.split()[0] if local_out else "unknown"
    
    # 获取腾讯云上的提交
    tencent_out, tencent_err, rc = run_cmd(
        "ssh -i ~/.ssh/tencent_sync -o ConnectTimeout=10 -o StrictHostKeyChecking=no "
        "ubuntu@43.139.1.235 'cd /var/www/daily-brief && git log --oneline -1' 2>&1"
    )
    
    if rc != 0 or "Connection timed out" in tencent_err or "Could not resolve" in tencent_err:
        return False, f"连接失败: {tencent_err}", local_hash, "unknown"
    
    tencent_hash = tencent_out.split()[0] if tencent_out else "unknown"
    
    # 比较
    if local_hash == tencent_hash:
        return True, "已同步", local_hash, tencent_hash
    else:
        return False, f"未同步 - 本地: {local_hash}, 腾讯云: {tencent_hash}", local_hash, tencent_hash

def check_website_content():
    """检查网站内容日期"""
    # 检查 GitHub Pages
    import urllib.request
    try:
        with urllib.request.urlopen("https://chinafox929.github.io/daily-brief/", timeout=10) as response:
            html = response.read().decode('utf-8')
            if "2026年3月5日" in html or "2026-03-05" in html:
                return True, "网站内容已更新为今日"
            elif "2026年3月4日" in html or "2026-03-04" in html:
                return False, "网站内容仍是昨日"
            else:
                return False, "无法识别网站日期"
    except Exception as e:
        return False, f"无法访问网站: {e}"

def main():
    """主函数"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"=== 每日简报同步状态检查 [{today}] ===\n")
    
    # 检查 GitHub
    github_ok, github_msg, local_hash, remote_hash = check_github_sync()
    print(f"📦 GitHub 同步: {'✅' if github_ok else '❌'} {github_msg}")
    
    # 检查腾讯云
    tencent_ok, tencent_msg, _, tencent_hash = check_tencent_sync()
    print(f"☁️  腾讯云同步: {'✅' if tencent_ok else '❌'} {tencent_msg}")
    
    # 检查网站内容
    website_ok, website_msg = check_website_content()
    print(f"🌐 网站内容: {'✅' if website_ok else '❌'} {website_msg}")
    
    # 总结
    print("\n=== 检查结果 ===")
    all_ok = github_ok and tencent_ok and website_ok
    
    if all_ok:
        print("✅ 所有同步正常！")
        return 0
    else:
        print("❌ 存在同步问题，需要手动处理")
        if not github_ok:
            print("   - 需要推送 GitHub: git push origin main")
        if not tencent_ok:
            print("   - 需要同步腾讯云: ssh ubuntu@43.139.1.235 'cd /var/www/daily-brief && git pull'")
        return 1

if __name__ == "__main__":
    exit(main())
