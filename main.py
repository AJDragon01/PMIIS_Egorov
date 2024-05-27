def count_digits(num1, num2):
    count1 = len(str(abs(num1)))
    count2 = len(str(abs(num2)))
    if count1 > count2:
        return f"В числе {num1} больше цифр ({count1})"
    elif count2 > count1:
        return f"В числе {num2} больше цифр ({count2})"
    else:
        return "Количество цифр в числах одинаково"