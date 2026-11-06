from uib_inf100_graphics.event_app import run_app
from uib_inf100_graphics.helpers import load_image, scaled_image
from PIL import Image
import random
import uib_inf100_music as music
import os
import sys
from pathlib import Path
import json


############
#            Dette er mitt første oredentlige spill. (snake telles liksom ikke siden det var en del håndholding)
#            Jeg har ikke brukt noen andre kilder enn det som er tilgjengelig på inf100 nettsiden, med unntak av for OS og JSON importering
#            Mye av triksene jeg har brukt her er basert på ting jeg gjorde i Snake
#            Alle assets er laget av meg.
#            så vil rette en stor takk ti pixilart.com, og beepbox.co som har vært mine verktøy for bilder og musikk respektivt
#            inspirasjonen til hovedkarakteren er snusmumrikken 
#            ellers er det bare ting som har kommet til meg (i mine mareritt mest sannsynlig)
#            Hadde jeg hatt mer tid, hadde jeg gjort mer :) men livet kom litt i veien så dette er alt jeg har rekket å gjøre
#            
#               og takk til Are 
#                   og en kompis av meg, Truls, som hjalp med innspill for visuell tydelighet på noen angrep
#
#            Det er et vanskelig spill, så ikke bli lei deg hvis du er dårlig.
#            skill issue heter det :P
#     ###########################       
#  
# OS check og JSON check stjal jeg fra Snaken min
# hvor jeg stjal det fra disse kildene:
##########kilder:
#https://docs.python.org/3/library/sys.html#sys.platform (docs for å finne ut hvordan jeg kan finne ut av OS fordi noen folk har mac)
#https://stackoverflow.com/questions/32991069/python-checking-for-json-files-and-creating-one-if-needed (Stackoverflow for å finne ut av hvordan sjekke om en JSON fil finnes)
#funksjon det gjelder ( check_json(app)) ( er ikke en komplett rip men er ganske likt kopiert)
#
#
#
############################
###to do
##################################
# forskjell på hit og i frames?
# boss 3
#  attack, look, og bakgrunn
# final boss
# attacks, bakgrunn
# settings:
#    rebinds
#    sounds
#    
#  lage lydeffekter?
# 



def app_started(app):
    
    #timer 
    app.timer_delay = 50

    #states
    app.game_state = "Menu"
    app.boss_fight = ""
    app.boss_stage = ""
    app.debug = True

    #player
    app.player_pos_x = 300 - 48
    app.player_pos_y = 400
    app.player_pos_hix = 300
    app.player_pos_hiy = 448
    app.player_state = ""
    app.player_facing = 1
    app.player_lives = 3
    app.show_basic_attack = 0
    app.basic_attack_cooldown = 0
    app.player_color = "red"
    app.player_sprint = 0
    app.listening_to_input = 0
    app.dash_timer = 0
    app.dodge_timer = 0
    app.player_health = 10
    app.i_frames = 0
    app.attack_stops_movement = 0
    app.player_money = 0
    app.animation_counter = 0
    app.do_animation = 0
    app.attack_hitbox = []
    app.idle_counter = 0
    app.difficulty = "Baby"
    app.beaten_baby = False
    app.beaten_easy = False
    app.beaten_hard = False
    app.beaten_b1 = False
    app.beaten_b2 = False
    app.beaten_b3 = False
    app.beaten_b4 = False
    
    #enemy
    app.enemy_pos_x = 100
    app.enemy_pos_hix = 200
    app.enemy_pos_y = 450
    app.enemy_pos_hiy = 700
    app.enemy_hit = 0
    app.enemy_movement_CD = 10
    app.enemy_spawn = 0
    app.enemy_attack_x = 0
    app.enemy_attack_y = 0
    app.show_boss_attack = 0
    app.enemy_cd = 0
    app.boss_stagger = 0
    app.enemy_do_animation = 0
    app.enemy_projectile_cd = 20
    app.projectile_1 = [[0 , 0 , 0 ,0],
                        [0 , 0 , 0 , 0]
    ]
    app.show_projectile_1 = False
    app.show_projectile_2 = False
    app.projectile_speed = 0
    #input delay and others
    app.input_delay = 0
    app.input_delay_menu = 0
    app.menu_selector = 0
    app.menu_selector_x = 0
    app.play_from_map = False
    ##import profile
    #create bindings
    create_bindings(app)
    #image_handler
    image_handler(app)
    sound_handler(app)
    
    #buttons
    main_menu_buttons(app)
    map_buttons(app)
    settings_buttons(app)
    rebind_buttons(app)
    
    #colors
    app.background_color = "ivory"
    app.button_color = "bisque"
    app.boss_color = "green"
    app.main_menu_song.play()
    app.enter_bind = "Enter"

    app.new_bound = 0
    app.invert_check = 0

    if check_json(app, "Story_of_Alfred/profile.json"):
        pass
    else:
        create_json(app)

    import_profile(app)

    #system greier
    app.os_windows = True
    clean_fixes(app)


def clean_fixes(app):
    #profile? kanskje
    get_system(app)
    if app.os_windows == False:
        app.enter_bind = "Return"

def get_system(app):
    temp = sys.platform
    if temp == "darwin":
        app.os_windows = False 

def check_json(app, file_name):
    return os.path.exists(file_name)

def create_bindings(app):
    app.bind_left = "a"
    app.bind_right = "d"
    app.bind_up = "w"
    app.bind_down =  "s"
    app.bind_dodge = "g"
    app.bind_dash = "h"
    app.bind_attack = "j"

def image_handler(app):
    create_player_animations(app)
    create_backgrounds(app)
    create_boss_one_animations(app)
    create_boss_two_animations(app)
    create_boss_3_animations(app)
    create_final_boss_animations(app)
    create_hud_images(app)

def sound_handler(app):
    #menyer og sånt
    app.main_menu_song = music.load_looping_sound("Story_of_Alfred/Music_assets/Main_theme.mp3")
    app.map_song = music.load_looping_sound("Story_of_Alfred/Music_assets/map_song.mp3")
    app.death_song = music.load_looping_sound("Story_of_Alfred/Music_assets/death_song.mp3")

    #bosser og sånt
    app.music_boss_one = music.load_looping_sound("Story_of_Alfred/Music_assets/Boss_one_song.mp3")
    app.music_boss_two = music.load_looping_sound("Story_of_Alfred/Music_assets/boss_2.mp3")     
    app.music_boss_three = music.load_looping_sound("Story_of_Alfred/Music_assets/boss_3.mp3")
    app.final_boss_song = music.load_looping_sound("Story_of_Alfred/Music_assets/Final_boss.mp3")
    


def create_json(app):
    profile = [app.beaten_baby, app.beaten_easy, app.beaten_hard, app.beaten_b1, app.beaten_b2, app.beaten_b3, app.beaten_b4,
                        app.bind_up, app.bind_down, app.bind_left, app.bind_right, app.bind_attack, app.bind_dodge, app.bind_dash]
    content =json.dumps(profile)
    Path("Story_of_Alfred/profile.json").write_text(content, encoding="utf-8")

def import_profile(app):
    content = Path("Story_of_Alfred/profile.json").read_text(encoding="utf-8")
    profile = json.loads(content)
    app.beaten_baby = profile[0]
    app.beaten_easy = profile[1]
    app.beaten_hard = profile[2]
    app.beaten_b1 = profile[3]
    app.beaten_b2 = profile[4]
    app.beaten_b3 = profile[5]
    app.beaten_b4 = profile[6]
    app.bind_up = profile[7]
    app.bind_down = profile[8]
    app.bind_left = profile[9]
    app.bind_right = profile[10]
    app.bind_attack = profile[11]
    app.bind_dodge = profile[12]
    app.bind_dash = profile[13]

def create_player_animations(app):

    #### idle animation
    image = load_image("Story_of_Alfred/Sprite_assets/player/idle1.png")
    image1 = scaled_image(image, 2)
    image = load_image("Story_of_Alfred/Sprite_assets/player/idle2.png")
    image2 = scaled_image(image, 2)
    app.player_idle_animation = [image1 , image2, image1, image2]
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    app.player_idle_animation1 = [rimage1, rimage2 , rimage1, rimage2]
    #attack animation
    image = load_image("Story_of_Alfred/Sprite_assets/player/player_attack1.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/player/player_attack2.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/player/player_attack3.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/player/player_attack4.png")
    image4 = scaled_image(image , 2)
    app.player_attack_animation = [image4 , image3, image2, image1]
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
    app.player_attack_animation1 = [rimage4, rimage3, rimage2, rimage1]

    ### walking animation
    image = load_image("Story_of_Alfred/Sprite_assets/player/walking1.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/player/walking2.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/player/walking3.png")
    image3 = scaled_image(image , 2)

    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    
    app.player_walking_animation = [image1 , image2 , image3, image2]
    app.player_walking_animation1 = [rimage1, rimage2, rimage3, rimage2]
    image = load_image("Story_of_Alfred/Sprite_assets/player/iframe.png")
    image1 = scaled_image(image , 2)
    image2 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    app.player_iframes = image1
    app.player_iframesr = image2

    image = load_image("Story_of_Alfred/Sprite_assets/player/player_damaged.png")
    image1 = scaled_image(image , 2)
    image2 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    app.player_damaged_image = image1
    app.player_damaged_imager = image2
