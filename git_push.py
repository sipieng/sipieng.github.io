import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

def check_git_config():
    """检查git配置"""
    try:
        # 检查git用户名
        name = subprocess.run(["git", "config", "user.name"], 
                            capture_output=True, 
                            text=True)
        email = subprocess.run(["git", "config", "user.email"], 
                             capture_output=True, 
                             text=True)
        
        if not name.stdout.strip() or not email.stdout.strip():
            print("Git用户信息未配置。正在配置...")
            # 提示用户输入信息
            user_name = input("请输入你的git用户名: ")
            user_email = input("请输入你的git邮箱: ")
            
            # 配置git用户信息
            subprocess.run(["git", "config", "user.name", user_name])
            subprocess.run(["git", "config", "user.email", user_email])
            print("Git用户信息配置完成！")
            
    except Exception as e:
        print(f"检查git配置时出错: {str(e)}")
        return False
    return True

def check_git_status():
    """检查git状态"""
    try:
        status = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, 
                              text=True)
        return bool(status.stdout.strip())
    except Exception as e:
        print(f"检查git状态时出错: {str(e)}")
        return False

def run_git_commands(commit_message=None):
    """
    运行git命令的函数，从.env文件读取SSH密钥密码
    
    Args:
        commit_message (str): 提交信息，如果为None则使用默认时间戳信息
    """
    try:
        # 检查git配置
        if not check_git_config():
            return False

        # 检查是否有文件需要提交
        if not check_git_status():
            print("没有文件需要提交！")
            return False

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

        # 确保commit信息被引号包围
        if not commit_message.startswith('"'):
            commit_message = f'"{commit_message}"'

        # Git 命令列表
        commands = [
            ["git", "add", "-A"],
            ["git", "commit", "-m", commit_message],
            ["git", "push"]
        ]

        # 设置环境变量
        env = os.environ.copy()
        env['SSH_PASS'] = ssh_passphrase
        
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
                if "nothing to commit" in result.stderr:
                    print("没有文件需要提交！")
                    return True
                elif "please tell me who you are" in result.stderr.lower():
                    print("Git用户信息未配置，请运行:")
                    print("git config --global user.email '你的邮箱'")
                    print("git config --global user.name '你的用户名'")
                    return False
                return False

        return True

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 你可以在这里自定义commit信息
    custom_message = "auto git"
    run_git_commands(custom_message)