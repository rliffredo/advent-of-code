import itertools
from collections import defaultdict
from typing import List, Tuple, Set

from common import read_data


def parse_data() -> List[Tuple[Set[str], Set[str]]]:
    raw_data = read_data("21", True)
    food_info = []
    for line in raw_data:
        raw_ingredients, raw_allergens = line.split(" (contains ")
        ingredients = set(raw_ingredients.split())
        allergens = set(i.strip(",") for i in raw_allergens.strip(")").split())
        food_info.append((ingredients, allergens))
    return food_info


def analyze_food_list(foods) -> Tuple[Set[str], List[Tuple[str, str]]]:
    # collects ingredients and allergens information
    food_with_allergens = defaultdict(list)
    possible_ingredients_for_allergen = defaultdict(set)
    all_ingredients = set(itertools.chain.from_iterable(f[0] for f in foods))
    for food_ingredients, food_allergens in foods:
        for allergen in food_allergens:
            possible_ingredients_for_allergen[allergen].update(food_ingredients)
            food_with_allergens[allergen].append((food_ingredients, food_allergens))

    # Part 1: remove all safe ingredients
    for allergen, ingredients in possible_ingredients_for_allergen.items():
        for food_ingredients, food_allergens in food_with_allergens[allergen]:
            ingredients.intersection_update(food_ingredients)

    # Part 2: assign remaining ingredients to allergen
    matched_allergens: Set[str] = set()
    while len(matched_allergens) < len(possible_ingredients_for_allergen):
        for allergen, ingredients in possible_ingredients_for_allergen.items():
            if len(ingredients) == 1:
                matched_allergens.update(list(ingredients))
            else:
                ingredients.difference_update(matched_allergens)

    ingredients_without_allergens = all_ingredients - matched_allergens
    ingredients_with_allergens = [(list(v)[0], k) for k, v in possible_ingredients_for_allergen.items()]

    return ingredients_without_allergens, ingredients_with_allergens


def part_1(print_result: bool = True) -> int:
    foods = parse_data()
    safe_ingredients, _ = analyze_food_list(foods)

    ingredient_mentions = (ingredient for ingredient in itertools.chain.from_iterable(f[0] for f in foods))
    count_of_safe_ingredient_mentions = [ingredient in safe_ingredients
                                         for ingredient in ingredient_mentions].count(True)

    if print_result:
        print(f"The number of mentions of safe ingredients is {count_of_safe_ingredient_mentions}")
    return count_of_safe_ingredient_mentions


def part_2(print_result: bool = True) -> str:
    foods = parse_data()
    _, ingredients_with_allergens = analyze_food_list(foods)

    canonical_list = ",".join(i[0] for i in sorted(ingredients_with_allergens, key=lambda i: i[1]))
    result = canonical_list
    if print_result:
        print(f"Canonical list with allergens is {result}")
    return result


SOLUTION_1 = 2265
SOLUTION_2 = "dtb,zgk,pxr,cqnl,xkclg,xtzh,jpnv,lsvlx"

if __name__ == "__main__":
    part_1()
    part_2()
