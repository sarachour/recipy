
from enum import Enum
import pint

class Ingredient(Enum):
    Onion = "onion"
    Potato = "potato"
    Carrot = "carrot"
    OliveOil = "olive oil"
    PortabelloMushroom = "portabello mushroom"
    MushroomBroth = "mushroom broth"
    Garlic = "garlic"
    RedWine = "red wine"
    Thyme = "thyme"
    Rosemary = "rosemary"
    Sage = "sage"
    TomatoPaste = "tomato paste"
    WorchestershireSauce = "worchestershire sauce"
    SoySauce = "soy sauce"
    VegetableStock = "vegetable stock"
    Salt = "salt"
    Pepper = "pepper"
    Sugar = "sugar"
    Flour = "flour"

class Quantity(Enum):
    lbs = "lbs"
    oz = "oz"
    tbsp = "tbsp"
    tsp = "tsp"
    tspDry = "tsp dry"
    tspFresh = "tsp fresh"
    largeItems = "large items"
    cloves = "cloves"
    cups = "cups"
    sprigs = "sprigs"
    leaves = "leaves"
    toTaste = "to taste"

class ConversionEngine:

    def __init__(self):
        self.rules = {}
        self.general_rules = {}

    def _add_rule(self,ingredient,quantity,targ_qty,amount):
        if not ingredient in self.rules:
            self.rules[ingredient] = {}

        if not quantity in self.rules[ingredient]:
            self.rules[ingredient][quantity] = {}

        if(targ_qty in self.rules[ingredient][quantity]):
            return
        self.rules[ingredient][quantity][targ_qty] = amount

    def add_rule(self,ingredient,quantity,targ_qty,amount):
        self._add_rule(ingredient,quantity,targ_qty,amount);
        self._add_rule(ingredient,targ_qty,quantity,1.0/amount);
        if targ_qty in self.general_rules:
            for transitive_targ in self.general_rules[targ_qty]:
                xamt = self.general_rules[targ_qty][transitive_targ]
                self._add_rule(ingredient,quantity,transitive_targ,amount*xamt)
                self._add_rule(ingredient,transitive_targ,quantity,1.0/(amount*xamt))

    def _add_general_rule(self,quantity,targ_qty,amount):
        if not quantity in self.general_rules:
            self.general_rules[quantity] = {}

        assert(not targ_qty in self.general_rules[quantity])
        self.general_rules[quantity][targ_qty] = amount

    def add_general_rule(self,quantity,targ_qty,amount):
        self._add_general_rule(quantity,targ_qty,amount);
        self._add_general_rule(targ_qty,quantity,1.0/amount);


    def convert(self,ingredient,amount,quantity,target_qty):
        if ingredient in self.rules and \
           quantity in self.rules[ingredient] and \
           target_qty in self.rules[ingredient][quantity]:
            return self.rules[ingredient][quantity][target_qty]*amount

        if quantity in self.general_rules and \
           targ_qty in self.general_rules[quantity]:
            return self.general_rules[quantity][target_qty]*amount

        raise Exception("ingredient <%s> cannot convert %s -> %s" \
                        % (ingredient,quantity,target_qty))


conversionEngine = ConversionEngine()
conversionEngine.add_general_rule(Quantity.lbs, \
                                  Quantity.oz, \
                                  16)


conversionEngine.add_rule(Ingredient.PortabelloMushroom, \
                         Quantity.largeItems, \
                         Quantity.oz, \
                         3.5)

conversionEngine.add_rule(Ingredient.Potato, \
                         Quantity.largeItems, \
                         Quantity.oz, \
                         13)

conversionEngine.add_rule(Ingredient.Rosemary, \
                          Quantity.sprigs, \
                          Quantity.tspDry, \
                          0.5)

conversionEngine.add_rule(Ingredient.Thyme, \
                          Quantity.sprigs, \
                          Quantity.tspDry, \
                          0.5)

conversionEngine.add_rule(Ingredient.Sage, \
                          Quantity.leaves, \
                          Quantity.tspDry, \
                          1.0/7.0)


class RecipeIngredient:

    def __init__(self,ingredient,quantity,unit):
        assert(isinstance(ingredient,Ingredient))
        assert(isinstance(unit,Quantity))
        self.ingredient = ingredient
        self.amount = quantity
        self.unit = unit

    def scale(self,factor):
        self.amount *= factor

    def convert(self,new_unit):
        self.amount = conversionEngine.convert(self.ingredient,
                                               self.amount, \
                                               self.unit, new_unit)
        self.unit = new_unit

    def pretty_print(self):
        nchars = len(self.ingredient.value)
        pad = ' '*(25-nchars)
        print('- %s:%s%.02f %s'  % (self.ingredient.value, \
                                    pad, \
                                    self.amount, \
                                    self.unit.value))

class Recipe:

    def __init__(self,ident,name,description):
        self.ident = ident
        self.name = name
        self.desc = description
        self.serves = 4
        self.steps = []
        self.ingredients = {}

    def scale(self,amt):
        for ing in self.ingredients.values():
            ing.scale(amt)

        self.serves *= amt

    def add_ingredient(self,ingredient,quantity,unit):
        ing = RecipeIngredient(ingredient,quantity,unit)
        assert(not ingredient.name in self.ingredients)
        self.ingredients[ingredient.name] = ing

    def get_ingredient(self,ingredient):
        return self.ingredients[ingredient.name]

    def add_step(self,step):
        self.steps.append(step)

    def pretty_print(self,prep=False):
        stmts =[
            "==== %s ====" % self.name,
            self.desc,
            "serves: %d" % self.serves,
            "",
        ]
        print("\n".join(stmts))
        if prep:
            print("==== Ingredients ====")
            for ing in self.ingredients.values():
                ing.pretty_print()

        print("\n\n")
        print("==== Steps ====")
        for step in self.steps:
            if prep and isinstance(step,PrepStep):
                step.pretty_print()
            elif not prep and not isinstance(step,PrepStep):
                step.pretty_print()

class TimeUnit(Enum):
    Minutes = "minutes"
    Seconds = "seconds"
    Hours = "hours"

class HeatLevel(Enum):
    Medium = "medium"
    High = "high"
    MediumHigh= "medium-high"
    MediumLow = "medium-low"
    Low = "low"
    Unknown = "unknown"

class Time:

    def __init__(self,amount,unit):
        assert(isinstance(unit,TimeUnit))
        self.amount = amount
        self.unit = unit

    def __repr__(self):
        return "%.2f %s" % (self.amount,self.unit.value)

class Step:

    def __init__(self,prose):
        self.prose = prose.split("\w")
        self.time = Time(None,TimeUnit.Minutes)
        self.ingredients = []

    def set_time(self,time,unit):
        self.time = Time(time,unit)

    def add_ingredient(self,ingredient,amt=None,unit=Quantity.oz):
        self.ingredients.append(RecipeIngredient(ingredient,amt,unit))

    def pretty_print(self):
        its = map(lambda ing: ing.ingredient.value, \
                  self.ingredients)

        print("time:  %s" % self.time)
        print("items:%s" % (", ".join(its)))
        print(" ".join(self.prose))
        print("\n")

class SkilletStep(Step):

    def __init__(self,prose):
        Step.__init__(self,prose)
        self.heat = HeatLevel.Unknown

    def set_heat(self,heat):
        self.heat = heat

    def pretty_print(self):
        print("heat: %s" % self.heat.value)
        Step.pretty_print(self)

class PrepStep(Step):

    def __init__(self,prose):
        Step.__init__(self,prose)

    def pretty_print(self):
        Step.pretty_print(self)

