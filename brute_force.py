import math

def calculate_daily_calories(age, weight, height):
    # Harris-Benedict equation (simplified): Men: BMR = 88.362 + (13.397 * weight in kg) + (4.799 * height in cm) - (5.677 * age)
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    total_calories = bmr * 1.2
    return total_calories

def divide_calories(total_calories):
    # Dividing calories into meals: 30% breakfast, 40% lunch, 30% dinner
    breakfast_calories = total_calories * 0.3
    lunch_calories = total_calories * 0.4
    dinner_calories = total_calories * 0.3
    return breakfast_calories, lunch_calories, dinner_calories

def meal_plan_allocation(breakfast_calories, food_calories, drink_calories, drink_item):
    remaining_calories = breakfast_calories
    allocation = {}

    # Step 1: Allocate at least one unit of each solid food item
    for food, calorie_per_unit in food_calories.items():
        allocation[food] = 1
        remaining_calories -= calorie_per_unit

    # Step 2: Try to allocate the drink (first check for 1 glass, then 0.5 glass)
    drink_calories_full = drink_calories
    drink_calories_half = drink_calories_full / 2
    if remaining_calories >= drink_calories_full:
        allocation["drink"] = 1
        remaining_calories -= drink_calories_full
    elif remaining_calories >= drink_calories_half:
        allocation["drink"] = 0.5
        remaining_calories -= drink_calories_half
    else:
        allocation["drink"] = 0  # No drink if not enough calories

    # Step 3: Redistribute remaining calories among solid foods
    for food, calorie_per_unit in food_calories.items():
        max_additional_units = math.floor(remaining_calories / calorie_per_unit)
        allocation[food] += max_additional_units
        remaining_calories -= max_additional_units * calorie_per_unit

    return allocation, drink_item

# Input
age = int(input("Enter age: "))
weight = float(input("Enter weight in kg: "))
height = float(input("Enter height in cm: "))

print("\n")

# Get meal and drink details from the user
num_items = int(input("Enter number of items: "))
food_calories = {}

print("Enter meal plan in this format: [food] [calorie per unit]\n")
for i in range(num_items - 1):  # All items except the last one (drink)
    item, calorie = input().split()
    food_calories[item] = int(calorie)

# Last item is the drink
drink_item, drink_calorie = input("Enter the drink and calorie per unit:").split()
drink_calories = int(drink_calorie)

# Calculate total daily calories and divide into meals
total_calories = calculate_daily_calories(age, weight, height)
breakfast_calories, _, _ = divide_calories(total_calories)

# Allocate meal plan for breakfast
allocation, drink_item = meal_plan_allocation(breakfast_calories, food_calories, drink_calories, drink_item)

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