def create_boss_one_animations(app):
    image = load_image("Story_of_Alfred/Sprite_assets/Boss_1.png")
    image1 = scaled_image(image, 2)
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss_one_idle = [image1]
    app.boss_one_idle1 = [rimage1]

    image = load_image("Story_of_Alfred/Sprite_assets/Boss_1_charge.png")
    image1 = scaled_image(image , 2)
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss_one_charge = [image1]
    app.boss_one_charge1 = [rimage1]


    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/2.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/3.png")
    image4 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/4.png")
    app.boss1_attack1 = [image1, image2, image3, image4]

    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss1_attack1f = [rimage1, rimage2, rimage3, rimage4]


    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/5.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/6.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/7.png")
    image4 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a1/8.png")
    image5 = scaled_image(image , 2)
    app.boss1_attack2 = [image1, image2, image3, image4,image5]
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
    rimage5 = image5.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss1_attack2f = [rimage1, rimage2, rimage3, rimage4, rimage5]
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a3/1.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a3/2.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a3/3.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b1_a3/4.png")
    image4 = scaled_image(image , 2)
    app.boss1_attack3 = [image1, image2, image3, image4]
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss1_attack3f = [rimage1, rimage2, rimage3, rimage4]
    image = load_image("Story_of_Alfred/Sprite_assets/b1_i.png")
    image1 = scaled_image(image , 2)
    app.boss1_hit = image1

def create_boss_two_animations(app):
    
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/2.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/3.png")
    image4 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/4.png")
    image5 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/5.png")
    image6 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_i/6.png")
    image7 = scaled_image(image , 2)
    app.boss_two_idle = [image1, image2,image3, image4, image5, image6, image7]



    image = load_image("Story_of_Alfred/Sprite_assets/b2_a1_0.png")
    image1 = scaled_image(image, 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_a1_1.png")
    image2 = scaled_image(image , 2)
    app.b2_a1_i = [image1, image2]
    image = load_image("Story_of_Alfred/Sprite_assets/b2_p1.png")
    image1 = scaled_image( image , 2)
    app.b2_p1_i = image1
    image = load_image("Story_of_Alfred/Sprite_assets/b2_a3_0.png")
    image1 = scaled_image(image, 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b2_a3_1.png")
    image2 = scaled_image(image , 2)
    app.b2_a3_i = [image1, image2]

def create_boss_3_animations(app):
    image = load_image("Story_of_Alfred/Sprite_assets/b3.png")
    image1 = scaled_image(image , 2)
    app.b3 = image1
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a1.png")
    image1 = scaled_image(image , 2)
    app.b3_a1 = image1
    image = load_image("Story_of_Alfred/Sprite_assets/b3_i.png")
    image1 = scaled_image(image , 2)
    app.b3_hit = image1
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a2/b3_a2_0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a2/b3_a2_1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a2/b3_a2_2.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a2/b3_a2_3.png")
    image4 = scaled_image(image , 2)
    app.b3_a2 = [image1, image2, image3, image4]

    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)

    app.b3_a2f = [rimage1, rimage2, rimage3, rimage4]
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a3_0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b3_a3_1.png")
    image2 = scaled_image(image , 2)
    app.b3_a3 = [image1, image2]

def create_final_boss_animations(app):
    image = load_image("Story_of_Alfred/Sprite_assets/b4_i/0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_i/1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_i/2.png")
    image3 = scaled_image(image , 2)
    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)

    app.b4_i = [image1, image2, image3]
    app.b4_i_f = [rimage1, rimage2, rimage3]

    image = load_image("Story_of_Alfred/Sprite_assets/b4_w/0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_w/1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_w/2.png")
    image3 = scaled_image(image , 2)

    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)

    app.b4_w = [image1, image2, image3]
    app.b4_w_f = [rimage1, rimage2, rimage3]
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a1/0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a1/1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a1/2.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a1/3.png")
    image4 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a1/4.png")
    image5 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a1/5.png")
    image6 = scaled_image(image , 2)

    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
    rimage5 = image5.transpose(Image.FLIP_LEFT_RIGHT)
    rimage6 = image6.transpose(Image.FLIP_LEFT_RIGHT)

    app.b4_a1 = [image1, image2, image3, image4, image5, image6]
    app.b4_a1_f =[rimage1, rimage2, rimage3, rimage4, rimage5, rimage6]
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a2/0.png")
    image1 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a2/1.png")
    image2 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a2/2.png")
    image3 = scaled_image(image , 2)
    image = load_image("Story_of_Alfred/Sprite_assets/b4_a2/3.png")
    image4 = scaled_image(image , 2)

    rimage1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
    rimage2 = image2.transpose(Image.FLIP_LEFT_RIGHT)
    rimage3 = image3.transpose(Image.FLIP_LEFT_RIGHT)
    rimage4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
    app.b4_a2 = [image1, image2, image3, image4]
    app.b4_a2_f = [rimage1, rimage2, rimage3, rimage4]
def create_backgrounds(app):
    image = load_image("Story_of_Alfred/Sprite_assets/Background.png")
    #image = scaled_image(image)
    app.main_menu_bg = image
    image = load_image("Story_of_Alfred/Sprite_assets/backgrounds/bg_b1.png")
    image1 = scaled_image(image , 2)
    app.boss_one_bg = image1
    image = load_image("Story_of_Alfred/Sprite_assets/backgrounds/bg_b2.png")
    image1 = scaled_image(image, 2)
    app.boss_two_bg = image1
    image = load_image("Story_of_Alfred/Sprite_assets/backgrounds/bg_b3.png")
    image1 = scaled_image(image , 2)
    app.boss_three_bg = image1
    image = load_image("Story_of_Alfred/Sprite_assets/backgrounds/bg_b4.png")
    image1 = scaled_image(image , 2)
    app.boss_final_bg = image1

def create_hud_images(app):
    image = load_image("Story_of_Alfred/Sprite_assets/HUD/Frame_1.png")
    image1 = scaled_image(image , 2)
    app.healthbar = image1
    image = load_image("Story_of_Alfred/Sprite_assets/HUD/icon.png")
    image1 = scaled_image(image , 4)
    app.player_icon = image1

def timer_fired(app):

    if app.game_state == "Running":

        player_movement(app)
        timer_player_char_one(app)
        if app.boss_fight == "One":
            boss_one_timer(app)
        elif app.boss_fight == "Two":
            boss_two_timer(app)
        elif app.boss_fight == "Three":
            boss_three_timer(app)
        elif app.boss_fight == "Final":
            boss_final_timer(app)
    elif app.game_state == "Binding_key":
        if app.bind_timer > 0:
            app.bind_timer -= 1
        if app.new_bound != 0:
            rebind_keys(app)
        if app.bind_timer == 0:
            app.game_state == "Rebind"
    


def input_delay(app):
    if app.input_delay > 0:
        app.input_delay -= 1
    if app.input_delay_menu > 0:
        app.input_delay_menu -= 1

def timer_player_char_one(app):
    player_animation_timer(app)
    if app.player_took_damage > 0:
        app.player_took_damage -= 1
    if app.i_frames > 0:
        app.player_color = "pink"
    else:
        app.player_color = "red"
    if app.basic_attack_cooldown > 0:
        app.basic_attack_cooldown -= 1
    if app.dodge_timer > 0:
        app.dodge_timer -= 1
    if app.dash_timer > 0:
        app.dash_timer -= 1
    if app.attack_stops_movement > 0:
        app.attack_stops_movement -= 1
    if app.i_frames > 0:
        app.i_frames -= 1
    if app.show_basic_attack > 0:
        app.show_basic_attack -= 1
    if app.idle_counter > 0:
        app.idle_counter -= 1
    if app.idle_counter == 0 and app.player_moving == False:
        app.player_state = "Idle"
    if app.player_health <= 0:
        kill_player(app)
    input_delay(app)
    

### animation timere
def player_animation_timer(app):
    app.do_animation += 1

    if app.do_animation > 10:
        if app.animation_counter < 3:
            app.animation_counter += 1
            app.do_animation = 0
        elif app.animation_counter == 3:
            app.animation_counter = 0
            app.do_animation = 0


def boss_animation_timer(app):
    app.enemy_do_animation += 1
    if app.enemy_do_animation > 10:
        if app.enemy_animation_counter > 4:
            app.enemy_animation_counter += 1
            app.enemy_do_animation = 0
        else:
            app.enemy_animation_counter = 0
            app.enemy_do_animation = 0



