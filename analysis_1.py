import sys
sys.path.insert(0, "C:/Users/dwlal/my_python_libs")

import pandas as pd
from transformers import pipeline

# 1. 다국어 감정 분석 모델 사용
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=model_name,
    tokenizer=model_name,
    truncation=True  # 너무 긴 문장은 자동 자름
)

# 2. 파일 불러오기
file_path = "C:/Users/dwlal/댓글_수집_세윤/댓글_뉴스/뉴스2.xlsx"
df = pd.read_excel(file_path)
comments = df['comment'].astype(str).tolist()

# 3. 감정 분석 실행 (한 번에)
results = sentiment_pipeline(comments)

# 4. 결과 정리
df['sentiment'] = [r['label'] for r in results]
df['score'] = [r['score'] for r in results]

# 5. 감정 점수 추출 (1~5점)
def extract_score(label):
    return int(label.split()[0])

df['sentiment_score'] = df['sentiment'].apply(extract_score)

# 6. 한국어 감정명 추가
def score_to_kor(score):
    if score <= 2:
        return "부정"
    elif score == 3:
        return "중립"
    else:
        return "긍정"

df['sentiment_kor'] = df['sentiment_score'].apply(score_to_kor)

# 7. 결과 저장
output_path = "C:/Users/dwlal/댓글_수집_세윤/댓글_뉴스/뉴스2_감정분석.xlsx"
df.to_excel(output_path, index=False)

print("✅ 다국어 감정 분석 완료! 저장 위치:", output_path)
