import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

def run_git_commands(commit_message=None):
    """
    运行git命令的函数
    
    Args:
        commit_message (str): 提交信息，如果为None则使用默认时间戳信息
    """
    try:
        # 加载.env文件
        load_dotenv()
        
        # 获取git密码
        git_password = os.getenv('GIT_PASSWORD')
        if not git_password:
            raise ValueError("未在.env文件中找到GIT_PASSWORD")

        # 确保在正确的目录下
        current_dir = os.getcwd()
        print(f"当前工作目录: {current_dir}")

        # 如果没有提供commit信息，使用时间戳作为默认信息
        if commit_message is None:
            commit_message = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Git 命令列表
        commands = [
            ["git", "add", "-A"],
            ["git", "commit", "-m", commit_message],
            # 使用环境变量中的密码进行push
            ["git", "push"]
        ]

        # 设置环境变量，包含git密码
        env = os.environ.copy()
        env['GIT_ASKPASS'] = 'echo'
        env['GIT_PASSWORD'] = git_password

        # 执行每个命令
        for command in commands:
            print(f"执行命令: {' '.join(command)}")
            if command[0:2] == ["git", "push"]:
                # push命令需要使用修改后的环境变量
                result = subprocess.run(command, 
                                     capture_output=True, 
                                     text=True,
                                     env=env)
            else:
                result = subprocess.run(command, 
                                     capture_output=True, 
                                     text=True)
            
            # 检查命令是否成功执行
            if result.returncode == 0:
                print(f"成功: {result.stdout}")
            else:
                print(f"错误: {result.stderr}")
                return False

        return True

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 你可以在这里自定义commit信息
    custom_message = "auto_git"
    run_git_commands(custom_message)