### timere kan importeres fra et annet dokument??
##### boss timere
def boss_one_timer(app):
    #finn ut retningen til boss
    if app.enemy_pos_x > app.player_pos_x and app.boss_stagger == 0:
        app.enemy_direction = 1
    if app.enemy_pos_x < app.player_pos_x and app.boss_stagger == 0:
        app.enemy_direction = -1
    #regn ut hva boss skal gjøre
    if app.enemy_action == "Idle":
        boss_one_action_calc(app)

    #kan boss gjøre noe?
    #hver action gir en cd
    #burde ryddes opp?
    if app.enemy_cd == 0:
        if app.enemy_action == "Walk_West":
            app.enemy_pos_x -= 20
            app.enemy_pos_hix -= 20
            app.enemy_cd += 10
            app.enemy_action = "Idle"
        elif app.enemy_action == "Walk_East":
            app.enemy_pos_x += 20
            app.enemy_pos_hix += 20
            app.enemy_cd += 10
            app.enemy_action = "Idle"
        elif app.enemy_action == "Attack_1":
            if app.boss_stagger == 0:
                app.b1_a1_f = 0
                app.animate_b1_a1 = True
            app.boss_stagger += 1
            if app.boss_stagger % 4 == 0:
                app.b1_a1_f += 1
            if app.boss_stagger > 10:
                boss_one_attack_1(app)
                app.enemy_cd += 8
                app.enemy_action = "Attack_2"
                app.boss_color = "green"
                app.boss_stagger = 0
                app.b1_a1_f = 0

        elif app.enemy_action == "Attack_2":                
            app.boss_stagger += 1
            if app.boss_stagger % 2 == 0:
                app.b1_a1_f += 1
            if app.boss_stagger > 4:
                boss_one_attack_2(app)
                app.enemy_cd += 20
                app.enemy_action = "Idle"
                app.boss_color = "green"
                app.boss_stagger = 0
                app.animate_b1_a1 = False

        elif app.enemy_action == "Attack_3":
            if app.boss_stagger == 0:
                app.b1_a1_f = 0
                app.animate_b1_a1 = True
            app.boss_stagger += 1
            if app.boss_stagger % 2 == 0:
                app.b1_a1_f += 1
            if app.boss_stagger > 4:
                boss_one_attack_3(app)
                app.enemy_cd +=10
                app.enemy_action = "Idle"
                app.boss_color = "green"
                app.boss_stagger = 0
                app.animate_b1_a1 = False

    #ta ned cd et punkt
    if app.enemy_cd > 0:
        app.enemy_cd -= 1
    if app.show_boss_attack > 0:
        app.show_boss_attack -= 1
    if app.enemy_i_frames > 0:
        app.enemy_i_frames -= 1
        

def boss_two_timer(app):
    
    if app.boss_stage == "One":

        if app.enemy_action == "Idle":
            boss_two_action_calc(app)
        if app.enemy_cd == 0:
           
            if app.enemy_action == "Attack_1":
                app.boss_stagger += 1
                if app.boss_stagger == 1:
                    boss_two_show_attack_1(app)
                    app.stop_showing_b2_a1 = 30
                if app.boss_stagger > 12:
                    boss_two_attack_1(app)
                    app.enemy_cd += 20
                    app.enemy_action = "Idle"
                    
            if app.enemy_action == "Attack_2":
                boss_two_attack_2(app)
                app.enemy_cd += 20
                app.enemy_action = "Idle"
                app.enemy_projectile_cd += 50
            if app.enemy_action == "Attack_3":

                app.boss_stagger += 1
                if app.boss_stagger == 1:
                    boss_two_show_attack_3(app)
                    app.stop_showing_b2_a3 = 20
                if app.boss_stagger > 8:
                    boss_two_attack_3(app)
                    app.enemy_cd += 12
                    app.enemy_action = "Idle"


    if app.enemy_cd > 0:
        app.enemy_cd -= 1
    if app.stop_showing_b2_a1 > 0:
        app.stop_showing_b2_a1 -= 1
    if app.stop_showing_b2_a1 == 0:
        app.show_attack_1 = False 
    if app.stop_showing_b2_a3 > 0:
        app.stop_showing_b2_a3 -= 1
    if app.stop_showing_b2_a3 == 0:
        app.show_attack_3 = False
    if app.enemy_tp_cd > 0:
        app.enemy_tp_cd -= 1
    if app.show_boss_attack > 0:
        app.show_boss_attack -= 1
    if app.enemy_projectile_cd > 0:
        app.enemy_projectile_cd -= 1
    app.animation_tick += 1
    if app.animation_tick % 7 == 0:
        if app.b2_animation <= 6:
            app.b2_animation_f += 1
            app.b2_animation += 1
        if app.b2_animation >= 7:
            app.b2_animation_f = 0
            app.b2_animation = 0
    
    projectile_manager_1(app)
    if app.boss_two_teleport == True:
        if app.tp_counter > 0:
            app.tp_counter -= 1
        if app.tp_counter == 0:
            random_factor = (10 * random.randrange(11))
            app.boss_two_teleport = False
            if app.enemy_pos_x - 1700 + random_factor < 50:
                app.enemy_pos_x = 720
                app.enemy_pos_hix = 736
            else:
                app.enemy_pos_x -= 1600 + random_factor
                app.enemy_pos_hix -= 1600 + random_factor
                
                
def boss_three_timer(app):
    if app.enemy_pos_x > app.player_pos_x and app.boss_stagger == 0:
        app.enemy_direction = 1
    if app.enemy_pos_x < app.player_pos_x and app.boss_stagger == 0:
        app.enemy_direction = -1
    if app.enemy_action == "Idle":
        boss_three_action_calc(app)
    if app.enemy_cd == 0:

        if app.enemy_action == "Attack_1":
            boss_three_attack_1(app)
            app.enemy_action = "Idle"
            app.enemy_cd = 20
        if app.enemy_action == "Attack_2":
            if app.boss_stagger == 0:
                boss_three_show_attack_2(app)
            app.boss_stagger += 1

            if app.boss_stagger % 2 == 0:
                app.b3_a2_f += 1
            if app.boss_stagger > 7:
                boss_three_attack_2(app)
                app.enemy_action = "Idle"
                app.enemy_cd = 10
                app.b3_a2_f = 0
                app.boss_stagger = 0
        if app.enemy_action == "Attack_3":
            if app.boss_stagger == 0:
                boss_three_show_attack_3(app)
            app.boss_stagger += 1
            if app.boss_stagger >7:
                boss_three_attack_3(app)
                app.enemy_action = "Idle"
                app.enemy_cd = 15
                
            
    projectile_manager_2(app)
    if app.enemy_cd > 0:
        app.enemy_cd -= 1
    if app.stop_showing_b3_a3 > 0:
        app.stop_showing_b3_a3 -= 1
    if app.stop_showing_b3_a3 == 1:
        app.show_b3_a3 = False
    if app.enemy_i_frames > 0:
        app.enemy_i_frames -= 1


def boss_final_timer(app):
    if app.enemy_health < 300:
        app.boss_stage = "Two"
    if app.enemy_pos_x > app.player_pos_x and app.boss_stagger == 0:
        app.enemy_direction = 1
    if app.enemy_pos_x < app.player_pos_x and app.boss_stagger == 0:
        app.enemy_direction = -1    
    if app.boss_stage == "One":
        if app.enemy_cd == 0 and app.enemy_action == "Idle":
            final_boss_action_calc_0(app)
        if app.enemy_action == "Walk_West":
            app.enemy_pos_x -= 10
            app.enemy_pos_hix -= 10
            
            app.enemy_action = "Idle"
        elif app.enemy_action == "Walk_East":
            app.enemy_pos_x += 10
            app.enemy_pos_hix += 10
            
            app.enemy_action = "Idle"
        elif app.enemy_action == "Attack_1":
            app.boss_stagger += 1
            if app.boss_stagger % 3 == 0:
                app.b4_a1_frame += 1
            if app.boss_stagger == 3:
                b4_a1_1(app)
                app.show_boss_attack = 10
            elif app.boss_stagger == 10:
                b4_a1_2(app)
                app.enemy_action = "Idle"
                app.boss_cd = 30
                app.show_boss_attack = 10
                app.b4_a1_frame = 0
        elif app.enemy_action == "Attack_2":
            app.boss_stagger += 1
            if app.boss_stagger % 4 == 0:
                app.b4_a2_frame += 1
            if app.boss_stagger == 13:
                b4_a2(app)
                app.enemy_action = "Idle"
                app.boss_cd = 20
                app.show_boss_attack = 10
                app.b4_a2_frame = 0   
    elif app.boss_stage == "Two":
        if app.enemy_cd == 0:
            final_boss_action_calc_1


    app.animation_tick += 1
    if app.enemy_i_frames > 0:
        app.enemy_i_frames -= 1
    if app.enemy_i_frames > 0:
        app.enemy_i_frames -= 1
    if app.enemy_cd > 0:
        app.enemy_cd -= 1
    if app.show_boss_attack > 0:
        app.show_boss_attack -= 1
    if app.animation_tick % 7 == 0:
        if app.b4_animation_f < 2:
            app.b4_animation_f += 1
        if app.b4_animation_f == 2:
            app.b4_animation_f = 0



#######################################
####action calc
#########################################
def boss_one_action_calc(app):
    if app.enemy_pos_x >= app.player_pos_x + 100:
            app.enemy_action = "Walk_West"
    elif app.enemy_pos_x <= app.player_pos_x - 100:
            app.enemy_action = "Walk_East"
    elif random.randrange(5) == 3:
        app.enemy_action = "Attack_3"
    else:
        app.enemy_action = "Attack_1"

def boss_two_action_calc(app):
    #teleport kanskje
    #range attack (untill hit)
    #summon on top of player
    #two phases
    attack_prompt = random.randrange(2)
    #move if need to move


    #or else do an attack
    if attack_prompt == 0 and app.enemy_action == "Idle":
            app.enemy_action = "Attack_1"
            
    elif attack_prompt == 1 and app.enemy_projectile_cd == 0 and app.enemy_action == "Idle" and app.b2_p_cd == False:
            app.enemy_action = "Attack_2"

    if attack_prompt == 1 and app.enemy_action == "Idle":
            app.enemy_action = "Attack_3"



def boss_three_action_calc(app):

    
    if app.player_pos_hix > app.enemy_pos_x - 150 and app.player_pos_x < app.enemy_pos_hix + 120:
        app.enemy_action = "Attack_2"

    elif app.show_projectile_3 == False:
        app.enemy_action = "Attack_1"
    else:
        app.enemy_action = "Attack_3"
def final_boss_action_calc_1(app):
    pass

