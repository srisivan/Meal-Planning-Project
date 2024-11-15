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

def greedy_meal_plan(breakfast_calories, food_calories, drink_calories, drink_item):
    allocation = {}
    calorie_density = {}

    # Step 1: Compute calorie density for each food and drink
    for food, calorie_per_unit in food_calories.items():
        calorie_density[food] = calorie_per_unit
    calorie_density["drink"] = drink_calories

    # Step 2: Sort items by calorie density in descending order
    sorted_items = sorted(calorie_density.items(), key=lambda x: x[1], reverse=True)

    # Step 3: Allocate items greedily
    remaining_calories = breakfast_calories
    for item, calorie_per_unit in sorted_items:
        max_units = math.floor(remaining_calories / calorie_per_unit)
        allocation[item] = max_units
        remaining_calories -= max_units * calorie_per_unit

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

# Allocate meal plan using greedy algorithm
allocation, drink_item = greedy_meal_plan(breakfast_calories, food_calories, drink_calories, drink_item)

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
