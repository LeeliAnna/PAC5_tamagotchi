import os

from numpy.ma.mrecords import reserved_fields

os.environ['SDL_VIDEO_WINDOW_POS'] = "350,45"
import pgzrun
import pgzero.actor
import pgzero.clock
import pgzero.screen
import pgzero.keyboard

Actor = pgzero.actor.Actor
clock : pgzero.clock.Clock
screen : pgzero.screen.Screen
keyboard : pgzero.keyboard.Keyboard

from datetime import datetime
from random import randint
from Dog import Dog
                                            #---------- Constantes ----------#
HEIGHT = 800
WIDTH = 600
ACTOR_POSITION_X = WIDTH/2 - 10
ACTOR_POSITION_Y = HEIGHT/2 + 10
ICONS_POSITION_X = WIDTH /2 + 5
ICONS_POSITION_Y = ACTOR_POSITION_Y
TIME = 6
WIN_CONDITION = 3

                                    #---------- Variables d'environnement ----------#
timer = TIME
activity_choice = -1
activity_selected = False
meal_choice = 0
meal_selected = False
cleaning_choice = 0
cleaning_selected = False
current_date = datetime.now()
light_off = None
night = False
game_on = False
game_choice = -1
husky_number = -2
win = 0
game_choice_selected = False

                                            #---------- Images ----------#
                                                    # Background
background = Actor("tamagochi_base_v2")
                                                    # Tamagotchi
husky = Dog("husky")
husky.x = ACTOR_POSITION_X
husky.y = ACTOR_POSITION_Y
                                                    # Nourriture
carrot = Actor("nourriture_carrotte_0001")
carrot.x = ACTOR_POSITION_X
carrot.y = ACTOR_POSITION_Y
nuggets = Actor("nourriture_carrotte_0002")
nuggets.x = ACTOR_POSITION_X
nuggets.y = ACTOR_POSITION_Y
                                                    # Médicament
medications = ["medicament_0003","medicament_0002","medicament_0001"]
medication = Actor("medicament_0003")
medication.index_animation = 0
medication.fps = 6
medication.x = ACTOR_POSITION_X
medication.y = ACTOR_POSITION_Y
                                                        # Caca
poops = ["caca_0001", "caca_0002"]
poop = Actor("caca_0001")
poop.index_animation = 0
poop.fps = 3
poop.x = ACTOR_POSITION_X
poop.y = ACTOR_POSITION_Y
                                                # Nettoyer le chien
cleaning_dog_table = ["husky_lavage_0001", "husky_lavage_0002"]
cleaning_dog = Actor("husky_lavage_0001")
cleaning_dog.index_animation = 0
cleaning_dog.fps = 3
cleaning_dog.x = ACTOR_POSITION_X
cleaning_dog.y = ACTOR_POSITION_Y
                                                #Icone de choix de nettoyage
cleaning_poop = Actor("sous_menu_nettoyage_caca")
cleaning_poop.x = ACTOR_POSITION_X
cleaning_poop.y = ACTOR_POSITION_Y

duck = Actor("sous_menu_nettoyage_bain")
duck.x = ACTOR_POSITION_X
duck.y = ACTOR_POSITION_Y

                                            # ---------- Jeux ---------- #
game_left_right =["husky_jeux_gauche_droite_0001","husky_jeux_gauche_droite_0002"]
husky_game_left_right = Actor("husky_jeux_gauche_droite_0001")
husky_game_left_right.x = ACTOR_POSITION_X
husky_game_left_right.y = ACTOR_POSITION_Y
husky_game_left_right.fps = 3
husky_game_left_right.index_animation = 0

                                                # Menu d'actvités
activities_images = [
                        ["nourriture_vide_3", "nourriture_3"],
                        ["seringue_vide","seringue_pleine"],
                        ["menu_nettoyage_dog", "menu_nettoyage_dog_pleins"],
                        ["menu_jeu_vide", "menu_jeu_plein"],
                        ["menu_ampoule_vide", "menu_ampoule_plein"]
                    ]

icon_meal = Actor("nourriture_vide_3")
icon_meal.x = ICONS_POSITION_X
icon_meal.y = ICONS_POSITION_Y

icon_medication = Actor("seringue_vide")
icon_medication.x = ICONS_POSITION_X
icon_medication.y = ICONS_POSITION_Y

icon_cleaning = Actor("menu_nettoyage_dog")
icon_cleaning.x = ICONS_POSITION_X
icon_cleaning.y = ICONS_POSITION_Y

icon_game = Actor("menu_jeu_vide")
icon_game.x = ICONS_POSITION_X
icon_game.y = ICONS_POSITION_Y

icon_light = Actor("menu_ampoule_vide")
icon_light.x = ICONS_POSITION_X
icon_light.y = ICONS_POSITION_Y

