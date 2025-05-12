from database import get_user_points, set_user_points

def generate_ref_link(user_id):
    return f"https://t.me/vappeebot?start={user_id}"

def apply_referral(user_id, ref_id):
    if user_id == int(ref_id):
        return
    # Налисление бонусов пригласителю
    bonus = get_user_points(ref_id) + 10
    set_user_points(ref_id, bonus)