import subprocess
import os
from datetime import datetime
import platform

def run_git_commands(commit_message=None):
    """
    运行git命令的函数，支持SSH认证
    
    Args:
        commit_message (str): 提交信息，如果为None则使用默认时间戳信息
    """
    try:
        # 确保在正确的目录下
        current_dir = os.getcwd()
        print(f"当前工作目录: {current_dir}")

        # 如果没有提供commit信息，使用时间戳作为默认信息
        if commit_message is None:
            commit_message = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 设置SSH环境变量
        env = os.environ.copy()
        
        # 在Windows系统下指定SSH路径
        if platform.system() == 'Windows':
            ssh_path = os.path.expanduser('~/.ssh')
            if not os.path.exists(ssh_path):
                raise ValueError(f"SSH目录不存在: {ssh_path}")
            
            # 设置GIT_SSH_COMMAND环境变量
            env['GIT_SSH_COMMAND'] = f'ssh -i "{os.path.join(ssh_path, "id_rsa")}"'

        # Git 命令列表
        commands = [
            ["git", "add", "-A"],
            ["git", "commit", "-m", commit_message],
            ["git", "push"]
        ]

        # 执行每个命令
        for command in commands:
            print(f"执行命令: {' '.join(command)}")
            result = subprocess.run(command, 
                                 capture_output=True, 
                                 text=True,
                                 env=env)
            
            # 检查命令是否成功执行
            if result.returncode == 0:
                print(f"成功: {result.stdout}")
            else:
                print(f"错误: {result.stderr}")
                # 如果是SSH密钥错误，提供更详细的提示
                if "Permission denied (publickey)" in result.stderr:
                    print("\n可能的解决方案:")
                    print("1. 确保你的SSH密钥已经正确生成并添加到GitHub")
                    print("2. 检查 ~/.ssh 目录下是否存在 id_rsa 和 id_rsa.pub 文件")
                    print("3. 运行 'ssh -T git@github.com' 测试SSH连接")
                    print("4. 如果需要，可以运行 'ssh-add ~/.ssh/id_rsa' 添加密钥到SSH agent")
                return False

        return True

    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("\n故障排除步骤:")
        print("1. 运行 'ssh -T git@github.com' 测试与GitHub的SSH连接")
        print("2. 检查SSH密钥是否正确配置")
        print("3. 确保仓库URL使用的是SSH格式 (git@github.com:username/repo.git)")
        return False

if __name__ == "__main__":
    # 你可以在这里自定义commit信息
    custom_message = "auto git"
    run_git_commands(custom_message)