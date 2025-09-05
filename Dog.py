from pgzero.actor import Actor
from pgzero.clock import clock
from random import randint
from datetime import datetime


current_date = datetime.now()

class Dog(Actor):

    # ---------- Constructeur avec les propriétés ---------- #
    def __init__(self, img, **kwargs):
        self.hunger_level = 1000
        self.health_level = 1000
        self.sick_luck = 10
        self.dirty_level = 0
        self.happiness_level = 1000

        self.do_poop = False
        self._is_sick = False
        self. _is_sleeping = False
        self.in_game = False

        self.fps = 10

        self.index_animation = 0

        self.DOG_HAPPY_ANIM = ["husky_heureux_0001", "husky_heureux_0002"]
        self.DOG_SICK_ANIM = ["husky_sick_0001", "husky_sick_0002"]
        self.DOG_DIRTY_ANIM = ["husky_sale_0001", "husky_sale_0002"]
        self.DOG_WASHING_ANIM = ["husky_lavage_0001", "husky_lavage_0002"]
        self.DOG_SAD_ANIM = ["husky_triste_0001", "husky_triste_0002"]
        self.DOG_SLEEPING_ANIM = ["dodo_0001", "dodo_0002"]
        self.DOG_HUNGRY = ["husky_hungry_0001", "husky_hungry_0002"]
        self.DOG_GAME_L_R = ["husky_jeux_gauche_droite_0001", "husky_jeux_gauche_droite_0002"]

        self._animation = self.DOG_HAPPY_ANIM

        self.fps = 3

        super().__init__(img, **kwargs)

    # ---------- Propriétés en getter/setter ---------- #
    @property
    def is_hungry(self):
        if self.hunger_level < 500:
            return True
        return False
    
    @property
    def is_sad(self):
        if self.happiness_level < 500:
            return True
        return False
    
    @property
    def is_dirty(self):
        if self.dirty_level > 500:
            return True
        return False
    
    @property
    def is_sleeping(self):
        time_now = datetime.now()
        if (time_now.hour >= 22 or time_now.hour < 10) or self._is_sleeping:
            return True
        return False
    
    @property
    def is_sick(self):
        return self._is_sick
    @is_sick.setter
    def is_sick(self, value):
        if self.health_level < 100:
            self._is_sick = True
        else:
            self._is_sick = False
    
    @property
    def animation(self):
        return self._animation
    @animation.setter
    def animation(self, value):
        if self._animation != value:
            self.index_animation = 0
        self._animation = value

    # ---------- Méthodes ---------- #
    #----- Animation -----#
    def dog_animation(self):
        self.index_animation += 1

        if self.index_animation >= len(self.animation):
            self.index_animation = 0
        
        self.image = self.animation[self.index_animation]

    #----- Dessin du husky -----#
    def draw(self):
        if self.is_sick:
            self.animation = self.DOG_SICK_ANIM
        elif self.is_dirty:
            self.animation = self.DOG_DIRTY_ANIM
        elif self.in_game:
            self.animation = self.DOG_GAME_L_R
        elif self.is_hungry:
            self.animation = self.DOG_HUNGRY
        elif self.is_sad:
            self.animation = self.DOG_SAD_ANIM
        elif self.is_sleeping:
            self.animation = self.DOG_SLEEPING_ANIM
        else:
            self.animation = self.DOG_HAPPY_ANIM

        super().draw()

    #----- Ce qui se passe sur le husky a chaque fin du timer -----#
    def when_timer_is_over(self):
        if not self.is_sleeping or not self._is_sleeping:
            self.hunger_level -= 1
            self.health_level -= 1
            self.dirty_level += 1
            self.happiness_level -= 1
            self.random_sick()

        print("---------------------------------------")
        print(f"santé : {self.health_level}/100")
        print(f"malade : {self.is_sick} {self.sick_luck} ")
        print(f"triste : {self.is_sad} {self.happiness_level} ")
        print(f"sale : {self.is_dirty} {self.dirty_level}")
        print(f"faim : {self.hunger_level} {self.is_hungry}")
        print(f"dors : {self.is_sleeping} ")

    #----- De venir malade de manière random -----#
    def random_sick(self):
        random_sick_chance = randint(1, self.health_level)
        if not self._is_sick and random_sick_chance <= self.sick_luck:
            self._is_sick = True

    #----- Effets provoquer par la nourriture -----#
    def meal_effect(self, type_of_meal):
        #----- Si carotte -----#
        if type_of_meal == 0:
            self.hunger_level = 1000
            if self.health_level <= 900:
                self.health_level += 1000
            else:
                self.health_level = 1000
        #----- Si poulet -----#
        if type_of_meal == 1:
            self.hunger_level = 1000
            self.sick_luck +=1
        random_poop_time = randint(1,10)
        clock.schedule_unique(self.pooping, random_poop_time)

    #----- Faire caca -----#
    def pooping(self):
        self.do_poop = True
        self.dirty_level += 100

    #----- Effet du soin -----#
    def medication_effect(self):
        #----- Si le husky est malade -----#
        if self._is_sick:
            self.health_level = 1000
            self.is_sick = False
        #----- Si on le soigne et qu'il n'est pas malade -----#
        else:
            self.happiness_level -= 200

    #----- Effet du nettoyage -----#
    def cleaning_effect(self):
        #----- Si le husky est sale -----#
        if self.is_dirty:
            self.dirty_level = 0
        #----- Si le husky n'est pas sale -----#
        else:
            self.happiness_level -= 100
            self.dirty_level = 0

    #----- effet du sommeil -----#
    def sleeping_effect(self):
        from main import light_off
        if light_off != -1:
            delta_time = light_off - current_date
            delta_time_seconds = delta_time.total_seconds()/3600
            
            #----- Si la différence entre l'heure de l'endormissement et l'heure ou on eteint la lumière est min 8h -----#
            if delta_time_seconds > 7:
                self.health_level = 1000
                self.happiness_level = 1000
            #----- Si la différence entre l'heure de l'endormissement et l'heure ou on eteint la lumière est moins de 8h -----#
            elif delta_time_seconds < 8:
                self.health_level = 700
                self.happiness_level = 700
            #----- Si on eteint pas du tout la lumière -----#
            else:
                self.health_level = 500
                self.happiness_level = 500

    #----- effets du jeu -----#
    def game_effect(self, position):
        self.in_game = False
        self.happiness_level = 1000
        print(self.in_game)