def final_boss_action_calc_0(app):
    r = random.randrange(11)
    if app.enemy_pos_x >= app.player_pos_x + 45:
            app.enemy_action = "Walk_West"
    elif app.enemy_pos_x <= app.player_pos_x - 45:
            app.enemy_action = "Walk_East"   
    elif r % 2== 0:
        app.enemy_action = "Attack_1"
    else:
        app.enemy_action = "Attack_2"
#### attacks


############################
############ Boss one ################
#################################
def boss_one_attack_1(app):

    if app.enemy_direction == 1:
        app.enemy_attack_x1 = app.enemy_pos_x -10 * app.enemy_direction
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_x - 60 * app.enemy_direction
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    elif app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_hix -10 * app.enemy_direction
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_hix - 60 * app.enemy_direction
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
            app.player_health -= 10
            app.i_frames += 4
    app.show_boss_attack += 10
    app.boss_stagger = 0

def boss_one_attack_2(app):
    #disse variablene trenger ikke være app hvis jeg ikke skal vise angrepene
    if app.enemy_direction == 1:
        app.enemy_attack_x1 = app.enemy_pos_x -20 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_x + 10 
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    elif app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_hix -20 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_hix + 10 
        app.enemy_attack_y2 = app.enemy_pos_y + 10

    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 5
        app.i_frames += 4
    app.show_boss_attack += 10
    app.boss_stagger = 0

def boss_one_attack_3(app):
    if app.enemy_direction == 1:

        app.enemy_attack_x1 = app.enemy_pos_x - 20 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_x - 50 
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    elif app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_hix + 20 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_hix + 50 
        app.enemy_attack_y2 = app.enemy_pos_y + 10

    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 5
        app.i_frames += 4
    app.show_boss_attack += 10
    app.boss_stagger = 0

############################
############ Boss two ################
#################################
def boss_two_attack_1(app):
    app.b2_a1_c = 1
    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 12
        app.i_frames += 4
    app.show_boss_attack += 10
    app.boss_stagger = 0

def boss_two_show_attack_1(app):
    random_factor = random.randrange(3)
    app.enemy_attack_x1 = app.player_pos_x - 20 + (10 * random_factor)
    app.enemy_attack_y1 = app.player_pos_hiy
    app.enemy_attack_x2 = app.player_pos_hix + 20 + (10 * random_factor)
    app.enemy_attack_y2 = app.player_pos_hiy - 20
    app.show_attack_1 = True
    app.b2_a1_c = 0

    
def boss_two_attack_2(app):
    area = app.player_pos_x + 12, app.player_pos_hix -12
    app.b2_p_cd = False
    create_projectile_1(app, area)

def boss_two_attack_3(app):
    app.b2_a3_c = 1
    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 8
        app.i_frames += 4
    app.show_boss_attack += 10
    app.boss_stagger = 0

def boss_two_show_attack_3(app):
    random_factor = random.randrange(-10, 10)
    app.enemy_attack_x1 = app.player_pos_x - 20 + (10 * random_factor)
    app.enemy_attack_y1 = app.player_pos_hiy
    app.enemy_attack_x2 = app.player_pos_hix + 20 + (10 * random_factor)
    app.enemy_attack_y2 = app.player_pos_hiy - 20
    app.show_attack_3 = True
    app.b2_a3_c = 0


def teleport_boss_two(app):
    app.tp_counter = 40
    app.boss_two_teleport = True
    app.enemy_pos_x += 1500
    app.enemy_pos_hix += 1500
###############################
##########BOSS THREE
#########################

def boss_three_attack_1(app):
    create_projectile_2(app)

def boss_three_show_attack_2(app):

    app.show_b3_a2 = True
    app.b3_a2_f = 0

def boss_three_attack_2(app):
    if app.enemy_direction == 1:
        app.enemy_attack_x1 = app.enemy_pos_x - 20
        app.enemy_attack_y1 = app.enemy_pos_y + 20
        app.enemy_attack_x2 = app.enemy_pos_x - 88
        app.enemy_attack_y2 = app.enemy_pos_y +40
    if app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_x + 20
        app.enemy_attack_y1 = app.enemy_pos_y + 20
        app.enemy_attack_x2 = app.enemy_pos_x + 88
        app.enemy_attack_y2 = app.enemy_pos_y +40

    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2   
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 8
        app.i_frames += 4
        app.player_pos_x -= 300
        app.player_pos_hix -= 300

    app.show_boss_attack += 20
    app.boss_stagger = 0

def boss_three_show_attack_3(app):
    app.enemy_attack_x1 = app.player_pos_x - 24
    app.enemy_attack_y1 = app.enemy_pos_y + 20
    app.enemy_attack_x2 = app.player_pos_hix + 24
    app.enemy_attack_y2 = app.enemy_pos_y +40  

    app.show_b3_a3 = True
    app.b3_a3_f = 0
    app.stop_showing_b3_a3 = 20

def boss_three_attack_3(app):
    app.b3_a3_f = 1
    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 12
        app.i_frames += 4

    app.boss_stagger = 0

####projectile manager
def create_projectile_1(app, area):
    x1 = area[0]
    x2 = area[1]

    y1= 100
    y2= 124

    app.projectile_1 = [[x1, y1 , x2 ,y2],
                        [x1 + 60, y1-300, x2+ 60, y2-300]
                ]
    app.projectile_speed = 10
    app.show_projectile_1 = True
    app.show_projectile_2 = True

def create_projectile_2(app):
    x = app.enemy_pos_x
    y = app.enemy_pos_y + 10
    x2 = x + 20
    y2 = y + 20
    app.projectile_2 = [x, y, x2 , y2]

    app.projectile_speed = 20
    app.show_projectile_3 = True

def projectile_manager_1(app):
    if app.projectile_1[0][1] < 700:
        app.projectile_1[0][1] += app.projectile_speed
        app.projectile_1[0][3] += app.projectile_speed
    else:
        app.show_projectile_1 = False
        

    if app.projectile_1[1][1] < 700:
        app.projectile_1[1][1] += app.projectile_speed
        app.projectile_1[1][3] += app.projectile_speed
    else:
        app.show_projectile_2 = False
        app.b2_p_cd = False
    if app.projectile_1[0][1] <= app.player_pos_hiy and app.projectile_1[0][1] >= app.player_pos_y:
        if collision_detection_enemy_attack(app, app.projectile_1[0]) == True and app.i_frames == 0:
            app.player_health -= 5
            app.i_frames += 5


    if app.projectile_1[1][1] <= app.player_pos_hiy and app.projectile_1[1][1] >= app.player_pos_y:
        if collision_detection_enemy_attack(app, app.projectile_1[1]) == True and app.i_frames == 0:
            app.player_health -= 5
            app.i_frames += 5

def projectile_manager_2(app):
    if app.projectile_2[0] > -100:
        app.projectile_2[0] -= app.projectile_speed
        app.projectile_2[2] -= app.projectile_speed
    else:
        app.show_projectile_3 = False

    if app.projectile_2[0] <= app.player_pos_hix and app.projectile_2[0] >= app.player_pos_x:
        if collision_detection_enemy_attack(app, app.projectile_2) == True and app.i_frames == 0:
            app.player_invert_controll = 10
            invert_controll(app)
            app.player_health -= 5
            app.i_frames += 5

###########################
#################final boss###################
######################


def b4_a1_1(app):
    if app.enemy_direction == 1:

        app.enemy_attack_x1 = app.enemy_pos_x - 10
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_x - 20 
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    elif app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_hix + 10 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_hix + 20 
        app.enemy_attack_y2 = app.enemy_pos_y + 10   

def b4_a1_2(app):
    if app.enemy_direction == 1:

        app.enemy_attack_x1 = app.enemy_pos_x - 15 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_x - 25 
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    elif app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_hix + 15 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_hix + 25 
        app.enemy_attack_y2 = app.enemy_pos_y + 10


    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 5
        app.i_frames += 4
    app.show_boss_attack += 10
    app.boss_stagger = 0    

def b4_a2(app):
    if app.enemy_direction == 1:

        app.enemy_attack_x1 = app.enemy_pos_x - 10 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_x - 40 
        app.enemy_attack_y2 = app.enemy_pos_y + 10
    elif app.enemy_direction == -1:
        app.enemy_attack_x1 = app.enemy_pos_hix + 10 
        app.enemy_attack_y1 = app.enemy_pos_y + 70
        app.enemy_attack_x2 = app.enemy_pos_hix + 40 
        app.enemy_attack_y2 = app.enemy_pos_y + 10   
    enemy_attack_hitbox = app.enemy_attack_x1, app.enemy_attack_y1, app.enemy_attack_x2, app.enemy_attack_y2
    if collision_detection_enemy_attack(app, enemy_attack_hitbox) == True and app.i_frames == 0:
        app.player_health -= 10
        app.i_frames += 6
    app.show_boss_attack += 10
    app.boss_stagger = 0  

def b4_a3(app):

    app.b4_a3_done = True


def projectile_manage_4(app):
    pass
##############################
############init game#######
############################

def init_baby(app):
    app.player_lives = 3
    app.play_from_map = False
    app.diff = "Baby"
def init_easy(app):
    app.player_lives = 1
    app.play_from_map = False
    app.diff = "Easy"
def init_hard(app):
    app.player_lives = 1
    app.player_health = 1
    app.play_from_map = False
    app.diff = "Hard"
################################
###############init classes##########
###############################
def init_playable_character_one(app):
    if app.invert_check % 2 != 0:
            invert_controll(app)
    app.player_direction = "East"
    app.player_state = "Idle"
    app.player_moving = False
    app.player_health = 100
    app.player_pos_x = 300 -48
    app.player_pos_y = 380
    app.player_pos_hix = 300
    app.player_pos_hiy = 424 
    app.player_took_damage = 0

