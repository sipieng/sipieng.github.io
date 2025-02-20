# import subprocess
# import os
# from datetime import datetime
# from dotenv import load_dotenv
# import platform
# import tempfile

# def check_git_config():
#     """检查git配置"""
#     try:
#         name = subprocess.run(["git", "config", "user.name"], 
#                             capture_output=True, 
#                             text=True)
#         email = subprocess.run(["git", "config", "user.email"], 
#                              capture_output=True, 
#                              text=True)
        
#         if not name.stdout.strip() or not email.stdout.strip():
#             print("Git用户信息未配置。正在配置...")
#             user_name = input("请输入你的git用户名: ")
#             user_email = input("请输入你的git邮箱: ")
            
#             subprocess.run(["git", "config", "user.name", user_name])
#             subprocess.run(["git", "config", "user.email", user_email])
#             print("Git用户信息配置完成！")
            
#     except Exception as e:
#         print(f"检查git配置时出错: {str(e)}")
#         return False
#     return True

# def create_askpass_script(passphrase):
#     """创建临时的SSH askpass脚本"""
#     if platform.system() == 'Windows':
#         script_content = f'@echo off\necho {passphrase}'
#         ext = '.bat'
#     else:
#         script_content = f'#!/bin/sh\necho "{passphrase}"'
#         ext = '.sh'
    
#     # 使用临时文件
#     temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext, mode='w')
#     temp.write(script_content)
#     temp.close()
    
#     # 在Unix系统上设置执行权限
#     if platform.system() != 'Windows':
#         os.chmod(temp.name, 0o700)
    
#     return temp.name

# def run_git_commands(commit_message=None):
#     """运行git命令的函数"""
#     try:
#         # 检查git配置
#         if not check_git_config():
#             return False

#         # 加载.env文件
#         load_dotenv()
        
#         # 获取SSH密钥密码
#         ssh_passphrase = os.getenv('SSH_PASSPHRASE')
#         if not ssh_passphrase:
#             raise ValueError("未在.env文件中找到SSH_PASSPHRASE")

#         # 创建askpass脚本
#         askpass_script = create_askpass_script(ssh_passphrase)

#         try:
#             # 准备环境变量
#             env = os.environ.copy()
#             env['SSH_ASKPASS'] = askpass_script
#             env['GIT_ASKPASS'] = askpass_script
#             if platform.system() == 'Windows':
#                 env['SSH_ASKPASS_REQUIRE'] = 'force'
#                 env['DISPLAY'] = 'dummy:0'
            
#             # 如果没有提供commit信息，使用时间戳作为默认信息
#             if commit_message is None:
#                 commit_message = f"Auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#             # Git 命令列表
#             commands = [
#                 ["git", "add", "-A"],
#                 ["git", "commit", "-m", commit_message],
#                 ["git", "push"]
#             ]

#             # 执行git命令
#             for command in commands:
#                 print(f"执行命令: {' '.join(command)}")
#                 result = subprocess.run(
#                     command,
#                     capture_output=True,
#                     text=True,
#                     env=env
#                 )
                
#                 if result.returncode == 0:
#                     print(f"成功: {result.stdout}")
#                 else:
#                     print(f"错误: {result.stderr}")
#                     if "nothing to commit" in result.stderr:
#                         print("没有文件需要提交！")
#                         return True
#                     return False

#             return True

#         finally:
#             # 清理临时文件
#             try:
#                 os.unlink(askpass_script)
#             except:
#                 pass

#     except Exception as e:
#         print(f"发生错误: {str(e)}")
#         return False

# if __name__ == "__main__":
#     run_git_commands("auto git")


import subprocess
import os
from dotenv import load_dotenv
import time

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
        # 延迟删除文件，确保文件在操作完成后可以删除
        time.sleep(2)  # 延迟2秒
        if os.path.exists(askpass_path):
            os.remove(askpass_path)

    return True

if __name__ == "__main__":
    run_git_commands("delete a.txt")


