def add_new_recipe(recipes, elf1, elf2):
    new_recipe = recipes[elf1] + recipes[elf2]
    if new_recipe < 10:
        recipes.append(new_recipe)
    else:
        recipes.append(new_recipe // 10)
        recipes.append(new_recipe % 10)

def next_elf_recipe(recipes, elf):
    return (elf + recipes[elf] + 1) % len(recipes)

def recipe_score(recipes, iterations, size):
    return ''.join(str(score) for score in recipes[iterations:iterations+size])

def calculate_score(recipes, elf1, elf2, iterations):
    while len(recipes) < iterations+10:
        add_new_recipe(recipes, elf1, elf2)
        elf1 = next_elf_recipe(recipes, elf1)
        elf2 = next_elf_recipe(recipes, elf2)
    return recipe_score(recipes, iterations, 10)

recipes = [3, 7]
elf1 = 0
elf2 = 1
iterations = 320851

print(f'The score after {iterations} iterations is {calculate_score(recipes, elf1, elf2, iterations)}')

###################

def calculate_iterations(recipes, elf1, elf2, target_score):
    iteration = 0
    while True:
        while len(recipes) < iteration + len(target_score):
            add_new_recipe(recipes, elf1, elf2)
            elf1 = next_elf_recipe(recipes, elf1)
            elf2 = next_elf_recipe(recipes, elf2)
        if recipe_score(recipes, iteration, len(target_score)) == target_score:
            return iteration
        iteration += 1

target_score = '320851'
recipes = [3, 7]
elf1 = 0
elf2 = 1

print(f'Iterations required to reach `{target_score}`: {calculate_iterations(recipes, elf1, elf2, target_score)}')