def soft_init_player(app):
    app.player_direction = "East"
    app.player_state = "Idle"
    app.player_pos_x = 300 -48
    app.player_pos_y = 380
    app.player_pos_hix = 300
    app.player_pos_hiy = 424 
    if app.invert_check % 2 != 0:
        invert_controll(app)
def init_boss_1(app):
    music.stop_all_sounds()
    app.boss_fight = "One"
    app.boss_stage = ""
    app.enemy_action = "Idle"
    app.enemy_direction = 1
    app.enemy_health = 900
    app.enemy_pos_x = 700
    app.enemy_pos_hix = 740
    app.enemy_pos_y = 380
    app.enemy_pos_hiy = 440
    app.game_state = "Running"
    app.music_boss_one.play()
    app.animate_b1_a1 = False
    app.b1_a1_f = 0
    app.animation_tick = 0
    app.stagger = False
    app.enemy_i_frames = 0

def init_boss_2(app):
    music.stop_all_sounds()
    app.enemy_direction = 1
    app.show_attack_1 = False
    app.show_attack_3 = False
    app.boss_fight = "Two"
    app.boss_stage = "One"
    app.enemy_action = "Idle"
    app.enemy_health = 600
    app.enemy_pos_x = 720
    app.enemy_pos_hix = 736
    app.enemy_pos_y = 380
    app.enemy_pos_hiy = 440
    app.enemy_cd = 20
    app.game_state = "Running"
    app.music_boss_two.play()

    app.stop_showing_b2_a1 = 0
    app.stop_showing_b2_a3 = 0
    app.enemy_tp_cd = 0
    app.boss_two_teleport = False
    app.b2_p_cd = False
    app.b2_animation_f = 0
    app.animation_tick = 0
    app.b2_animation = 0
    app.enemy_i_frames = 0

def init_boss_3(app):
    music.stop_all_sounds()
    app.enemy_action = "Idle"
    app.boss_fight = "Three"
    app.boss_stage = ""
    app.projectile_2 = [0 , 0 , 0 , 0]
    app.enemy_health = 400
    app.enemy_pos_x = 700
    app.enemy_pos_hix = 710
    app.enemy_pos_y = 380
    app.enemy_pos_hiy = 440
    app.enemy_i_frames = 0
    app.game_state = "Running"
    app.show_projectile_3 = False
    app.player_invert_controll = 0
    app.show_b3_a2 = False
    app.show_b3_a3 = False
    app.stop_showing_b3_a3 = 0
    app.b3_a2_f = 0 
    app.enemy_direction = 1
    app.music_boss_three.play()

def init_final_boss(app):
    music.stop_all_sounds()
    app.boss_fight = "Final"
    app.boss_stage = "One"
    app.enemy_health = 700
    app.enemy_pos_x = 700
    app.enemy_pos_hix = 740
    app.enemy_pos_y = 380
    app.enemy_pos_hiy = 440
    app.game_state = "Running"
    app.enemy_i_frames = 0
    app.enemy_action = "Idle"
    app.enemy_direction = 1
    app.b4_animation_f = 0
    app.animation_tick = 0
    app.b4_a1_frame = 0
    app.b4_a2_frame = 0
    app.final_boss_song.play()
    app.b4_a3_done = False
######

###########player management######
    
def player_movement(app):
    if app.player_direction == "West" and app.attack_stops_movement == 0:
        app.player_facing = -1
    elif app.player_direction == "East" and app.attack_stops_movement == 0:
        app.player_facing = 1 

    if app.player_direction == "West" and app.player_moving == True and app.attack_stops_movement == 0 and app.player_pos_x - 10 > 0:
        app.player_pos_x -= 10 
        app.player_pos_hix -= 10
        app.player_state = "Walking"
    elif app.player_direction == "East" and app.player_moving == True and app.attack_stops_movement == 0 and app.player_pos_hix + 10 < 900:
        app.player_pos_x += 10 
        app.player_pos_hix += 10
        app.player_state = "Walking"

def player_health(app):
    if app.player_health == 0:
        pass

def basic_attack(app):
    app.basic_attack_cooldown += 10
    app.attack_stops_movement = 12
    app.show_basic_attack = 10
    app.player_state = "Attack"
    app.idle_counter = 10
    app.do_animation = 5
    app.animation_counter = 0

    if app.player_direction == "East":
        attack_hitbox = app.player_pos_hix, app.player_pos_y+40, app.player_pos_hix + 60, app.player_pos_y+20
    if app.player_direction == "West":
        attack_hitbox = app.player_pos_x - 60, app.player_pos_y+40, app.player_pos_x, app.player_pos_y+20
    app.attack_hitbox = attack_hitbox
    if attack_collision_detection(app, attack_hitbox) == True:
        app.enemy_hit = 10
        if app.enemy_health - 50 <= 0:
            kill_enemy(app)

        elif app.enemy_health >= 0:
            app.enemy_health -= 50

        if app.boss_fight == "Two" and app.boss_stage == "One":
            teleport_boss_two(app)

def player_dodge(app):
    app.i_frames = 6


def player_dead_check(app):
    if app.player_health < 1:
        #player død
        
        pass

####collison detection

def attack_collision_detection(app, attack_hitbox):
    hitbox_lo_x = attack_hitbox[0] 
    hitbox_lo_y = attack_hitbox[1]
    hitbox_hi_x = attack_hitbox[2] 
    hitbox_hi_y = attack_hitbox[3] 
    #if hit, enemy_hit += 10
    if hitbox_lo_x >= app.enemy_pos_x and hitbox_lo_x <= app.enemy_pos_x + 100:
        enemy_hit = True
        app.enemy_i_frames = 6
        return enemy_hit
    elif hitbox_hi_x >= app.enemy_pos_x and hitbox_hi_x <= app.enemy_pos_x + 50:
        enemy_hit = True
        app.enemy_i_frames = 6
        return enemy_hit
    
def collision_detection_enemy_attack(app, attack_hitbox):
    hitbox_lo_x = attack_hitbox[0] 
    hitbox_lo_y = attack_hitbox[1]
    hitbox_hi_x = attack_hitbox[2] 
    hitbox_hi_y = attack_hitbox[3] 

    #to fix##############
    if hitbox_lo_x >= app.player_pos_x and hitbox_hi_x <= app.player_pos_x:
        enemy_hit = True
    elif hitbox_lo_x >= app.player_pos_hix and hitbox_hi_x <= app.player_pos_hix:
        enemy_hit = True
    elif (hitbox_lo_x + hitbox_hi_x) / 2 >= app.player_pos_x and (hitbox_lo_x + hitbox_hi_x) / 2 <= app.player_pos_hix:
        enemy_hit = True
    elif app.player_pos_x >= hitbox_lo_x and app.player_pos_x <= hitbox_hi_x:
        enemy_hit = True
    elif app.player_pos_hix >= hitbox_lo_x and app.player_pos_hix <= hitbox_hi_x:
        enemy_hit = True
    else:
        enemy_hit = False

    if enemy_hit == True:
        app.player_took_damage = 6
    return enemy_hit

def collision_detection(app):
    if app.player_pos_x == app.enemy_pos_x or app.player_pos_x == app.enemy_pos_x + 50:
        if app.i_frames > 0:
            pass
        else:
            app.player_health -= 1
            app.i_frames += 4
    

    

def kill_enemy(app):
    killed_boss_init(app)

def killed_boss_init(app):
    if app.boss_fight == "One":
        app.game_state = "Boss_One_Down"
        if app.beaten_b1 == False:
            app.beaten_b1 = True
    if app.boss_fight == "Two":
        app.game_state = "Boss_Two_Down"
        if app.beaten_b2 == False:
            app.beaten_b2 = True
    if app.boss_fight == "Three":
        app.game_state = "Boss_Three_Down"
        if app.beaten_b3 == False:
            app.beaten_b3 = True
    
def next_boss(app):
    if app.boss_fight == "One":
        soft_init_player(app)
        init_boss_2(app)
    if app.boss_fight == "Two":
        soft_init_player(app)
        init_boss_3(app)
    if app.boss_fight == "Three":
        soft_init_player(app)
        init_final_boss(app)
    if app.boss_fight == "Final":
        victory_screen(app)

def kill_player(app):
    app.player_lives -= 1
    death_screen_init(app)


def invert_controll(app):
    temp_r = app.bind_right
    temp_l = app.bind_left
    app.bind_right = temp_l
    app.bind_left = temp_r
    app.invert_check += 1



##### settings controllere####
def main_menu_pressed(app):
    if app.menu_selector == 0:
        if app.debug == True:
            map_init(app)
        else:
            init_difficulty_menu(app)
        
        
    if app.menu_selector == 1:
        settings_init(app)
        
    app.menu_selector = 0
    app.menu_selector_x = 0

def settings_menu_pressed(app):
    if app.menu_selector == 0 and app.menu_selector_x == 0 and app.input_delay_menu == 0:
        rebind_init(app)
    if app.menu_selector == 1 and app.menu_selector_x == 0 and app.input_delay_menu == 0:
        map_init(app)
    if app.menu_selector == 0 and app.menu_selector_x == 1 and app.input_delay_menu == 0:
        sound_screen_init(app)

    app.menu_selector = 0
    app.menu_selector_x = 0



