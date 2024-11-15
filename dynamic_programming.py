import math

def calculate_daily_calories(age, weight, height):
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    total_calories = bmr * 1.2
    return total_calories

def divide_calories(total_calories):
    breakfast_calories = total_calories * 0.3
    lunch_calories = total_calories * 0.4
    dinner_calories = total_calories * 0.3
    return breakfast_calories, lunch_calories, dinner_calories

def dp_meal_plan(breakfast_calories, food_calories, drink_calories, drink_item):
    items = list(food_calories.keys()) + ["drink"]
    calories = list(food_calories.values()) + [drink_calories]
    n = len(items)

    # DP table initialization
    dp = [[0] * (int(breakfast_calories) + 1) for _ in range(n + 1)]
    allocation = {}

    # Populate DP table
    for i in range(1, n + 1):
        for w in range(int(breakfast_calories) + 1):
            if calories[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - int(calories[i - 1])] + calories[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Traceback to find allocation
    w = int(breakfast_calories)
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item = items[i - 1]
            if item not in allocation:
                allocation[item] = 0
            allocation[item] += 1
            w -= int(calories[i - 1])

    return allocation, drink_item

# Input
age = int(input("Enter age: "))
weight = float(input("Enter weight in kg: "))
height = float(input("Enter height in cm: "))

print("\n")

num_items = int(input("Enter number of items: "))
food_calories = {}

print("Enter meal plan in this format: [food] [calorie per unit]\n")
for i in range(num_items - 1):
    item, calorie = input().split()
    food_calories[item] = int(calorie)

drink_item, drink_calorie = input("Enter the drink and calorie per unit:").split()
drink_calories = int(drink_calorie)

# Calculate total daily calories and divide into meals
total_calories = calculate_daily_calories(age, weight, height)
breakfast_calories, _, _ = divide_calories(total_calories)

# Allocate meal plan using dynamic programming
allocation, drink_item = dp_meal_plan(breakfast_calories, food_calories, drink_calories, drink_item)

# Output
print("\n--- Optimized Breakfast Meal Plan ---")
print(f"Total breakfast calories target: {breakfast_calories:.2f} cal")
for food, units in allocation.items():
    total_calories_item = units * (food_calories.get(food, drink_calories) if food != "drink" else drink_calories)
    if food == "drink" and units == 0:
        print(f"{drink_item.capitalize()}: Not included")
    elif food == "drink":
        print(f"{drink_item.capitalize()}: {units} glass(es) ({total_calories_item:.2f} cal)")
    else:
        print(f"{food.capitalize()}: {units} unit(s) ({total_calories_item} cal)")
