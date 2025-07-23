# core/recommendation.py

from typing import Dict


def generate_weight_loss_plan(der: float, species: str) -> Dict[str, float]:
    """
    تولید برنامه کاهش وزن ایمن برای سگ یا گربه بر اساس DER

    Args:
        der (float): نیاز انرژی روزانه (Daily Energy Requirement)
        species (str): گونه حیوان ('dog' یا 'cat')

    Returns:
        Dict[str, float]: دیکشنری شامل:
            - target_kcal: کالری هدف برای مصرف روزانه
            - reduction_percent: درصد کاهش نسبت به DER
            - note: توضیح درباره برنامه کاهش وزن
    """
    species_lower = species.lower()
    plan: Dict[str, float] = {}

    if species_lower == "dog":
        # کاهش 20٪ برای سگ‌ها
        reduction_rate = 0.20
        target_kcal = round(der * (1 - reduction_rate), 2)
        note = (
            "کاهش وزن ایمن برای سگ: 20٪ از DER کاسته شود "
            f"(مقدار هدف: {target_kcal} kcal)"
        )
        plan = {
            "target_kcal": target_kcal,
            "reduction_percent": int(reduction_rate * 100),
            "note": note
        }

    elif species_lower == "cat":
        # کاهش 25٪ برای گربه‌ها با حداقل 180 kcal
        reduction_rate = 0.25
        calculated = der * (1 - reduction_rate)
        target_kcal = round(calculated, 2)
        if target_kcal < 180:
            target_kcal = 180.0
        note = (
            "کاهش وزن ایمن برای گربه: حدود 25٪ از DER کاسته شود "
            f"(مقدار هدف: {target_kcal} kcal یا حداقل 180 kcal)"
        )
        plan = {
            "target_kcal": target_kcal,
            "reduction_percent": int(reduction_rate * 100),
            "note": note
        }

    else:
        raise ValueError("گونه وارد شده باید 'dog' یا 'cat' باشد.")

    return plan


# مثال تست
if __name__ == '__main__':
    der_dog = 800.0
    der_cat = 300.0
    print('Dog plan:', generate_weight_loss_plan(der_dog, 'dog'))
    print('Cat plan:', generate_weight_loss_plan(der_cat, 'cat'))