def difficulty_menu_pressed(app):
 
    if app.menu_selector == 0 and app.input_delay_menu == 0:
        init_boss_1(app)
        init_playable_character_one(app)
        init_baby(app)
    if app.menu_selector == 1 and app.input_delay_menu == 0:
        init_boss_1(app)
        init_playable_character_one(app)
        init_easy(app)
    if app.menu_selector == 2 and app.input_delay_menu == 0:
        init_boss_1(app)
        init_playable_character_one(app)
        init_hard(app)

    app.input_delay_menu += 1

def map_button_pressed(app):
    if app.menu_selector == 0 and app.menu_selector_x == 0:
        init_boss_1(app)
        init_playable_character_one(app)
    if app.menu_selector == 1 and app.menu_selector_x == 0:
        init_boss_2(app)
        init_playable_character_one(app)
    if app.menu_selector == 0 and app.menu_selector_x == 1:
        init_boss_3(app)
        init_playable_character_one(app)
    if app.menu_selector == 1 and app.menu_selector_x == 1:
        init_final_boss(app)
        init_playable_character_one(app)
    app.play_from_map = True
    app.menu_selector = 0
    app.menu_selector_x = 0

def rebind_button_pressed(app):
    if app.menu_selector == 0 and app.menu_selector_x == 0 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Up"
        
    elif app.menu_selector == 1 and app.menu_selector_x == 0 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Down"
    elif app.menu_selector == 2 and app.menu_selector_x == 0 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Left"
    elif app.menu_selector == 3 and app.menu_selector_x == 0 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Right"
    elif app.menu_selector == 0 and app.menu_selector_x == 1 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Dodge"
    elif app.menu_selector == 1 and app.menu_selector_x == 1 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Dash"
    elif app.menu_selector == 2 and app.menu_selector_x == 1 and app.input_delay_menu == 0:
        app.game_state = "Binding_key"
        app.action_to_bind = "Attack"
    elif app.menu_selector == 3 and app.menu_selector_x == 1 and app.input_delay_menu == 0:
        rebind_init(app)
        app.menu_selector = 0
        app.menu_selector_x = 0

    app.bind_timer = 100
    app.listening_to_input = True

def rebind_keys(app):
    if app.action_to_bind == "Up":
        app.bind_up = app.new_bound
    elif app.action_to_bind == "Down":
        app.bind_down = app.new_bound
    elif app.action_to_bind == "Left":
        app.bind_left = app.new_bound
    elif app.action_to_bind == "Right":
        app.bind_right = app.new_bound
    elif app.action_to_bind == "Attack":
        app.bind_attack = app.new_bound
    elif app.action_to_bind == "Dodge":
        app.bind_dodge = app.new_bound  
    elif app.action_to_bind == "Dash":
        app.bind_dash = app.new_bound     

    rebind_buttons(app)
    app.game_state = "Rebind"
    app.listening_to_input = False
    app.new_bound = 0

def sound_menu_button_pressed(app):
    pass


##### menyer init#####
def map_init(app):
    music.stop_all_sounds()

    app.game_state = "Map"
    app.map_song.play()
    if app.invert_check % 2 != 0:
        invert_controll(app)
def settings_init(app):
    app.game_state = "Settings"

def rebind_init(app):
    app.game_state = "Rebind"

def init_menu(app):
    
    music.stop_all_sounds()
    app.game_state = "Menu"
    app.main_menu_song.play()
def init_menu_from_settings(app):
    app.game_state = "Menu"
def death_screen_init(app):
    music.stop_all_sounds()
    app.game_state = "Dead"
    app.death_song.play()
def init_difficulty_menu(app):
    music.stop_all_sounds()
    app.game_state = "Difficulty"
    app.map_song.play()

def sound_screen_init(app):
    app.game_state = "Sound_screen"

def victory_screen(app):
    victory_text(app)
    app.game_state = "Victory"

def victory_text(app):
    r = random.randrange(3)
    if app.diff == "Baby":
        if r == 0:
            app.victory_text ="Attempt number 100?"
        if r == 1:
            app.victory_text ="I knew you would get it!\n .... eventually"
        if r == 2:
            app.victory_text ="You did your best!"
    if app.diff == "Easy":
        if r == 0:
            app.victory_text ="We are all so proud of you"
        if r == 1:
            app.victory_text ="This is when the game begins!"
        if r == 2:
            app.victory_text ="You did your best!"
    if app.diff == "Hard":
        app.victory_text = "You won....\n But at what cost?"

##############################
##############Keys#################
#############################

def key_released(app, event):
    if (event.key == app.enter_bind):
        input_delay(app)
    if (event.key == "Escape"):
        input_delay(app)

    if app.game_state == "Running":
        if (event.key == app.bind_left) and app.player_direction == "West":
            app.player_moving = False
            
        if (event.key == app.bind_right) and app.player_direction == "East":
            app.player_moving = False



def key_pressed(app, event):
    if app.listening_to_input == True and app.input_delay_menu == 0:
        if (event.key == "Escape"):
            rebind_init(app)
            app.listening_to_input = False
        if (event.key == app.enter_bind):
            pass
        else:
            app.new_bound = (event.key)

    if app.game_state == "Running":
        if (event.key == app.bind_dash) and app.dash_timer == 0:
            app.player_pos_x += 40 * app.player_facing
            app.player_pos_hix += 40 * app.player_facing
            app.dash_timer = 20
            app.i_frames += 2
        if (event.key == app.bind_dodge) and app.dodge_timer == 0:
            app.dodge_timer += 20
            player_dodge(app)
        if (event.key == app.bind_left) and app.input_delay == 0 and app.attack_stops_movement == 0:
            app.player_direction = "West"
            app.player_moving = 1
        elif (event.key == app.bind_right) and app.input_delay == 0 and app.attack_stops_movement == 0:
            app.player_direction = "East"
            app.player_moving = 1 
        elif (event.key == app.bind_attack) and app.basic_attack_cooldown == 0:
            basic_attack(app)


    elif app.game_state == "Menu":
        if (event.key == app.enter_bind):
            main_menu_pressed(app)
            app.input_delay_menu = 1
        elif (event.key == app.bind_up):
            if app.menu_selector > 0:
                app.menu_selector -= 1
        elif (event.key == app.bind_down):
            if app.menu_selector < 2:
                app.menu_selector += 1
    elif app.game_state == "Settings":
        if (event.key == app.enter_bind):
            settings_menu_pressed(app)
            app.input_delay_menu = 1   
        elif (event.key == "Escape"):
            init_menu_from_settings(app)
            app.input_delay_menu = 1
        elif (event.key == app.bind_up):
            if app.menu_selector > 0:
                app.menu_selector -= 1
        elif (event.key == app.bind_down):
            if app.menu_selector < 1:
                app.menu_selector += 1   
        elif (event.key == app.bind_left):
            if app.menu_selector_x > 0:
                app.menu_selector_x -= 1
        elif (event.key == app.bind_right):
            if app.menu_selector_x < 1:
                app.menu_selector_x += 1 
    elif app.game_state == "Sounds":
        pass
    elif app.game_state == "Difficulty":
        if (event.key == app.enter_bind):
            difficulty_menu_pressed(app)
            app.input_delay_menu = 1
        elif (event.key == "Escape"):
            init_menu(app)
        elif (event.key == app.bind_left):
            if app.menu_selector > 0:
                app.menu_selector -= 1
        elif (event.key == app.bind_right):
            if app.menu_selector < 2:
                app.menu_selector += 1 
    elif app.game_state == "Map":
        if (event.key == app.enter_bind) and app.input_delay_menu == 0:
            map_button_pressed(app)
            app.input_delay_menu = 1
        if (event.key == "Escape"):
            music.stop_all_sounds()
            settings_init(app)
            app.main_menu_song.play()
        elif (event.key == app.bind_up):
            if app.menu_selector > 0:
                app.menu_selector -= 1
        elif (event.key == app.bind_down):
            if app.menu_selector < 2:
                app.menu_selector += 1
        elif (event.key == app.bind_left):
            if app.menu_selector_x == 1:
                app.menu_selector_x = 0
        elif (event.key == app.bind_right):
            if app.menu_selector_x == 0:
                app.menu_selector_x = 1

    elif app.game_state == "Rebind":
        if (event.key == app.enter_bind) and app.input_delay_menu == 0:
            rebind_button_pressed(app)
        elif (event.key == "Escape") and app.input_delay_menu == 0:
            settings_init(app)
            app.input_delay_menu += 1
        elif (event.key == app.bind_up):
            if app.menu_selector > 0:
                app.menu_selector -= 1
        elif (event.key == app.bind_down):
            if app.menu_selector < 3:
                app.menu_selector += 1
        elif (event.key == app.bind_left):
            if app.menu_selector_x == 1:
                app.menu_selector_x = 0
        elif (event.key == app.bind_right):
            if app.menu_selector_x == 0:
                app.menu_selector_x = 1     
    elif app.game_state == "Boss_One_Down":
        if (event.key == app.enter_bind) and app.play_from_map == False:
            next_boss(app)
        elif (event.key == app.enter_bind):
            map_init(app)
    
    elif app.game_state == "Boss_Two_Down" :
        if (event.key == app.enter_bind) and app.play_from_map == False:
            next_boss(app)
        elif (event.key == app.enter_bind):
            map_init(app)
    
    elif app.game_state == "Dead":
        if (event.key == "r"):
            if app.player_lives > 0:
                if app.boss_fight == "One":
                    init_boss_1(app)
                    init_playable_character_one(app)
                if app.boss_fight == "Two":
                    init_boss_2(app)
                    init_playable_character_one(app)
                if app.boss_fight == "Three":
                    init_boss_2(app)
                    init_playable_character_one(app)
            else:
                map_init(app)


            









