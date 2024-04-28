import pandas as pd

def preprocess_data():
    
    # 데이터 파일 열기
    data = pd.read_csv('C:\\Users\\alsrud\\Desktop\\Babal-AI-MenuRecommender\\Babal-AI-MenuRecommender\\menu_recommendation\\data\\food_info.csv', encoding='cp949')

    # 데이터 전처리
    selected_data = data[['식품명', '식품대분류명', '대표식품명', '영양성분함량기준량', '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)', '당류(g)']]
    selected_data = selected_data.fillna(0)
    
    return selected_data