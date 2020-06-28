import arcade
import json
import random
import arcade_gui
import time


# declaring constants and default values
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "MapGame"
DEFAULT_BACKGROUND = arcade.load_texture(f"sprites/backgrounds/backg_clean.png")

DEFAULT_PLAYER_SPRITE = arcade.Sprite("sprites/player_sprites/crossh_cross.png", 0.1)

DEFAULT_TARGET = arcade.Sprite("sprites/targets/target_default.png", 0.1)


def load_sprite_scales():
    with open("utils/sprite_scales.json", "r") as scales_json:
        data = json.load(scales_json)
        return data


# classes that will be used within the views
class MenuButton(arcade.TextButton):

    def __init__(self, view, text, x, y, open_view, font_color=arcade.color.WHITE, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=250, height=75, theme=theme)
        self.view = view
        self.font_color = font_color
        self.open_view = open_view

    def on_press(self):
        self.open_view.setup()
        self.view.window.show_view(self.open_view)


class ExitButton(arcade.TextButton):
    def __init__(self, view, text, x=0, y=0, width=250, height=75, color=arcade.color.ROYAL_AZURE,
                 font_color=arcade.color.BLACK, secondary_color=arcade.color.BLACK, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=width, height=height, face_color=color,
                         font_color=font_color, highlight_color=secondary_color, theme=theme)
        self.view = view
        self.font_color = font_color

    def on_press(self):
        self.view.window.close()


class CustomizeButton(arcade.TextButton):
    def __init__(self, view, text, x, y, file, font_color=arcade.color.WHITE, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=200, height=50, theme=theme)
        self.font_color = font_color
        self.file = file
        self.view = view

    def on_press(self):
        sprites_scales = load_sprite_scales()
        if "target" in self.file:
            new_target = arcade.Sprite(f"sprites/targets/{self.file}", sprites_scales["sprites"]["targets"][self.file])
            self.view.target = new_target
        elif "crossh" in self.file:
            new_player_sprite = arcade.Sprite(f"sprites/player_sprites/{self.file}",
                                              sprites_scales["sprites"]["player_sprites"][self.file])
            self.view.player_sprite = new_player_sprite
        elif "backg" in self.file:
            background = arcade.load_texture(f"sprites/{self.file}")
            menu_view = MenuView(background, self.view.player_sprite, self.view.target)
            menu_view.setup()
            self.view.window.show_view(menu_view)
        elif "speed" in self.file:
            pass
        else:
            pass


class TextLabel(arcade.TextLabel):
    def __init__(self, text, x=0, y=0, font_size=15, font_name="Calibri", color=arcade.color.WHITE):
        super().__init__(text=text, x=x, y=y, font_size=font_size, font_name=font_name, color=color)