#### mitt tegnebrett ##################
def redraw_all(app, canvas):

    if app.game_state == "Running":
        draw_backgrounds(app, canvas)
        if app.show_basic_attack > 0 and app.debug == True:
            draw_basic_attack(app, canvas)
            draw_character_hitbox(app, canvas)
        draw_character_advanced(app, canvas)
        if app.debug == True:
            canvas.create_text ( 100, 300 ,
                                text=f"{app.player_state}",
                                font="times 30")
            canvas.create_text(100, 400,
                            text=app.enemy_action)
        ############boss fights
        if app.boss_fight == "One":
            if app.debug == True:
                draw_boss_one_hitbox(app, canvas)
                draw_boss_one_healthbar(app, canvas)
            draw_boss_one(app, canvas)
            
        elif app.boss_fight == "Two":
            draw_boss_two(app, canvas)
            if app.show_boss_attack > 0 and app.debug == True:
                draw_boss_two_attack(app, canvas)
            if app.show_projectile_1 == True:
                canvas.create_image(app.projectile_1[0][0] + 12, app.projectile_1[0][1],pil_image=app.b2_p1_i)

            if app.show_projectile_2 == True:

                canvas.create_image(app.projectile_1[1][0] + 12, app.projectile_1[1][1],pil_image=app.b2_p1_i)
        elif app.boss_fight == "Three":
            draw_boss_three(app, canvas)
            draw_boss_three_projectiles(app, canvas)
            if app.show_boss_attack > 0 and app.debug == True:
                draw_boss_two_attack(app, canvas)
        elif app.boss_fight == "Final":
            if app.show_boss_attack > 0 and app.debug == True:
                draw_boss_two_attack(app, canvas)
            if app.debug == True:
                draw_boss_one_hitbox(app, canvas)
                canvas.create_text(200, 200, text=app.enemy_health,fill="white")
            draw_boss_final(app, canvas)


    elif app.game_state == "Menu":
        draw_main_menu(app, canvas)
        draw_main_menu_selector(app, canvas)
        for button in app.main_menu_buttons:
            draw_main_menu_buttons(app, button , canvas)
    elif app.game_state ==  "Binding_key":
        draw_binding_key_pop_up(app, canvas)
    elif app.game_state == "Map":
        draw_map_selector(app, canvas)
        for button in app.map_buttons:
            draw_map_buttons(app, button , canvas)
    elif app.game_state == "Settings":
        for button in app.settings_buttons:
            draw_setting_buttons(app, button, canvas)
        draw_settings_selector(app, canvas)
    elif app.game_state == "Difficulty":
        for button in app.difficulty_buttons:
            draw_difficulty_buttons(app, button, canvas)
        draw_difficulty_selector(app, canvas)
    elif app.game_state == "Rebind":
        for button in app.rebind_buttons:
            draw_rebind_buttons(app , button , canvas)
        draw_rebind_selector(app, canvas)
    elif app.game_state == "Boss_One_Down":
        canvas.create_text(450, 450, text=f"Borg is dead\r press {app.enter_bind} to continue")
    elif app.game_state == "Boss_Two_Down":
        canvas.create_text(450, 450, text=f"Berg is dead\r press {app.enter_bind} to continue")
    elif app.game_state == "Dead":
        draw_death_screen(app, canvas)
    elif app.game_state == "Victory":
        draw_victory_screen(app, canvas)



def main_menu_buttons(app):
    app.main_menu_buttons =[[100 , 100, 300 , 300 , "Start"],
                            [100 , 320 , 300 , 520 , "Settings"],
                            [100 , 540, 300 , 740, "Blank"]
                        ]
def map_buttons(app):
    #temp, må polishes (bare for debug)
    app.map_buttons = [[100, 100, 400 , 400, "Boss 1"],
                       [100 , 450, 400 , 750, "Boss 2"],
                       [450, 100, 750, 400, "Boss 3"],
                       [450, 450, 750, 750, "Final Boss"]
                    ]
def settings_buttons(app):

    app.settings_buttons = [[100, 100, 400 , 400, "Rebinds"],
                            [100, 450, 400, 750, "Map"],
                            [500, 100, 800, 400, "Sound"],
                            [500, 450, 800, 750, "Clear profile"]
                            ]

    app.difficulty_buttons= [[100, 300, 300, 500, "Baby"],
                             [350, 300, 550, 500, "Easy"],
                             [600, 300, 800, 500, "Hard"]
                             ]
def rebind_buttons(app):
    app.rebind_buttons = [[100, 70, 300, 260, f"Up \n[{app.bind_up}]"],
                          [100, 270, 300, 460, f"Down\n  [{app.bind_down}]"],
                          [100, 470, 300, 660, f"Left\n [{app.bind_left}]"],
                          [100, 670, 300, 860, f"Right\n  [{app.bind_right}]"],
                          [350, 70, 550, 260, f"Dodge\n [{app.bind_dodge}]"],
                          [350, 270, 550, 460, f"Dash\n[{app.bind_dash}]"],
                          [350, 470, 550, 660, f"Attack\n[{app.bind_attack}]"],
                          [350, 670, 550, 860, "blank\nBack"]
                          ]

    
################ tegne funksjoner ################

def draw_main_menu_buttons(app, button , canvas):
    x1, y1, x2, y2 , label = button
    canvas.create_rectangle(x1, y1, 
                            x2, y2,
                            fill=app.button_color)
    canvas.create_text( (x1 + x2)/2, (y1+y2)/2,
                       text=label,
                       font="times 20")
    
def draw_map_buttons(app, button , canvas):
    x1, y1, x2, y2 , label = button
    canvas.create_rectangle(x1, y1, 
                            x2, y2,
                            fill=app.button_color)
    canvas.create_text( (x1 + x2)/2, (y1+y2)/2,
                       text=label,
                       font="times 20")
def draw_setting_buttons(app, button , canvas):
    x1, y1, x2, y2 , label = button
    canvas.create_rectangle(x1, y1, 
                            x2, y2,
                            fill=app.button_color)
    canvas.create_text( (x1 + x2)/2, (y1+y2)/2,
                       text=label,
                       font="times 20")
def draw_difficulty_buttons(app, button, canvas):
    x1, y1, x2, y2 , label = button
    canvas.create_rectangle(x1, y1, 
                            x2, y2,
                            fill=app.button_color)
    canvas.create_text( (x1 + x2)/2, (y1+y2)/2,
                       text=label,
                       font="times 20")

def draw_rebind_buttons(app, button, canvas):
    x1, y1, x2, y2 , label = button
    canvas.create_rectangle(x1, y1, 
                            x2, y2,
                            fill=app.button_color)
    canvas.create_text( (x1 + x2)/2, (y1+y2)/2,
                       text=label, 
                       font="times 25")
def draw_main_menu(app, canvas):

    canvas.create_image(450, 450 , pil_image=app.main_menu_bg)

def draw_main_menu_selector(app, canvas):
    canvas.create_rectangle(100, 100 + (app.menu_selector) * 220, 
                            300  , 300 + (app.menu_selector *220),
                            fill="", outline="red",width=5)
    
def draw_map_selector(app, canvas):
    canvas.create_rectangle(100 +(app.menu_selector_x * 350),100 + (app.menu_selector) * 350, 
                            400 +(app.menu_selector_x * 350), 400 + (app.menu_selector *350),
                            fill="", outline="red",width=5)

def draw_settings_selector(app, canvas):
    canvas.create_rectangle(100 +(app.menu_selector_x * 400), 100 + (app.menu_selector * 350), 
                            400 +(app.menu_selector_x * 400), 400 + (app.menu_selector *350),
                            fill="", outline="red",width=5)

def draw_difficulty_selector(app, canvas):
    canvas.create_rectangle(100 + (app.menu_selector * 250), 300  , 
                            300 + (app.menu_selector *250) , 500 ,
                            fill="", outline="red",width=5)
def draw_rebind_selector(app, canvas):
    canvas.create_rectangle(100 + (app.menu_selector_x * 250), 70 + (app.menu_selector * 200)  , 
                            300 + (app.menu_selector_x *250) , 260 + (app.menu_selector*200) ,
                            fill="", outline="red",width=5)  
def draw_character_hitbox(app, canvas):
    
    canvas.create_rectangle(app.player_pos_x, app.player_pos_y ,
                       app.player_pos_hix, app.player_pos_hiy,
                       fill=app.player_color)


    
def draw_character_advanced(app, canvas):

    ### skal byttes ut til noe renere og penere
    draw_hud_player(app, canvas)
    if app.player_state == "Idle":
        if app.player_direction == "East":
            canvas.create_image(app.player_pos_x + 48, app.player_pos_y+25, pil_image=app.player_idle_animation[app.animation_counter] )
        elif app.player_direction == "West":
            canvas.create_image(app.player_pos_x, app.player_pos_y+25, pil_image=app.player_idle_animation1[app.animation_counter] )
    if app.player_state == "Walking":
        if app.player_direction == "East":
            canvas.create_image(app.player_pos_x + 48, app.player_pos_y + 25, pil_image=app.player_walking_animation[app.animation_counter])
        elif app.player_direction == "West":
            canvas.create_image(app.player_pos_x, app.player_pos_y + 25, pil_image=app.player_walking_animation1[app.animation_counter])
    if app.player_state == "Attack":
        if app.player_direction == "East":
            canvas.create_image(app.player_pos_x + 48 , app.player_pos_y + 25 , pil_image=app.player_attack_animation[app.animation_counter])
        elif app.player_direction == "West":
            canvas.create_image(app.player_pos_x, app.player_pos_y + 25 , pil_image=app.player_attack_animation1[app.animation_counter])
    if app.i_frames > 0:
        if app.player_direction == "East":
            canvas.create_image(app.player_pos_x + 48, app.player_pos_y+25, pil_image=app.player_iframes)
        elif app.player_direction == "West":
            canvas.create_image(app.player_pos_x , app.player_pos_y+25, pil_image=app.player_iframesr)
    if app.player_took_damage > 0:
        if app.player_direction == "East":
            canvas.create_image(app.player_pos_x +48, app.player_pos_y +25, pil_image=app.player_damaged_image)
        elif app.player_direction == "West":
            canvas.create_image(app.player_pos_x , app.player_pos_y+25, pil_image=app.player_damaged_imager)


