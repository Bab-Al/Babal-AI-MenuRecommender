import pandas as pd
import numpy as np

def extract_menu(gender, age, categories):
    
    # 데이터 파일 열기
    data = pd.read_csv('data\\food_info.csv', encoding='cp949')

    # 원하는 데이터로 간추리기
    selected_data = data[['식품명', '식품대분류명', '대표식품명', '영양성분함량기준량', '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)']]
    selected_data = selected_data.fillna(0)

    # 사용자가 선호하는 음식 카테고리로 전처리하기
    if categories:
        preferred_data = selected_data[selected_data['식품대분류명'].isin(categories)]

    # 해당 파일의 각 음식을 벡터 값으로 나타내기
    # 각각의 특성을 0과 1 사이값으로 정규화 (min-max scaling)
    # 최대 최소값 알아내기
    kcal_max = preferred_data[['에너지(kcal)']].max().values[0]
    kcal_min = preferred_data[['에너지(kcal)']].min().values[0]

    carbo_max = preferred_data[['탄수화물(g)']].max().values[0]
    carbo_min = preferred_data[['탄수화물(g)']].min().values[0]

    protein_max = preferred_data[['단백질(g)']].max().values[0]
    protein_min = preferred_data[['단백질(g)']].min().values[0]

    fat_max = preferred_data[['지방(g)']].max().values[0]
    fat_min = preferred_data[['지방(g)']].min().values[0]

    # 정규화 표 생성하기
    normalized_data = preferred_data[['식품명']].copy()
    normalized_data['에너지(kcal)_정규화'] = (preferred_data['에너지(kcal)'] - kcal_min) / (kcal_max - kcal_min)
    normalized_data['탄수화물(g)_정규화'] = (preferred_data['탄수화물(g)'] - carbo_min) / (carbo_max - carbo_min)
    normalized_data['단백질(g)_정규화'] = (preferred_data['단백질(g)'] - protein_min) / (protein_max - protein_min)
    normalized_data['지방(g)_정규화'] = (preferred_data['지방(g)'] - fat_min) / (fat_max - fat_min)

    # 음식의 정규화된 특성 벡터
    food_vectors = normalized_data[['에너지(kcal)_정규화', '탄수화물(g)_정규화', '단백질(g)_정규화', '지방(g)_정규화']].values

    # 사용자 벡터 구하기
    user_data = pd.read_csv('data\\preffered_data.csv', encoding='cp949')
    filtered_user_data = user_data[(user_data['성별'] == gender) & (user_data['연령'] == age)]
    user_preffered_energy = filtered_user_data['필요 추정 에너지(kcal/일)'].values[0] / 3
    user_preffered_carbo = filtered_user_data['권장 섭취 탄수화물량(g/일)'].values[0] /3
    user_preffered_protein = filtered_user_data['권장 섭취 단백질량(g/일)'].values[0] / 3
    user_preffered_fat = filtered_user_data['권장 섭취 지방량(g/일)'].values[0] / 3

    normalized_user_preffered_energy = (user_preffered_energy - kcal_min) / (kcal_max - kcal_min)
    normalized_user_preffered_carbo = (user_preffered_carbo - carbo_min) / (carbo_max - carbo_min)
    normalized_user_preffered_protein = (user_preffered_protein - protein_min) / (protein_max - protein_min)
    normalized_user_preffered_fat = (user_preffered_fat - fat_min) / (fat_max - fat_min)

    user_vector = np.array([normalized_user_preffered_energy, normalized_user_preffered_carbo, normalized_user_preffered_protein, normalized_user_preffered_fat])
    
    # 각 음식과 사용자 벡터 간의 코사인 유사도 계산
    cosine_similarities = np.dot(food_vectors, user_vector) / (np.linalg.norm(food_vectors, axis=1) * np.linalg.norm(user_vector))

    # 가장 유사한 음식 찾기 (3개)
    top_n = 3
    top_food_indices = np.argsort(cosine_similarities)[::-1][:top_n]

    recommendations = []
    for idx in top_food_indices:
        name = preferred_data.iloc[idx]['식품명']
        energy = preferred_data.iloc[idx]['에너지(kcal)']
        carbo = preferred_data.iloc[idx]['탄수화물(g)']
        protein = preferred_data.iloc[idx]['단백질(g)']
        fat = preferred_data.iloc[idx]['지방(g)']
        similarities = cosine_similarities[idx]
        recommendations.append({'menuName': str(name), 'calories': float(energy), 'carbo': float(carbo), 'protein': float(protein), 'fat': float(fat), '유사도': float(similarities)})

    print(recommendations)
    return recommendations