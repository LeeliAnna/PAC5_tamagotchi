import os
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
#----- Variable globale du jeu -----#
timer = TIME
activity_choice = -1
activity_selected = False
#----- Choix de nourriture -----#
meal_choice = 0
meal_selected = False
#----- Choix de nettoyage -----#
cleaning_choice = 0
cleaning_selected = False
#----- Gestion du la notion de jour/nuit -----#
current_date = datetime.now()
light_off = None
night = False
#----- mini-jeu -----#
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
medication.fps = 3
medication.x = ACTOR_POSITION_X
medication.y = ACTOR_POSITION_Y
                                                        # Caca
poops = ["caca_0001", "caca_0002"]
poop = Actor("caca_0001")
poop.index_animation = 0
poop.fps = 10
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

#----- Variable de controle de la victoire -----#
hearts = []
icon_heart = Actor("heart")
icon_heart.x = ACTOR_POSITION_X + 60
icon_heart.y = ACTOR_POSITION_Y

                                        # ---------- Draw et update ----------

def draw():
    global activity_choice,activity_selected,meal_choice,meal_selected

    screen.clear()
    background.draw()

    #----- Si mini-jeu est en cours :  -----#
    #----- Affichage du jeu et de points de victoire  -----#
    if game_on:
        icon_game.draw()
        if win > 0:
            for heart in hearts:
                heart.draw()
    #----- Si non affiche le menu de choix d'activités -----#
    else:
        for activity in activities_actors:
            activity.draw()

    #----- S'il n'y a aucune activité selectionnée affiche le Husky ou le caca si besoin -----#
    if not activity_selected:
        if husky.do_poop:
            poop.draw()
        else:
            husky.draw()
    #----- Si le choix est nourriture -----#
    elif activity_choice == 0 and activity_selected:
        #----- Affiche le choix de la nourriture -----#
        if meal_choice == 0:
            carrot.draw()
        if meal_choice == 1:
            nuggets.draw()
    #----- Si le choix est soins affiche le medicament -----#
    elif activity_choice == 1 and activity_selected:
        medication.draw()
    #----- Si le choix est nettoyage -----#
    elif activity_choice == 2 and activity_selected:
        #----- Affiche le choix du type de nettoyage -----#
        if cleaning_choice == 0:
            cleaning_poop.draw()
        if cleaning_choice == 1:
            duck.draw()
        if cleaning_choice == 1 and cleaning_selected:
            cleaning_dog.draw()
    else:
    #----- Si non affiche le husky -----#
        husky.draw()

def update(dt):
    global timer, night, game_on

    #----- Si la nuit est activée, bascule en mode nuit -----#
    if night:
        background.image = "tamagochi_base_v2_nuit"

    #----- Si le mini-jeu est actif, déclenche le et donne la po^ssibilité de choisir -----#
    if game_on:
        if game_choice == -1:
            icon_game.image = "sous_meu_jeu_vide"
        elif game_choice == 0:
            icon_game.image = "sous_meu_jeu_droite"
        elif game_choice == 1:
            icon_game.image = "sous_meu_jeu_gauche"
    #----- Si non affiche les autres activitées et affiche leur état -----#
    else:
        for index in range(len(activities_images)):
            if activity_choice == index:
                activities_actors[index].image = activities_images[index][1]
            else:
                activities_actors[index].image = activities_images[index][0]
    #----- Si le husky a fait caca anime le -----#
    if husky.do_poop:
        clock.schedule_interval(pooping_animation, 1 / poop.fps)
    #----- A chaque fois que le timer arrive à zero -----#
    if timer <= 0:
        #----- S'il ne fait pas nuit -----#
        if not night:
            #----- si le husky de dors pas et n'est pas en mini-jeu -----#
            if not husky.is_sleeping and not husky._is_sleeping and not husky.in_game:
                #----- Applique les effet du temps sur le husky -----#
                husky.when_timer_is_over()
        #----- resert le timer -----#
        timer = TIME
    timer -= dt


                        # ---------- Déclarations des touches pour contrôler le jeu ----------

