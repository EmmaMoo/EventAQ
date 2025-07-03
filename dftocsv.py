import json
import pandas as pd

input_file = 'event.xlsx'
output_file = 'event_out.csv'

df = pd.read_excel(input_file)

data = []

for index, row in df.iterrows():
    微博id = row['微博id']
    微博正文 = row['微博正文']
    
    try:

        event = json.loads(row['生成结果'])  
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e} at row {index} for 微博id: {微博id}")
        continue  


    if isinstance(event, dict) and '地点' in event and '时间' in event and '事件名称' in event and '程度' in event:

        if isinstance(event['地点'], list) and isinstance(event['时间'], list) and isinstance(event['事件名称'], list)and isinstance(event['程度'], list):

            for location in event['地点']:
                for date in event['时间']:

                    if len(event['事件名称']) == len(event['程度']):
                        data.extend({
                            '微博id': 微博id,
                            '微博正文': 微博正文,
                            '地点': location,
                            '时间': date,
                            '事件名称': event_name,
                            '程度': event_degree
                        } for event_name, event_degree in zip(event['事件名称'], event['程度']))
                    else:
                        data.extend({
                            '微博id': 微博id,
                            '微博正文': 微博正文,
                            '地点': location,
                            '时间': date,
                            '事件名称': event_name,
                            '程度': 1  
                        } for event_name in event['事件名称'])

        else:

            data.append({
                '微博id': 微博id,
                '微博正文': 微博正文,
                '地点': event['地点'],  
                '时间': event['时间'],   
                '事件名称': event['事件名称'],  
                '程度': event['程度']
            })
    else:
        print(f"跳过微博id {微博id}，事件数据格式不符合要求，行 {index}")


output_df = pd.DataFrame(data)


output_df.to_csv(output_file, index=False)

print(f"csv文件已生成：{output_file}")
unique_events = output_df['事件名称'].dropna().unique()
pd.DataFrame({'事件名称': unique_events}).to_csv('list.csv', index=False, encoding='utf-8-sig')
print('事件名称去重后已保存为 list.csv')
