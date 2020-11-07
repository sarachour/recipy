from cookbook.potroast import RECIPE as potroast
from lib.recipe import Ingredient

amt_potatoes = 3.8
potato = potroast.get_ingredient(Ingredient.Potato)
potroast.scale(amt_potatoes/potato.amount)
potroast.pretty_print(prep=True)
input()
potroast.pretty_print(prep=False)