activities_actors = [
                        icon_meal,
                        icon_medication,
                        icon_cleaning,
                        icon_game,
                        icon_light
                    ]

icon_game = Actor("sous_meu_jeu_vide")
icon_game.x = ICONS_POSITION_X
icon_game.y = ICONS_POSITION_Y
icons_game = ["sous_meu_jeu_droite", "sous_meu_jeu_gauche"]

# icon_heart_1 = Actor("heart")
hearts = []
icon_heart = Actor("heart")
icon_heart.x = ACTOR_POSITION_X + 60
icon_heart.y = ACTOR_POSITION_Y
# for live in range(0, icon_heart_1.width * WIN_CONDITION , icon_heart_1.width):
#     icon_heart = Actor("heart")
#     icon_heart.x = ACTOR_POSITION_X
#     icon_heart.y = ACTOR_POSITION_Y
#     # hearts.append(icon_heart)



                                        # ---------- Draw et update ----------

def draw():
    global activity_choice,activity_selected,meal_choice,meal_selected

    screen.clear()
    background.draw()

    if game_on:
        icon_game.draw()
        if win > 0:
            for heart in hearts:
                heart.draw()
    else:
        for activity in activities_actors:
            activity.draw()

    if not activity_selected:
        if husky.do_poop:
            poop.draw()
        else:
            husky.draw()
    elif activity_choice == 0 and activity_selected:
        if meal_choice == 0:
            carrot.draw()
        if meal_choice == 1:
            nuggets.draw()
    elif activity_choice == 1 and activity_selected:
        medication.draw()
    elif activity_choice == 2 and activity_selected:
        if cleaning_choice == 0:
            cleaning_poop.draw()
        if cleaning_choice == 1:
            duck.draw()
        if cleaning_choice == 1 and cleaning_selected:
            cleaning_dog.draw()
    else:
        husky.draw()

def update(dt):
    global timer, night, game_on

    if night:
        background.image = "tamagochi_base_v2_nuit"

    if game_on:
        if game_choice == -1:
            icon_game.image = "sous_meu_jeu_vide"
        elif game_choice == 0:
            icon_game.image = "sous_meu_jeu_droite"
        elif game_choice == 1:
            icon_game.image = "sous_meu_jeu_gauche"
        # for heart in hearts:
        #     heart.draw()
    else:
        for index in range(len(activities_images)):
            if activity_choice == index:
                activities_actors[index].image = activities_images[index][1]
            else:
                activities_actors[index].image = activities_images[index][0]

    if husky.do_poop:
        clock.schedule_interval(pooping_animation, 1 / poop.fps)
    if timer <= 0:
        if not night:
            if not husky.is_sleeping and not husky._is_sleeping and not husky.in_game:
                husky.when_timer_is_over()
        timer = TIME
    timer -= dt


                        # ---------- Déclarations des touches pour contrôler le jeu ----------

def on_key_down(key):
    global activity_choice,activity_selected, night, timer, cleaning_selected, meal_selected, game_on, game_choice, game_choice_selected, husky_number

    if activity_selected and not night:
        if activity_choice == 0:
            second_menu(key, 0)
        if activity_choice == 2:
            second_menu(key, 2)
    elif night:
        activity_choice = 4
        if key == key.SPACE:
            night = False
            husky._is_sleeping = False
            reset_activities()
        return
    else:
        if key == key.RIGHT:
            activity_choice += 1
        elif key == key.LEFT:
            activity_choice -= 1
        elif key == key.SPACE:
            if activity_choice > -1:
                activity_selected = True

    if activity_choice < -1:
        activity_choice = len(activities_actors) - 1
    elif activity_choice >= len(activities_actors):
        activity_choice = -1


    if activity_choice == 1 and activity_selected:
        # clock.schedule_interval(actors_animations_unique(medication,medications), 1/medication.fps)
        clock.schedule_interval(medication_animation, 1/medication.fps)
    if activity_choice == 3 and activity_selected:
        if not game_on or not game_choice_selected:
            husky_number = randint(0, 1)
        game_on = True
        husky.in_game = True

        if key == key.RIGHT:
            game_choice = 0
        elif key == key.LEFT:
            game_choice = 1
        elif key == key.SPACE:
            if game_choice != -1:
                game_choice_selected = True
        if game_choice_selected:
            game_1(husky_number)

    if activity_choice == 4 and activity_selected:
        if not night:
            night = True
            husky._is_sleeping = True
            get_shutdown()

