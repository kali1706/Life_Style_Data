from __future__ import annotations

from typing import Dict, Tuple


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if not weight_kg or not height_m or height_m == 0:
        return 0.0
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi: float) -> str:
    if bmi <= 0:
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def macro_ratios(carbs_g: int, proteins_g: int, fats_g: int) -> Dict[str, float]:
    carbs_kcal = (carbs_g or 0) * 4
    proteins_kcal = (proteins_g or 0) * 4
    fats_kcal = (fats_g or 0) * 9
    total = carbs_kcal + proteins_kcal + fats_kcal
    if total == 0:
        return {"carbs": 0.0, "protein": 0.0, "fat": 0.0}
    return {
        "carbs": round(100.0 * carbs_kcal / total, 1),
        "protein": round(100.0 * proteins_kcal / total, 1),
        "fat": round(100.0 * fats_kcal / total, 1),
    }


def caloric_balance(intake_kcal: int, burned_kcal: int) -> int:
    return int((intake_kcal or 0) - (burned_kcal or 0))


def heart_rate_zones(max_hr: int) -> Dict[str, Tuple[int, int]]:
    if not max_hr:
        return {}
    def pct(p: float) -> int:
        return int(round(max_hr * p))
    return {
        "zone1": (pct(0.50), pct(0.60)),
        "zone2": (pct(0.60), pct(0.70)),
        "zone3": (pct(0.70), pct(0.85)),
        "zone4": (pct(0.85), pct(1.00)),
    }
