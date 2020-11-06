from lib.recipe import *
# recipe 2
rec = Recipe("veg_potroast","Vegetarian Pot Roast","Five Star Vegetarian Pot Roast")
rec.serves = 7 

rec.add_ingredient(Ingredient.OliveOil, 2, Quantity.tbsp)
rec.add_ingredient(Ingredient.PortabelloMushroom,5,Quantity.largeItems)
rec.add_ingredient(Ingredient.Carrot,4,Quantity.largeItems)
rec.add_ingredient(Ingredient.Onion,1,Quantity.largeItems)
rec.add_ingredient(Ingredient.Garlic,3,Quantity.cloves)
rec.add_ingredient(Ingredient.Potato, 5, Quantity.largeItems)
rec.add_ingredient(Ingredient.RedWine, 1.5, Quantity.cups)

rec.add_ingredient(Ingredient.Thyme, 1, Quantity.sprigs)
rec.add_ingredient(Ingredient.Rosemary, 1, Quantity.sprigs)
rec.add_ingredient(Ingredient.Sage, 3.5, Quantity.leaves)

rec.add_ingredient(Ingredient.TomatoPaste, 3, Quantity.tbsp);
rec.add_ingredient(Ingredient.WorchestershireSauce, 2, Quantity.tbsp)
rec.add_ingredient(Ingredient.SoySauce, 1, Quantity.tbsp)
rec.add_ingredient(Ingredient.VegetableStock, 2, Quantity.cups)

rec.add_ingredient(Ingredient.Salt, 1, Quantity.toTaste)
rec.add_ingredient(Ingredient.Pepper, 1, Quantity.toTaste)
rec.add_ingredient(Ingredient.Sugar, 1, Quantity.tbsp)
rec.add_ingredient(Ingredient.Flour, 4, Quantity.tbsp)

rec.get_ingredient(Ingredient.PortabelloMushroom).convert(Quantity.oz)
rec.get_ingredient(Ingredient.Potato).convert(Quantity.lbs)

rec.get_ingredient(Ingredient.Thyme).convert(Quantity.tspDry)
rec.get_ingredient(Ingredient.Rosemary).convert(Quantity.tspDry)
rec.get_ingredient(Ingredient.Sage).convert(Quantity.tspDry)

amt_potatoes = 1.0
potato = rec.get_ingredient(Ingredient.Potato)

step = PrepStep('''
Cut mushrooms into chunky pieces.
''')
step.set_time(10,TimeUnit.Minutes)
step.add_ingredient(Ingredient.PortabelloMushroom)
rec.add_step(step)


step = PrepStep('''
Finely chop onions and garlic.
''')
step.set_time(5,TimeUnit.Minutes)
step.add_ingredient(Ingredient.Onion)
step.add_ingredient(Ingredient.Garlic)
rec.add_step(step)


step = PrepStep('''
Peel and cut potatoes into large chunks (~5 pieces per potato).
''')
step.set_time(15,TimeUnit.Minutes)
step.add_ingredient(Ingredient.Potato)
rec.add_step(step)


step = PrepStep('''
Peel and cut carrots into one inch chunks.
''')
step.set_time(15,TimeUnit.Minutes)
step.add_ingredient(Ingredient.Carrot)
rec.add_step(step)

step = SkilletStep('''
Sautee mushrooms in olive oil / butter / water until they're golden all over. Remove
to a plate or a bowl and set aside. Reserve any of the juices for the broth.
''')
step.set_time(5,TimeUnit.Minutes)
step.add_ingredient(Ingredient.OliveOil)
step.add_ingredient(Ingredient.PortabelloMushroom)
step.set_heat(HeatLevel.MediumLow)
rec.add_step(step)

step = SkilletStep('''
Add the remaining oil and sautee onions until golden. It's important to get a good gold
color on them because that's what adds a lot of flavor. Once that's done, turn off the heat and
add the garlic immediately. Let it cook in the residual heat.
''')
step.set_time(5,TimeUnit.Minutes)
step.add_ingredient(Ingredient.OliveOil)
step.add_ingredient(Ingredient.Onion)
step.add_ingredient(Ingredient.Garlic)
step.set_heat(HeatLevel.MediumLow)
rec.add_step(step)

step = SkilletStep('''
Add the potatoes, carrots, wine, soy sauce, broth, sugar and seasonings and give a good
stir. Scrape the bottom to get all the flavor. Add the reserved mushroom broth. Add the
fresh herbs on the top.
''')
step.add_ingredient(Ingredient.Carrot)
step.add_ingredient(Ingredient.Potato)
step.add_ingredient(Ingredient.RedWine)
step.add_ingredient(Ingredient.Sugar)
step.add_ingredient(Ingredient.Salt)
step.add_ingredient(Ingredient.Pepper)
step.add_ingredient(Ingredient.TomatoPaste)
step.add_ingredient(Ingredient.WorchestershireSauce)
step.add_ingredient(Ingredient.SoySauce)
step.add_ingredient(Ingredient.Thyme)
step.add_ingredient(Ingredient.Rosemary)
step.add_ingredient(Ingredient.Sage)
step.add_ingredient(Ingredient.VegetableStock)
step.add_ingredient(Ingredient.MushroomBroth)
step.set_time(1,TimeUnit.Minutes)
rec.add_step(step)

step = SkilletStep('''
Raise the heat and bring to a simmer. Once it's simmering, seal the pot shut and let simmer
until the potatoes are soft (they can be easily poked with a fork).
''')
step.set_heat(HeatLevel.MediumLow)
step.set_time(45, TimeUnit.Minutes)
rec.add_step(step)

step = PrepStep('''
While you're waiting for the pot roast to cook, make a slurry with the flour. Gradually
add water to the flour in a small bowl until it's pourable like cream.
''')
step.set_time(2, TimeUnit.Minutes)
rec.add_step(step)

step = SkilletStep('''
Once the potatoes are soft, pour in the flour slurry and stir immediately to incorporate.
Add the mushrooms back in and stir gently again. At this point, the potatoes should be easlly soft.
Give it a few minutes to thicken / for the mushrooms to warm up.
''')
step.set_heat(HeatLevel.MediumLow)
step.set_time(45, TimeUnit.Minutes)
rec.add_step(step)


RECIPE = rec
