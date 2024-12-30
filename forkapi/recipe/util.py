


def calculate_recipe_total_time(total: int) -> str:
    if total < 60:
        return f"{total:.2f}"

    hours = total // 60
    minutes = total % 60
    fractional_hours = minutes / 60
    total_hours = hours + fractional_hours
    print(total_hours)
    return f"{hours}.{minutes:02}"