def second_menu(keyboard, choice):
    global meal_choice,meal_selected, cleaning_choice, cleaning_selected
    if night or game_on:
        return
    
    if choice == 0:
        if keyboard == keyboard.RIGHT:
            meal_choice = 0
        elif keyboard == keyboard.LEFT:
            meal_choice = 1
        elif keyboard == keyboard.SPACE:
            if not husky.is_sleeping:
                meal_selected = True
                clock.schedule_unique(meal_effect_in_game, 1)
    elif choice == 2:
        if keyboard == keyboard.RIGHT:
            cleaning_choice = 0
            print({cleaning_choice})
        elif keyboard == keyboard.LEFT:
            cleaning_choice = 1
            print({cleaning_choice})
        elif keyboard == keyboard.SPACE:
            if not husky.is_sleeping:
                cleaning_selected = True
                if cleaning_choice == 0 and husky.do_poop:
                    husky.do_poop = False
                    reset_activities()
                # if cleaning_choice == 0 and not husky.do_poop:
                #     reset_activities()
                if cleaning_choice == 1:
                    duck.x = - 800
                    # clock.schedule_interval(actors_animations_unique(cleaning_dog, cleaning_dog), 1/cleaning_dog.fps)
                    clock.schedule_interval(cleaning_dog_animation, 2 / cleaning_dog.fps)

                                            # ---------- Reset ----------

def reset_activities():
    global activity_selected, activity_choice, meal_choice, meal_selected, cleaning_choice, cleaning_selected, game_choice, game_selected, game_on, game_choice_selected, husky_number, hearts, win
    # reset variable de selection d'activités
    activity_choice = -1
    activity_selected = False
    # reset variables de selection de repas
    meal_choice = 0
    meal_selected = False
    # reset varaible de choix de nettoyage
    cleaning_choice = 0
    cleaning_selected = False
    duck.x = ACTOR_POSITION_X
    # reset des variables du mini jeu
    game_choice = -1
    husky_number = -2
    game_selected = False
    game_choice_selected = False
    game_on = False
    hearts = []
    win = 0
    # reset du background pour le passage jour/nuit
    background.image = "tamagochi_base_v2"

                                        # ---------- Effets dans le jeu ----------

def get_shutdown():
    global light_off, night
    if night == True:
        light_off = current_date
        husky._is_sleeping = True
    else:
        light_off = -1
    reset_activities()
    return light_off

def meal_effect_in_game():
    husky.meal_effect(meal_choice)
    reset_activities()

def game_1(husky_random_number):
    global game_on,game_choice, game_choice_selected, win, WIN_CONDITION

    if game_choice == husky_random_number and win <= WIN_CONDITION:
        win += 1
        new_heart = Actor("heart")
        new_heart.x = ACTOR_POSITION_X + 55* win
        new_heart.y = ACTOR_POSITION_Y
        hearts.append(new_heart)
        game_choice_selected = False
        game_choice = -1
        if win == WIN_CONDITION :
            husky.game_effect(husky_random_number)
            clock.schedule_unique(reset_activities, 2)
    else:
        game_choice_selected = False
        game_choice = -1


                                            # ---------- Animation ----------

def medication_animation():
    medication.index_animation +=1

    if medication.index_animation >=len(medications):
        medication.index_animation = 0
        clock.unschedule(medication_animation)
        husky.medication_effect()
        reset_activities()

    medication.image = medications[medication.index_animation]

def cleaning_dog_animation():
    cleaning_dog.index_animation +=1
    if cleaning_dog.index_animation >=len(cleaning_dog_table):
        cleaning_dog.index_animation = 0
        clock.unschedule(cleaning_dog_animation)
        husky.cleaning_effect()
        reset_activities()

    cleaning_dog.image = cleaning_dog_table[cleaning_dog.index_animation]

def pooping_animation():
    poop.index_animation +=1

    if poop.index_animation >=len(poops):
        poop.index_animation = 0

    poop.image = poops[poop.index_animation]


clock.schedule_interval(husky.dog_animation, 1/husky.fps)

pgzrun.go()

                                        # ---------- Essais mis de coter ----------

# #Fonction plus générique pour déclencher des evenements.
# def actors_animations_unique(actor_choice, actor_animation_table):
#     def anim_unique():
#         actor_choice.index_animation +=1
#         if actor_choice.index_animation >= len(actor_animation_table):
#             actor_choice.index_animation = 0
#             clock.unschedule(lambda a : actors_animations_unique(actor_choice, actor_animation_table))
#         actor_choice.image = actor_animation_table[actor_choice.index_animation]
#     return anim_unique
#
# def actor_animation(actor_choice, actor_animation_table):
#     def anim_repet():
#         actor_choice.index_animation += 1
#
#         if actor_choice.index_animation >= len(actor_animation_table):
#             actor_choice.index_animation = 0
#
#         actor_choice.image = actor_animation_table[actor_choice.index_animation]
#     return anim_repet