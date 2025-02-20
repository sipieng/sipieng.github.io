import subprocess
import os
from dotenv import load_dotenv


def run_git_commands(commit_message="Auto commit"):
    """执行git add、commit、push，读取密码从.env文件"""
    load_dotenv()

    ssh_passphrase = os.getenv('SSH_PASSPHRASE')
    if not ssh_passphrase:
        print("未在.env文件中找到SSH_PASSPHRASE")
        return False

    # 在用户主目录下创建askpass.bat文件，避免临时目录中的路径问题
    user_dir = os.path.expanduser("~")  # 获取用户主目录路径
    askpass_path = os.path.join(user_dir, 'askpass.bat')

    with open(askpass_path, 'w') as f:
        f.write(f'@echo off\necho {ssh_passphrase}')

    # 使用绝对路径
    askpass_full_path = askpass_path

    # 设置环境变量
    env = os.environ.copy()
    env['SSH_ASKPASS'] = askpass_full_path  # 使用绝对路径
    env['GIT_ASKPASS'] = askpass_full_path  # 使用绝对路径
    env['SSH_ASKPASS_REQUIRE'] = 'force'

    try:
        # 执行git命令
        for command in [["git", "add", "-A"], ["git", "commit", "-m", commit_message], ["git", "push"]]:
            result = subprocess.run(command, capture_output=True, text=True, env=env)
            if result.returncode != 0:
                print(f"错误: {result.stderr}")
                return False
            print(f"成功: {result.stdout}")

    finally:
        if os.path.exists(askpass_path):
            os.remove(askpass_path)

    return True

if __name__ == "__main__":
    run_git_commands()


