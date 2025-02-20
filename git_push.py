import subprocess
import os
from datetime import datetime
import platform
from dotenv import load_dotenv

def run_git_commands(commit_message=None):
    """
    运行git命令的函数，从.env文件读取SSH密钥密码
    
    Args:
        commit_message (str): 提交信息，如果为None则使用默认时间戳信息
    """
    try:
        # 加载.env文件
        load_dotenv()
        
        # 获取SSH密钥密码
        ssh_passphrase = os.getenv('SSH_PASSPHRASE')
        if not ssh_passphrase:
            raise ValueError("未在.env文件中找到SSH_PASSPHRASE")

        # 确保在正确的目录下
        current_dir = os.getcwd()
        print(f"当前工作目录: {current_dir}")

        # 如果没有提供commit信息，使用时间戳作为默认信息
        if commit_message is None:
            commit_message = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 设置环境变量
        env = os.environ.copy()
        
        # 创建临时SSH脚本来处理密码
        if platform.system() == 'Windows':
            # Windows版本的SSH askpass脚本
            ssh_script = '''@echo off
            echo %SSH_PASS%
            '''
            script_ext = '.bat'
        else:
            # Unix版本的SSH askpass脚本
            ssh_script = '''#!/bin/bash
            echo "$SSH_PASS"
            '''
            script_ext = '.sh'

        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'ssh_askpass{script_ext}')
        
        try:
            # 创建并写入脚本
            with open(script_path, 'w') as f:
                f.write(ssh_script)
            
            # 设置脚本权限
            if platform.system() != 'Windows':
                os.chmod(script_path, 0o700)

            # 设置SSH环境变量
            env['SSH_ASKPASS'] = script_path
            env['SSH_PASS'] = ssh_passphrase
            env['GIT_ASKPASS'] = script_path
            if platform.system() == 'Windows':
                env['SSH_ASKPASS_REQUIRE'] = 'force'
                ssh_path = os.path.expanduser('~/.ssh/id_rsa')
                env['GIT_SSH_COMMAND'] = f'ssh -i "{ssh_path}"'

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
                    return False

        finally:
            # 清理临时脚本文件
            if os.path.exists(script_path):
                os.remove(script_path)

        return True

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 你可以在这里自定义commit信息
    custom_message = "auto git"
    run_git_commands(custom_message)