def on_key_down(key):
    global activity_choice,activity_selected, night, timer, cleaning_selected, meal_selected, game_on, game_choice, game_choice_selected, husky_number

    #----- S'il y a une activité de selectionnée et qu'il ne fait pas nuit -----#
    if activity_selected and not night:
        #----- Si l'activité selectionnée est 0 ou 2 entre dans un sous-menu -----#
        if activity_choice == 0:
            second_menu(key, 0)
        if activity_choice == 2:
            second_menu(key, 2)
    #----- s'il fait nuit l'activité possible est 4 donc allumer la lumière -----#
    elif night:
        activity_choice = 4
        #-----  si c'est selectionner change le mode du jeu en jour, reveille le husky et reset les activitées -----#
        if key == key.SPACE:
            night = False
            husky._is_sleeping = False
            reset_activities()
        return
        #----- si non navige dans le menu principal -----#
    else:
        if key == key.RIGHT:
            activity_choice += 1
        elif key == key.LEFT:
            activity_choice -= 1
        elif key == key.SPACE:
            if activity_choice > -1:
                activity_selected = True

    #----- Permet de ne pas avoir d'activitée de selectionnée et de naviguer dane le menu principale -----#
    if activity_choice < -1:
        activity_choice = len(activities_actors) - 1
    elif activity_choice >= len(activities_actors):
        activity_choice = -1

    #----- Si le choix d'activité est soin. Affiche le medicament et anime le  -----#
    if activity_choice == 1 and activity_selected:
        # clock.schedule_interval(actors_animations_unique(medication,medications), 1/medication.fps)
        clock.schedule_interval(medication_animation, 1/medication.fps)
    #----- Si le choix d'activité est le mini-jeu lance le -----#
    if activity_choice == 3 and activity_selected:
        if not game_on or not game_choice_selected:
            #----- initialisation du random (gauche ou droite) -----#
            husky_number = randint(0, 1)
        game_on = True
        husky.in_game = True

        #----- Lie les touches clavier à un choix -----#
        if key == key.RIGHT:
            game_choice = 0
        elif key == key.LEFT:
            game_choice = 1
        elif key == key.SPACE:
            if game_choice != -1:
                game_choice_selected = True
        #----- Si le choix est selectionner déclanche la fonction mini-jeu -----#
        if game_choice_selected:
            game_1(husky_number)
    
    #----- Si le choix est lumière et qu'il ne fait pas nuit eteint -----#
    if activity_choice == 4 and activity_selected:
        if not night:
            night = True
            husky._is_sleeping = True
            get_shutdown()

def second_menu(keyboard, choice):
    global meal_choice,meal_selected, cleaning_choice, cleaning_selected

    #----- S'il fait nuit ou que le mini-jeu est en route stop -----#
    if night or game_on:
        return
    
    #----- Si le choix est nourriture, fais un choix de nourriture -----#
    if choice == 0:
        if keyboard == keyboard.LEFT:
            meal_choice = 0
        elif keyboard == keyboard.RIGHT:
            meal_choice = 1
        elif keyboard == keyboard.SPACE:
            if not husky.is_sleeping:
                meal_selected = True
                clock.schedule_unique(meal_effect_in_game, 1)
    #----- Si le choix est nettoyage, donne le choix du nettoyage et applique les effets -----#
    elif choice == 2:
        if keyboard == keyboard.LEFT:
            cleaning_choice = 0
            print({cleaning_choice})
        elif keyboard == keyboard.RIGHT:
            cleaning_choice = 1
            print({cleaning_choice})
        elif keyboard == keyboard.SPACE:
            if not husky.is_sleeping:
                cleaning_selected = True
                if cleaning_choice == 0 and husky.do_poop:
                    husky.do_poop = False
                    reset_activities()
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
    husky.in_game = False
    # reset du background pour le passage jour/nuit
    background.image = "tamagochi_base_v2"

                                        # ---------- Effets dans le jeu ----------

def get_shutdown():
    global light_off, night
    #----- Capture l'heure à laquel on eteint le lumière s'il fait nuit -----#
    if night == True:
        light_off = current_date
        husky._is_sleeping = True
    #----- Si non met l'heure à -1 et reset les activités -----#
    else:
        light_off = -1
    reset_activities()
    return light_off

#----- Fonction qui applique les effets de la nourriture -----#
def meal_effect_in_game():
    husky.meal_effect(meal_choice)
    reset_activities()

#----- Lancement du jeu -----#
def game_1(husky_random_number):
    global game_on,game_choice, game_choice_selected, win, WIN_CONDITION

    #----- Si le choix est egale au random  -----#
    if game_choice == husky_random_number:
        #----- Si on est compris entre les points et la condition de victoire applique les effets -----#
        if win < WIN_CONDITION:
            win += 1
            new_heart = Actor("heart")
            new_heart.x = ACTOR_POSITION_X + 55* win
            new_heart.y = ACTOR_POSITION_Y
            hearts.append(new_heart)
        game_choice_selected = False
        game_choice = -1
        #----- Si on est au bon nombre entre point et condition de victoire  applique les effects au husky et reset apres 2 secondes -----#
        if win >= WIN_CONDITION :
            husky.game_effect(husky_random_number)
            clock.schedule_unique(reset_activities, 2)
    else:
        #----- Si non reset le choix et continue le mini-jeu -----#
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