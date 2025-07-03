import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from zhipuai import ZhipuAI
import time

df = pd.read_csv('rawdata.csv')
if df['微博正文'].isna().any():
    print(f"发现 {df['微博正文'].isna().sum()} 条缺失值，已清理。")
    df = df.dropna(subset=['微博正文']).reset_index(drop=True)  

df_bj = df[df['微博正文'].str.contains('北京')].reset_index(drop=True)

print(f"共有 {len(df_bj)} 条数据")

if '生成结果' not in df_bj.columns:
    df_bj['生成结果'] = ""

progress_file = 'progress.json'
output_file = 'event.xlsx'

try:
    with open(progress_file, 'r') as f:
        processed_indices = set(json.load(f))
except FileNotFoundError:
    processed_indices = set()


client = ZhipuAI(api_key="Yours_key")  # 替换成你的 API 密钥


def generate_event(i, content, time):
    try:
        # 确保content是一个字符串类型，避免格式化问题
        content_str = ', '.join(content) if isinstance(content, list) else str(content)
        response = client.chat.completions.create(
            model="GLM-4-Air",
            messages=[
                {"role": "user", "content": f"""请从以下内容中识别社会活动事件、突发事件及气象活动，并提取关键信息。不要输出其他内容：
                {content}
                微博的发布时间为{time}，当前时间为{time}。
                输出为一个字典，包含以下四个字段：
                1. 地点：事件发生的地点。如果涉及多个地点，请拆分成多条数据，每条数据只包含一个地点。
                2. 时间：事件发生的时间。格式为“年-月-日”。如果事件持续多日，请拆分为多条数据。
                3. 事件名称：明确的事件名称，如“火灾”、“地震”、“演唱会”、“暴雨”等，不超过10个字。
                4. 程度：事件的强度或趋势。用整数表示，`1` 表示事件发生，`0` 表示事件未发生或结束。

                输出格式示例：
                [
                    {{
                        "地点": "<地点名称>",
                        "时间": "<具体日期>",
                        "事件名称": "<事件>",
                        "程度": 1  # 1 表示事件发生，0 表示事件未发生或结束
                    }},
                    {{
                        "地点": "<地点名称>",
                        "时间": "<具体日期>",
                        "事件名称": "<事件>",
                        "程度": 0  # 1 表示事件发生，0 表示事件未发生或结束
                    }}
                ]
                """}
            ],
        )
        
        # 获取响应内容并打印
        output_text = response.choices[0].message.content  # 确保返回值为字符串
        print(f"Index {i}: {output_text}")

        return i, output_text
    except Exception as e:
        print(f"Index {i} 处理失败: {e}")
        return i, None

results = []


batch_size = 200
max_workers = 10  
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    for start_idx in range(0, len(df_bj), batch_size):
        end_idx = min(start_idx + batch_size, len(df_bj))
        futures = []

        for i in range(start_idx, end_idx):
            if i not in processed_indices:
                futures.append(executor.submit(generate_event, i, df_bj['微博正文'][i], df_bj['发布时间'][i]))

        for future in as_completed(futures):
            idx, output_text = future.result()
            if output_text is not None:
                results.append((idx, output_text))
                processed_indices.add(idx)  # 记录已处理索引

        if results:
            for idx, output_text in results:
                df_bj.loc[idx, '生成结果'] = output_text


            try:
                df_bj.to_excel(output_file, index=False)
                print(f"结果已保存到 {output_file}")
            except Exception as e:
                print(f"保存文件失败：{e}")
            results = []  

        with open(progress_file, 'w') as f:
            json.dump(list(processed_indices), f)
        print(f"已处理 {end_idx}/{len(df_bj)} 条数据")

        time.sleep(1)

print("所有数据已处理并保存！")