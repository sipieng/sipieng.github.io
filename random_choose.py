import pandas as pd
import re

source = "list_new.xlsx"
n = 5

# 要过滤的内容
patt_list = ["~", "未完", "disk", "disc", "mp3", "缺", "补", "iplayer", "audio book", "audio drama", "webrip", "volume", "pdf", "BBC Drama"]
patt_list_re = [r"CD\d", r"0\d", r"\d\.", r"\d --", r"\(\d{2,3}K [^)]+\)"]

# 把要过滤的内容用"|"符号合并，以便在pandas中用正则表达式替换。re.escape用于自动处理特殊字符的转义
patt = "|".join(map(re.escape, patt_list)) + "|" + "|".join(patt_list_re)

# 使用pandas处理
df = pd.read_excel(source, sheet_name="List")
df = (
    df[['路径']]    # 保留DataFrame结构而不是Series
    .drop_duplicates()
    .assign(路径=df['路径'].str.rsplit("\\", n=1).str[-1])  # 提取反斜杠后的内容
)
df = df[~df['路径'].str.contains(patt, case=False, regex=True)] # 过滤不需要的内容，`~`表示取反，即不包含
print(f"\n总数：{len(df)}条，随机抽取{n}条\n=========================")

selection = df['路径'].sample(n).tolist()
for i in selection:
    print(i)
