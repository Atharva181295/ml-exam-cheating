import pandas as pd
import logging

logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

data = {
    'candidate_id': [1, 2, 3, 4, 5, 6],  
    'question_number': [1, 1, 1, 2, 2, 2],
    'answer_option': ['a', 'b', 'a', 'c', 'd', 'c'],
    'timestamp': ['2024-03-14 08:00:00', '2024-03-14 08:00:10', '2024-03-14 08:00:20',
                  '2024-03-14 08:02:00', '2024-03-14 08:02:10', '2024-03-14 08:02:15']
}

df = pd.DataFrame(data)

df['timestamp'] = pd.to_datetime(df['timestamp'])

cheating_instances = df.groupby(['question_number', 'answer_option']).filter(lambda x: len(x) > 1 and (x['timestamp'].max() - x['timestamp'].min()).seconds <= 30)

cheating_groups = cheating_instances.groupby(['question_number', 'answer_option'])

for (question_number, answer_option), group in cheating_groups:
    candidates_cheating = group['candidate_id'].unique()
    if len(candidates_cheating) > 1:
        message = f"Potential cheating detected for candidates {', '.join(map(str, candidates_cheating))} on question {question_number}, answer option {answer_option}"
        print(message)
        logging.info(message) 
