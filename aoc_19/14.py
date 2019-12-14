import math
from dataclasses import dataclass
from typing import List, Dict

from common import read_data


@dataclass
class Component:
    element: str
    amt: int

    @staticmethod
    def from_string(str_component: str):
        amt, element = str_component.split()
        return Component(amt=int(amt), element=element)


@dataclass
class Reaction:
    reactants: List[Component]
    product: Component


@dataclass
class ReactionContext:
    reactions: Dict[str, Reaction]
    available_elements: Dict[str, int]
    consumed_ore: int = 0


def parse_data(data):
    all_reactions: Dict[str, Reaction] = {}
    for line in data:
        ingredients, result = line.split('=>')
        reactants = [Component.from_string(c) for c in ingredients.split(',')]
        product = Component.from_string(result)
        all_reactions[product.element] = Reaction(reactants=reactants, product=product)
    return ReactionContext(reactions=all_reactions, available_elements={}, consumed_ore=0)


def consume_element(reactant: Component, rc: ReactionContext) -> None:
    available_reactant = rc.available_elements.get(reactant.element, 0)
    if available_reactant < reactant.amt:
        needed_reactant = reactant.amt - available_reactant
        make_element(reactant.element, needed_reactant, rc)
    rc.available_elements[reactant.element] -= reactant.amt


def make_element(element: str, needed_amount: int, rc: ReactionContext) -> ReactionContext:
    if element == 'ORE':
        rc.consumed_ore += needed_amount
        rc.available_elements['ORE'] = rc.available_elements.get('ORE', 0) + needed_amount
        return rc
    recipe_for_element = rc.reactions[element]
    recipe_executions = math.ceil(needed_amount / recipe_for_element.product.amt)
    for _ in range(recipe_executions):
        for reactant in recipe_for_element.reactants:
            consume_element(reactant, rc)
        rc.available_elements[recipe_for_element.product.element] = rc.available_elements.get(
            recipe_for_element.product.element, 0) + recipe_for_element.product.amt


################
# ## PART 1 ## #
################

def create_fuel(reaction_context: ReactionContext) -> int:
    make_element('FUEL', 1, reaction_context)
    return reaction_context.consumed_ore


raw_recipes = read_data("14", by_lines=True)
parsed_reaction_context = parse_data(raw_recipes)
print(f'To produce one FUEL we need {create_fuel(parsed_reaction_context)} ORE')  # 870051


################
# ## PART 2 ## #
################

def calculate_trillion(reaction_context: ReactionContext) -> int:
    trillion = 1000000000000
    # Approximate the amount. We cannot get "too near" the correct solution, or not all material
    # will be used, leading to smaller yields
    initial_amt = 5000
    correcting_factor = 0.99
    print(f'***** INITIAL AMOUNT: {initial_amt} CORRECTING FACTOR: {correcting_factor*100}% ******')
    make_element('FUEL', initial_amt, reaction_context)
    # The approximation is like running on parallel lines, and then putting everything together,
    # and then checking if we can do some more.
    production_lines = math.floor(trillion * correcting_factor / reaction_context.consumed_ore)
    for element in reaction_context.available_elements:
        reaction_context.available_elements[element] *= production_lines
    reaction_context.consumed_ore *= production_lines
    fuel_made = initial_amt * production_lines
    # Note: a better approach might be to add in thousands, then in hundreds, tens, units as
    # we get nearer (or surpass).
    # The current algorithm is very slow, and should be improved, but that might require a
    # refactoring of `make_element`
    while reaction_context.consumed_ore < trillion:
        print(f'With {reaction_context.consumed_ore} ORE we are producing {fuel_made} FUEL')
        make_element('FUEL', 1, reaction_context)
        fuel_made += 1
    return fuel_made - 1


parsed_reaction_context = parse_data(raw_recipes)
print(f'With one trillion ORE we can produce {calculate_trillion(parsed_reaction_context)} FUEL')  # 1863741