def draw_boss_one(app , canvas):
    if app.show_boss_attack > 0 and app.debug == True:
        draw_boss_one_attack(app, canvas)
    if app.animate_b1_a1 == True and app.enemy_action == "Attack_1":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x-36, app.enemy_pos_y + 24, pil_image=app.boss1_attack1[app.b1_a1_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x + 77, app.enemy_pos_y + 24, pil_image=app.boss1_attack1f[app.b1_a1_f])
    elif app.animate_b1_a1 == True and app.enemy_action == "Attack_2":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x-36, app.enemy_pos_y + 24, pil_image=app.boss1_attack2[app.b1_a1_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x + 77, app.enemy_pos_y + 24, pil_image=app.boss1_attack2f[app.b1_a1_f])

    elif app.animate_b1_a1 == True and app.enemy_action == "Attack_3":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x -36, app.enemy_pos_y + 24,pil_image=app.boss1_attack3[app.b1_a1_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x + 77, app.enemy_pos_y + 24,pil_image=app.boss1_attack3f[app.b1_a1_f])
    else:
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x +12, app.enemy_pos_y +24, pil_image=app.boss_one_idle[0])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x + 30 , app.enemy_pos_y +24, pil_image=app.boss_one_idle1[0])
    if app.enemy_i_frames > 0:
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x+ 12, app.enemy_pos_y + 24, pil_image=app.boss1_hit)
        elif app.enemy_direction == -1: 
            canvas.create_image(app.enemy_pos_x +14, app.enemy_pos_y + 24, pil_image=app.boss1_hit)


def draw_boss_two(app, canvas):
    if app.debug == True:
        canvas.create_rectangle(app.enemy_pos_x, app.enemy_pos_y,
                                app.enemy_pos_hix, app.enemy_pos_hiy,
                                fill="green")
    canvas.create_image(app.enemy_pos_x-12, app.enemy_pos_y + 24, pil_image=app.boss_two_idle[app.b2_animation_f])
    if app.debug == True:
        canvas.create_text(app.enemy_pos_x, app.enemy_pos_y - 300,
                       text=app.enemy_health)
    if app.show_attack_1 == True:
        canvas.create_image(app.enemy_attack_x1 + 44, app.enemy_attack_y1 +1, pil_image=app.b2_a1_i[app.b2_a1_c])
    if app.show_attack_3 == True:
        canvas.create_image(app.enemy_attack_x1 + 44, app.enemy_attack_y1 +1, pil_image=app.b2_a3_i[app.b2_a3_c])


                     
def draw_boss_three(app, canvas):
    if app.debug == True:
        canvas.create_rectangle(app.enemy_pos_x, app.enemy_pos_y,
                                app.enemy_pos_hix, app.enemy_pos_hiy,
                                fill="green")
    canvas.create_image(app.enemy_pos_x, app.enemy_pos_y + 24, pil_image=app.b3)

    if app.show_b3_a2 == True:
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x - 48, app.enemy_pos_y +30, pil_image=app.b3_a2[app.b3_a2_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x + 48, app.enemy_pos_y +30, pil_image=app.b3_a2f[app.b3_a2_f])
    if app.show_b3_a3 == True:
        canvas.create_image(app.enemy_attack_x1 + 48, app.enemy_attack_y1+20, pil_image=app.b3_a3[app.b3_a3_f])
    if app.enemy_i_frames > 0:
        canvas.create_image(app.enemy_pos_x, app.enemy_pos_y + 24, pil_image=app.b3_hit)

def draw_boss_three_projectiles(app, canvas):
    
    if app.show_projectile_3 == True:
        canvas.create_image(app.projectile_2[0] +12, app.projectile_2[1], pil_image=app.b3_a1)
    if app.show_projectile_3 == True:
        canvas.create_rectangle(app.projectile_2[0], app.projectile_2[1] , app.projectile_2[2] , app.projectile_2[3], fill="black")

def draw_boss_final(app, canvas):
    if app.enemy_action == "Idle":    
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x+ 10, app.enemy_pos_y + 24, pil_image=app.b4_i[app.b4_animation_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x+ 30, app.enemy_pos_y + 24, pil_image=app.b4_i_f[app.b4_animation_f])
    elif app.enemy_action == "Walk_West":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x+10, app.enemy_pos_y + 24, pil_image=app.b4_w[app.b4_animation_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x+30, app.enemy_pos_y + 24, pil_image=app.b4_w_f[app.b4_animation_f])
    elif app.enemy_action == "Walk_East":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x+10, app.enemy_pos_y + 24, pil_image=app.b4_w_f[app.b4_animation_f])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x+30, app.enemy_pos_y + 24, pil_image=app.b4_w[app.b4_animation_f])
    elif app.enemy_action == "Attack_1":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x+10, app.enemy_pos_y + 24, pil_image=app.b4_a1[app.b4_a1_frame])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x+30, app.enemy_pos_y + 24, pil_image=app.b4_a1_f[app.b4_a1_frame])
    elif app.enemy_action == "Attack_2":
        if app.enemy_direction == 1:
            canvas.create_image(app.enemy_pos_x+10, app.enemy_pos_y + 24, pil_image=app.b4_a2[app.b4_a2_frame])
        elif app.enemy_direction == -1:
            canvas.create_image(app.enemy_pos_x+30, app.enemy_pos_y + 24, pil_image=app.b4_a2_f[app.b4_a2_frame])


def draw_basic_attack(app, canvas):
    canvas.create_rectangle(app.attack_hitbox[0], app.attack_hitbox[1],
                            app.attack_hitbox[2], app.attack_hitbox[3],
                            fill="blue")



def draw_boss_one_hitbox(app, canvas):
    canvas.create_rectangle(app.enemy_pos_x, app.enemy_pos_y,
                          app.enemy_pos_hix, app.enemy_pos_hiy,
                          fill=app.boss_color) 

def draw_boss_one_healthbar(app, canvas):
    canvas.create_text(app.enemy_pos_x, app.enemy_pos_y -300,
                       text=app.enemy_health)
    
def draw_boss_one_attack(app, canvas):
    canvas.create_rectangle(app.enemy_attack_x1, app.enemy_attack_y1,
                            app.enemy_attack_x2, app.enemy_attack_y2,
                            fill="blue")
def draw_boss_two_attack(app, canvas):
    canvas.create_rectangle(app.enemy_attack_x1, app.enemy_attack_y1,
                            app.enemy_attack_x2, app.enemy_attack_y2,
                            fill="blue")
    
def draw_death_screen(app, canvas):
    canvas.create_text(450, 450, 
                       text="You died\r press r to restart",
                       font="times, 30")

def draw_hud_player(app, canvas):
    if app.boss_fight == "One":
        canvas.create_rectangle(0 , 700 , 900, 900,
                            fill="ivory")
    elif app.boss_fight == "Two":
                canvas.create_rectangle(0 , 700 , 900, 900,
                            fill="pale violet red")
    canvas.create_image(200, 750, pil_image=app.healthbar)
    canvas.create_text(200, 750,
                       text=app.player_health,
                       font="times 20",
                       fill="white")
    for i in range(app.player_lives):
        canvas.create_image(160 + (i*36), 800, pil_image=app.player_icon)

def draw_backgrounds(app, canvas):
    if app.boss_fight == "One":
        canvas.create_image(450 , 250, pil_image=app.boss_one_bg)
    elif app.boss_fight == "Two":
        canvas.create_image(450 , 250, pil_image=app.boss_two_bg)
    elif app.boss_fight == "Three":
        canvas.create_image(450, 250, pil_image=app.boss_three_bg)
    elif app.boss_fight == "Final":
        canvas.create_image(450, 250, pil_image=app.boss_final_bg)
def draw_binding_key_pop_up(app, canvas):
    canvas.create_rectangle(300 , 300, 600 , 600,
                            fill=app.button_color)
    canvas.create_text(450, 450, 
                       text=f"You are binding{app.action_to_bind}\n press new key\n time left: {round(app.bind_timer / 10)}")


def draw_victory_screen(app, canvas):
    canvas.create_text( 450, 450,
                       text=f"You won on{app.diff}.\n {app.victory_text}")
def app_stopped(app):
    if app.invert_check % 2 != 0:
        invert_controll(app)

    profile = [app.beaten_baby, app.beaten_easy, app.beaten_hard, app.beaten_b1, app.beaten_b2, app.beaten_b3, app.beaten_b4,
                    app.bind_up, app.bind_down, app.bind_left, app.bind_right, app.bind_attack, app.bind_dodge, app.bind_dash]
    
    content =json.dumps(profile)
    
    Path("Story_of_Alfred/profile.json").write_text(content, encoding="utf-8")
    music.stop_all_sounds()
    

run_app(width=900,height=900)
