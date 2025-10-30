# game_logic.py
def calculate_nutrition(selected_foods):
    """選択された食品の合計栄養価を計算する"""
    total_nutrition = {k: 0 for k in list(FOOD_DATA.values())[0].keys()}
    
    for food_name in selected_foods:
        if food_name in FOOD_DATA:
            for nutrient, value in FOOD_DATA[food_name].items():
                total_nutrition[nutrient] += value
    
    return total_nutrition

def evaluate_balance(target_user, selected_foods):
    """栄養バランスを評価し、スコアを返す"""
    target_rda = TARGET_RDA.get(target_user)
    if not target_rda:
        return 0, "対象者不明"

    current_nutrition = calculate_nutrition(selected_foods)
    score = 0
    feedback = []

    # 評価ロジック: 主要な3大栄養素を評価
    nutrients_to_check = ["エネルギー(kcal)", "タンパク質(g)", "脂質(g)", "炭水化物(g)"]
    
    # 理想的な目標値（例えば、一日の推奨摂取量の1/3を目標とする）
    MEAL_FACTOR = 0.33 
    
    for nutrient in nutrients_to_check:
        target_value = target_rda[nutrient] * MEAL_FACTOR
        current_value = current_nutrition.get(nutrient, 0)
        
        # 達成率を計算
        ratio = current_value / target_value
        
        # 理想的な割合（例: 0.8倍〜1.2倍）に収まっているか
        if 0.8 <= ratio <= 1.2:
            # 理想的な範囲なら高得点
            score += 100 
            feedback.append(f"✅ {nutrient}: 理想的なバランスです。")
        elif 0.5 <= ratio < 0.8:
            score += 50
            feedback.append(f"⚠️ {nutrient}: 少し不足しています。")
        elif ratio < 0.5:
            feedback.append(f"❌ {nutrient}: 大幅に不足しています！")
        elif ratio > 1.5:
            feedback.append(f"❌ {nutrient}: 摂取しすぎです！")
        elif ratio > 1.2:
            score += 30
            feedback.append(f"⚠️ {nutrient}: やや過剰です。")

    # 総合スコア (最大400点 + ボーナス)
    final_score = score + len(selected_foods) * 5 # 品目数ボーナス（多様性）

    return final_score, "\n".join(feedback)

# 実行例: 
# selected = ["ごはん", "ゆで卵", "きゅうり"]
# final_score, feedback = evaluate_balance("成人男性", selected)
# print(f"スコア: {final_score}\nフィードバック:\n{feedback}")