# first screen you see when starting the game, you have to set the size of your display
class ScreenView(arcade_gui.UIView):

    def __init__(self, player_sprite):
        super().__init__()
        self.theme = None
        self.player_sprite = player_sprite
        self.width = 1920
        self.height = 1080

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()
        self.set_buttons()

        input_box_width = arcade_gui.UIInputBox(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2,
            width=250,
            height=75,
            id="width_box"
        )

        input_box_height = arcade_gui.UIInputBox(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2 - 150,
            width=250,
            height=75,
            id="height_box"
        )

        self.add_ui_element(input_box_width)
        self.add_ui_element(input_box_height)

    def set_buttons(self):
        submit_button = arcade_gui.UIFlatButton(
            text='Submit',
            center_x=int(SCREEN_WIDTH / 2),
            center_y=int(SCREEN_HEIGHT / 2) - 250,
            width=200,
            height=40,
            id='submit_button'
        )
        self.add_ui_element(submit_button)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AZURE)
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Set Display Size", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                         arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Width", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("Height", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_event(self, event: arcade_gui.UIEvent):
        super(ScreenView, self).on_event(event)

        if event.type == arcade_gui.UIFlatButton.CLICKED and event.ui_element.id == "submit_button":
            self.open_menu()

    def open_menu(self):
        height_input: arcade_gui.UIInputBox = self.find_by_id("height_box")
        self.height = height_input.text

        width_input: arcade_gui.UIInputBox = self.find_by_id("width_box")
        self.width: arcade_gui.UIInputBox = width_input.text

        menu_view = MenuView(background=DEFAULT_BACKGROUND, target=DEFAULT_TARGET, player_sprite=DEFAULT_PLAYER_SPRITE)
        menu_view.setup()
        self.window.show_view(menu_view)


# start screen including any buttons to go further
class MenuView(arcade.View):

    def __init__(self, background, player_sprite, target):
        super().__init__()
        self.player_sprite = player_sprite
        self.theme = None
        self.background = background
        self.target = target

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()
        self.set_buttons()

    def set_buttons(self):
        start_button = MenuButton(self, "Start Game", 640, 430,
                                  GameView(background=self.background, player_sprite=self.player_sprite,
                                           target=self.target, score=0), arcade.color.WHITE, self.theme)
        customize_button = MenuButton(self, "Customize", 640, 340,
                                      CustomizeView(background=self.background, player_sprite=self.player_sprite,
                                                    target=self.target), arcade.color.WHITE, self.theme)
        exit_button = ExitButton(self, "Exit Game", 640, 250, font_color=arcade.color.WHITE, theme=self.theme)

        self.button_list.append(start_button)
        self.button_list.append(customize_button)
        self.button_list.append(exit_button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Game Menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


# view where the game will be played and displayed
class GameView(arcade.View):

    def __init__(self, background, player_sprite, target, score):
        super().__init__()

        self.background = background
        self.target = target
        self.theme = None

        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()

        self.score = score
        self.player_sprite = player_sprite
        self.player_sprite.center_x = 640
        self.player_sprite.center_y = 360
        self.player_list.append(self.player_sprite)

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()

        self.target_list = arcade.SpriteList()
        self.target.center_x = random.randrange(SCREEN_WIDTH)
        self.target.center_y = random.randrange(SCREEN_HEIGHT)
        self.target_list.append(self.target)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.target_list.draw()
        super().on_draw()
        self.player_list.draw()

        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 20, 680, arcade.color.BLACK, 25)

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(background=self.background, player_sprite=self.player_sprite, target=self.target,
                                   score=self.score)
            pause_view.setup()
            self.window.show_view(pause_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        targets = arcade.get_sprites_at_point([x, y], self.target_list)
        if targets:
            for target in targets:
                target.remove_from_sprite_lists()
                self.target.center_x = random.randrange(SCREEN_WIDTH)
                self.target.center_y = random.randrange(SCREEN_HEIGHT)
                self.target_list.append(self.target)
                self.score += 1
        else:
            for target in self.target_list:
                target.remove_from_sprite_lists()
                self.target.center_x = random.randrange(SCREEN_WIDTH)
                self.target.center_y = random.randrange(SCREEN_HEIGHT)
                self.target_list.append(self.target)

    def update(self, delta_time: float):
        self.target_list.update()


# pause menu that will be available by pressing "escape"
class PauseView(arcade.View):

    def __init__(self, background, player_sprite, target, score):
        super().__init__()

        self.background = background
        self.target = target
        self.theme = None

        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()

        self.score = score
        self.player_sprite = player_sprite
        self.player_sprite.center_x = 640
        self.player_sprite.center_y = 360
        self.player_list.append(self.player_sprite)

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()
        self.set_buttons()

    def set_buttons(self):
        leave_button = MenuButton(self, "Back To Menu", 640, 290,
                                  MenuView(background=self.background, player_sprite=self.player_sprite,
                                           target=self.target), arcade.color.WHITE, self.theme)
        self.button_list.append(leave_button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        super().on_draw()
        self.player_list.draw()

        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 20, 680, arcade.color.BLACK, 25)
        arcade.draw_text("Game Paused", SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, arcade.color.BLACK, 60)
        arcade.draw_text("Press ESCAPE To Return to Game", SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2 - 15,
                         arcade.color.BLACK, 15)

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            game_view = GameView(background=self.background, player_sprite=self.player_sprite, target=self.target,
                                 score=self.score)
            game_view.setup()
            self.window.show_view(game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


# the view where users can customize most thing of the game like crosshair or background
class CustomizeView(arcade.View):
    def __init__(self, background, player_sprite, target):
        super().__init__()
        self.player_sprite = player_sprite
        self.theme = None
        self.background = background
        self.target = target

    def set_button_textures(self):
        default = "sprites/button_default.png"
        hover = "sprites/button_hover.png"
        clicked = "sprites/button_locked.png"
        self.theme.add_button_textures(default, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.Theme()
        self.set_button_textures()

    def setup(self):
        self.setup_theme()
        self.set_targets()
        self.set_crosshairs()
        self.set_backgrounds()
        # self.set_speed()

    def set_targets(self):
        target_text = TextLabel(text="Targets", x=175, y=625, font_size=25)
        self.text_list.append(target_text)

        target_moehre = CustomizeButton(view=self, file="target_moehre.png", text="Moehre", x=175, y=575,
                                        theme=self.theme)
        self.button_list.append(target_moehre)

        target_default = CustomizeButton(view=self, file="target_default.png", text="Default", x=175, y=500,
                                         theme=self.theme)
        self.button_list.append(target_default)

    def set_crosshairs(self):
        crosshair_text = TextLabel(text="Crosshairs", x=425, y=625, font_size=25)
        self.text_list.append(crosshair_text)

        crossh_cross = CustomizeButton(view=self, file="crossh_cross.png", text="Cross", x=425, y=575, theme=self.theme)
        self.button_list.append(crossh_cross)

        crossh_dot = CustomizeButton(view=self, file="crossh_dot.png", text="Dot", x=425, y=500, theme=self.theme)
        self.button_list.append(crossh_dot)

        crossh_circle = CustomizeButton(view=self, file="crossh_circle.png", text="Circle", x=425, y=425,
                                        theme=self.theme)
        self.button_list.append(crossh_circle)

        crossh_cross_circle = CustomizeButton(view=self, file="crossh_cross_circle.png", text="Cross & Circle", x=425,
                                              y=350, theme=self.theme)
        self.button_list.append(crossh_cross_circle)

    def set_backgrounds(self):
        background_text = TextLabel(text="Backgrounds", x=675, y=625, font_size=25)
        self.text_list.append(background_text)

        background_clean = CustomizeButton(view=self, file="backgrounds/backg_clean.png", text="Clean", x=675, y=575,
                                           theme=self.theme)
        self.button_list.append(background_clean)

        background_forest = CustomizeButton(view=self, file="backgrounds/backg_forest.png", text="Forest", x=675, y=500,
                                            theme=self.theme)
        self.button_list.append(background_forest)

        background_mountains = CustomizeButton(view=self, file="backgrounds/backg_mountains.png", text="Mountains",
                                               x=675, y=425, theme=self.theme)
        self.button_list.append(background_mountains)

        background_sea = CustomizeButton(view=self, file="backgrounds/backg_sea.png", text="Sea", x=675, y=350,
                                         theme=self.theme)
        self.button_list.append(background_sea)

    """def set_speed(self):
        background_text = TextLabel(text="Speed", x=925, y=625, font_size=25)
        self.text_list.append(background_text)

        speed_beginner = CustomizeButton(text="Beginner", x=925, y=575, theme=self.theme)
        self.button_list.append(speed_beginner)

        speed_slow = CustomizeButton(text="Slow", x=925, y=500, theme=self.theme)
        self.button_list.append(speed_slow)

        speed_medium = CustomizeButton(text="Medium", x=925, y=425, theme=self.theme)
        self.button_list.append(speed_medium)

        speed_fast = CustomizeButton(text="Fast", x=925, y=350, theme=self.theme)
        self.button_list.append(speed_fast)

        speed_ultra = CustomizeButton(text="Ultra", x=925, y=275, theme=self.theme)
        self.button_list.append(speed_ultra)"""

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Customizations", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            menu_view = MenuView(background=self.background, player_sprite=self.player_sprite, target=self.target)
            menu_view.setup()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "MapGame")
    window.set_mouse_visible(False)
    screen_view = ScreenView(DEFAULT_PLAYER_SPRITE)
    screen_view.setup()
    window.show_view(screen_view)
    """menu_view = MenuView(background=DEFAULT_BACKGROUND, player_sprite=DEFAULT_PLAYER_SPRITE, target=DEFAULT_TARGET)
    menu_view.setup()
    window.show_view(menu_view)"""
    arcade.run()


if __name__ == "__main__":
    main()
