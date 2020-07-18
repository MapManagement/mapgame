import arcade
import json
import random
import time
import timeit
from arcade import gui
from arcade.gui import UIManager

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
class MenuButton(gui.UIFlatButton):

    def __init__(self, view, text, x, y, open_view, font_color=arcade.color.WHITE):
        super().__init__(text=text, center_x=x, center_y=y, width=250, height=75)
        self.view = view
        self.font_color = font_color
        self.open_view = open_view

        self.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

    def on_press(self):
        self.view.ui_manager.purge_ui_elements()
        self.open_view.setup()
        self.view.window.show_view(self.open_view)


class ExitButton(gui.UIFlatButton):
    def __init__(self, view, text, x=0, y=0, width=250, height=75, font_color=arcade.color.BLACK,
                 secondary_color=arcade.color.BLACK, theme=None):
        super().__init__(text=text, center_x=x, center_y=y, width=width, height=height, font_color=font_color,
                         highlight_color=secondary_color, theme=theme)
        self.view = view
        self.font_color = font_color

        self.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

    def on_press(self):
        self.view.window.close()


class CustomizeButton(gui.UIFlatButton):
    def __init__(self, view, text, x, y, file, id, font_color=arcade.color.WHITE):
        super().__init__(text=text, center_x=x, center_y=y, width=200, height=50, id=id)
        self.file = file
        self.view = view

        self.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

    def on_press(self):
        sprites_scales = load_sprite_scales()
        if "target" in self.file:
            new_target = arcade.Sprite(f"sprites/targets/{self.file}", sprites_scales["sprites"]["targets"][self.file])
            self.view.target = new_target
        elif "crossh" in self.file:
            new_player_sprite = arcade.Sprite(f"sprites/player_sprites/{self.file}",
                                              sprites_scales["sprites"]["player_sprites"][self.file])
            self.view.player_sprite = new_player_sprite
            self.view.player_list[0] = self.view.player_sprite

            menu_view = MenuView(self.view.background, self.view.player_sprite, self.view.target, self.view.height,
                                 self.view.width)
            self.view.ui_manager.purge_ui_elements()
            menu_view.setup()
            self.view.window.show_view(menu_view)

        elif "backg" in self.file:
            background = arcade.load_texture(f"sprites/{self.file}")
            menu_view = MenuView(background, self.view.player_sprite, self.view.target, self.view.height,
                                 self.view.width)
            self.view.ui_manager.purge_ui_elements()
            menu_view.setup()
            self.view.window.show_view(menu_view)
        else:
            pass


class TextLabel(gui.UILabel):
    def __init__(self, text, center_x=0, center_y=0, font_size=15, font_name="Calibri"):
        super().__init__(text=text, center_x=center_x, center_y=center_y, font_size=font_size, font_name=font_name)
        self.set_style_attrs(font_color=arcade.color.WHITE,
                             font_color_hover=arcade.color.WHITE)


class SensSubmitButton(CustomizeButton):
    def __init__(self, view, text, x, y):
        super().__init__(view=view, text=text, x=x, y=y, file=None, id="sens_submit_button")

        self.view = view

    def on_press(self):
        sensitivity = self.view.ui_manager.find_by_id("speed_box").text


class SubmitButton(gui.UIFlatButton):
    def __init__(self, text, center_x, center_y, width, height, view):
        super().__init__(text=text, center_x=center_x, center_y=center_y, width=width, height=height,
                         id="submit_button")
        self.view = view

        self.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

    def on_press(self):
        given_witdh = str(self.view.ui_manager.find_by_id("width_box").text)
        given_height = str(self.view.ui_manager.find_by_id("height_box").text)

        if given_height != "" and given_witdh != "":
            self.view.window.close()

            window = arcade.Window(int(given_witdh), int(given_height), fullscreen=True, title="MapGame")
            window.set_mouse_visible(False)
            menu_view = MenuView(background=DEFAULT_BACKGROUND, player_sprite=DEFAULT_PLAYER_SPRITE,
                                 target=DEFAULT_TARGET, height=int(given_height), width=int(given_witdh))
            menu_view.setup()
            window.show_view(menu_view)
            arcade.run()


# first screen you see when starting the game, you have to set the size of your display
class ScreenView(arcade.View):

    def __init__(self, player_sprite):
        super().__init__()
        self.ui_manager = UIManager(self.window)

        self.height = 720
        self.width = 1280

        self.player_sprite = player_sprite

    def setup(self):
        input_box_width = gui.UIInputBox(
            center_x=self.width / 2,
            center_y=self.height / 2,
            width=250,
            height=75,
            text=str(1920),
            id="width_box"
        )
        input_box_width.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

        input_box_height = gui.UIInputBox(
            center_x=self.width / 2,
            center_y=self.height / 2 - 150,
            width=250,
            height=75,
            text=str(1080),
            id="height_box"
        )
        input_box_height.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

        self.ui_manager.add_ui_element(input_box_width)
        self.ui_manager.add_ui_element(input_box_height)

        self.set_buttons()

    def set_buttons(self):
        submit_button = SubmitButton(
            text='Submit',
            center_x=int(self.width / 2),
            center_y=int(self.height / 2) - 250,
            width=200,
            height=40,
            view=self
        )
        submit_button.on_click()
        self.ui_manager.add_ui_element(submit_button)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AZURE)
        super().on_draw()
        self.player_sprite.draw()

        arcade.draw_text("Set Display Size", self.width / 2, self.height / 1.5,
                         arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("Width", self.width / 2, self.height / 2 + 50,
                         arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("Height", self.width / 2, self.height / 2 - 100,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


# start screen including any buttons to go further
class MenuView(arcade.View):

    def __init__(self, background, player_sprite, target, height, width):
        super().__init__()
        self.ui_manager = UIManager(self.window)

        self.height = height
        self.width = width

        self.background = background
        self.target = target

        self.player_list = arcade.SpriteList()

        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.width / 2
        self.player_sprite.center_y = self.height / 2
        self.player_list.append(self.player_sprite)

    def setup(self):
        self.set_buttons()

    def set_buttons(self):
        start_button = MenuButton(self, "Start Game", self.width / 2, self.height / 2,
                                  GameView(background=self.background, player_sprite=self.player_sprite,
                                           target=self.target, score=0, missed=0, height=self.height, width=self.width),
                                  font_color=arcade.color.WHITE)

        customize_button = MenuButton(self, "Customize", self.width / 2, self.height / 2 - 100,
                                      CustomizeView(background=self.background, player_sprite=self.player_sprite,
                                                    target=self.target, height=self.height, width=self.width),
                                      font_color=arcade.color.WHITE)

        exit_button = ExitButton(self, "Exit Game", self.width / 2, self.height / 2 - 200,
                                 font_color=arcade.color.WHITE)

        self.ui_manager.add_ui_element(start_button)
        self.ui_manager.add_ui_element(customize_button)
        self.ui_manager.add_ui_element(exit_button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
        super().on_draw()
        self.player_list.draw()

        arcade.draw_text("Game Menu", self.width / 2, self.height / 1.5,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


# view where the game will be played and displayed
class GameView(arcade.View):

    def __init__(self, background, player_sprite, target, height, width, score, missed):
        super().__init__()
        self.ui_manager = UIManager(self.window)

        self.height = height
        self.width = width

        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        self.background = background
        self.target = target
        self.theme = None

        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()

        self.score = score
        self.missed = missed
        self.timer = 0
        self.old_time = time.time()

        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.width / 2
        self.player_sprite.center_y = self.height / 2
        self.player_list.append(self.player_sprite)

    def setup(self):
        self.target_list = arcade.SpriteList()
        self.target.center_x = random.randrange(SCREEN_WIDTH)
        self.target.center_y = random.randrange(SCREEN_HEIGHT)
        self.target_list.append(self.target)

    def on_draw(self):
        draw_start_time = timeit.default_timer()
        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1

        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
        self.target_list.draw()
        super().on_draw()
        self.player_list.draw()

        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 20, self.height - 50, arcade.color.BLACK, 25)

        missed_text = f"Missed: {self.missed}"
        arcade.draw_text(missed_text, 20, self.height - 100, arcade.color.BLACK, 25)

        timer_text = f"Reaction Time: {round(self.timer, 3)}"
        arcade.draw_text(timer_text, 20, self.height - 150, arcade.color.BLACK, 25)

        if self.fps is not None:
            fps_text = f"FPS: {round(self.fps, 1)}"
            arcade.draw_text(fps_text, 20, self.height - 200, arcade.color.BLACK, 25)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(background=self.background, player_sprite=self.player_sprite, target=self.target,
                                   score=self.score, missed=self.missed, height=self.height, width=self.width)
            pause_view.setup()
            self.window.show_view(pause_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        targets = arcade.get_sprites_at_point([x, y], self.target_list)
        if targets:
            self.timer = time.time() - self.old_time
            self.old_time = time.time()
            for target in targets:
                target.remove_from_sprite_lists()
                self.target.center_x = random.randrange(self.width)
                self.target.center_y = random.randrange(self.height)
                self.target_list.append(self.target)
                self.score += 1
        else:
            self.missed += 1

    def update(self, delta_time: float):
        self.target_list.update()


# pause menu that will be available by pressing "escape"
class PauseView(arcade.View):

    def __init__(self, background, player_sprite, target, height, width, score, missed):
        super().__init__()
        self.ui_manager = UIManager(self.window)

        self.height = height
        self.width = width

        self.background = background
        self.target = target
        self.theme = None

        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()

        self.score = score
        self.missed = missed

        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.width / 2
        self.player_sprite.center_y = self.height / 2
        self.player_list.append(self.player_sprite)

    def setup(self):
        self.set_buttons()

    def set_buttons(self):
        leave_button = MenuButton(self, "Back To Menu", self.width / 2, self.height / 2 - 100,
                                  MenuView(background=self.background, player_sprite=self.player_sprite,
                                           target=self.target, height=self.height, width=self.width),
                                  arcade.color.WHITE)
        self.ui_manager.add_ui_element(leave_button)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
        super().on_draw()
        self.player_list.draw()

        score_text = f"Hits: {self.score}"
        arcade.draw_text(score_text, 20, self.height - 50, arcade.color.BLACK, 25)
        arcade.draw_text("Game Paused", self.width / 2.55, self.height / 2, arcade.color.BLACK, 60)
        arcade.draw_text("Press ESCAPE To Return to Game", self.width / 2.3, self.height / 2 - 25,
                         arcade.color.BLACK, 15)

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            game_view = GameView(background=self.background, player_sprite=self.player_sprite, target=self.target,
                                 score=self.score, missed=self.missed, height=self.height, width=self.width)
            self.ui_manager.purge_ui_elements()
            game_view.setup()
            self.window.show_view(game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


# the view where users can customize most thing of the game like crosshair or background
class CustomizeView(arcade.View):
    def __init__(self, background, player_sprite, target, height, width):
        super().__init__()
        self.ui_manager = UIManager(self.window)

        self.height = height
        self.width = width

        self.background = background
        self.target = target

        self.player_list = arcade.SpriteList()

        self.player_sprite = player_sprite
        self.player_sprite.center_x = self.width / 2
        self.player_sprite.center_y = self.height / 2
        self.player_list.append(self.player_sprite)

    def setup(self):
        self.set_mouse_speed()
        self.set_targets()
        self.set_crosshairs()
        self.set_backgrounds()
        self.set_mode()
        self.set_locked_texture(target_id="target_default", crosshair_id="crossh_cross",
                                background_id="background_clean", mode_id="mode_clicking")

    def set_mouse_speed(self):
        mouse_speed_text = TextLabel(text="Sensitivity", center_x=self.width / 2 - 500, center_y=self.height / 1.5,
                                     font_size=25)
        self.ui_manager.add_ui_element(mouse_speed_text)

        speed_input = gui.UIInputBox(center_x=self.width / 2 - 500, center_y=self.height / 1.5 - 75, font_size=25,
                                     width=200, height=50, text="1", id="speed_box")
        self.ui_manager.add_ui_element(speed_input)
        speed_input.set_style_attrs(
            font_color=arcade.color.WHITE,
            bg_color=arcade.color.BLACK,
            border_color=arcade.color.DAVY_GREY,
            bg_color_hover=arcade.color.DAVY_GREY,
            border_color_hover=arcade.color.BLACK
        )

        speed_submit = SensSubmitButton(view=self, text="Submit Sens", x=self.width / 2 - 500,
                                        y=self.height / 1.5 - 150)

        self.ui_manager.add_ui_element(speed_submit)

    def set_targets(self):
        target_text = TextLabel(text="Targets", center_x=self.width / 2 - 250, center_y=self.height / 1.5, font_size=25)
        self.ui_manager.add_ui_element(target_text)

        target_moehre = CustomizeButton(view=self, file="target_moehre.png", text="Moehre", x=self.width / 2 - 250,
                                        y=self.height / 1.5 - 75, id="target_moehre")
        self.ui_manager.add_ui_element(target_moehre)

        target_default = CustomizeButton(view=self, file="target_default.png", text="Default", x=self.width / 2 - 250,
                                         y=self.height / 1.5 - 150, id="target_default")
        self.ui_manager.add_ui_element(target_default)

    def set_crosshairs(self):
        crosshair_text = TextLabel(text="Crosshairs", center_x=self.width / 2, center_y=self.height / 1.5, font_size=25)
        self.ui_manager.add_ui_element(crosshair_text)

        crossh_cross = CustomizeButton(view=self, file="crossh_cross.png", text="Cross", x=self.width / 2,
                                       y=self.height / 1.5 - 75, id="crossh_cross")
        self.ui_manager.add_ui_element(crossh_cross)

        crossh_dot = CustomizeButton(view=self, file="crossh_dot.png", text="Dot", x=self.width / 2,
                                     y=self.height / 1.5 - 150, id="crossh_dot")
        self.ui_manager.add_ui_element(crossh_dot)

        crossh_circle = CustomizeButton(view=self, file="crossh_circle.png", text="Circle", x=self.width / 2,
                                        y=self.height / 1.5 - 225, id="crossh_circle")
        self.ui_manager.add_ui_element(crossh_circle)

        crossh_cross_circle = CustomizeButton(view=self, file="crossh_cross_circle.png", text="Cross & Circle",
                                              x=self.width / 2, y=self.height / 1.5 - 300, id="crossh_cross_circle")
        self.ui_manager.add_ui_element(crossh_cross_circle)

    def set_backgrounds(self):
        background_text = TextLabel(text="Backgrounds", center_x=self.width / 2 + 250, center_y=self.height / 1.5,
                                    font_size=25)
        self.ui_manager.add_ui_element(background_text)

        background_clean = CustomizeButton(view=self, file="backgrounds/backg_clean.png", text="Clean",
                                           x=self.width / 2 + 250, y=self.height / 1.5 - 75, id="background_clean")
        self.ui_manager.add_ui_element(background_clean)

        background_forest = CustomizeButton(view=self, file="backgrounds/backg_forest.png", text="Forest",
                                            x=self.width / 2 + 250, y=self.height / 1.5 - 150, id="background_forest")
        self.ui_manager.add_ui_element(background_forest)

        background_mountains = CustomizeButton(view=self, file="backgrounds/backg_mountains.png", text="Mountains",
                                               x=self.width / 2 + 250, y=self.height / 1.5 - 225,
                                               id="background_mountains")
        self.ui_manager.add_ui_element(background_mountains)

        background_sea = CustomizeButton(view=self, file="backgrounds/backg_sea.png", text="Sea",
                                         x=self.width / 2 + 250, y=self.height / 1.5 - 300, id="background_sea")
        self.ui_manager.add_ui_element(background_sea)

    def set_mode(self):
        mode_text = TextLabel(text="Mode", center_x=self.width / 2 + 500, center_y=self.height / 1.5, font_size=25)
        self.ui_manager.add_ui_element(mode_text)

        mode_clicking = CustomizeButton(view=self, file="", text="Clicking",
                                        x=self.width / 2 + 500, y=self.height / 1.5 - 75, id="mode_clicking")
        self.ui_manager.add_ui_element(mode_clicking)

        mode_tracking = CustomizeButton(view=self, file="", text="Tracking",
                                        x=self.width / 2 + 500, y=self.height / 1.5 - 150, id="mode_tracking")
        self.ui_manager.add_ui_element(mode_tracking)

        mode_flicking = CustomizeButton(view=self, file="", text="Flicking",
                                        x=self.width / 2 + 500, y=self.height / 1.5 - 225, id="mode_flicking")
        self.ui_manager.add_ui_element(mode_flicking)

        mode_pure_reaction = CustomizeButton(view=self, file="", text="Pure Reaction",
                                             x=self.width / 2 + 500, y=self.height / 1.5 - 300, id="mode_pure_reaction")
        self.ui_manager.add_ui_element(mode_pure_reaction)

    def set_locked_texture(self, target_id, crosshair_id, background_id, mode_id):
        locked_target: gui.UIElement = self.ui_manager.find_by_id(target_id)
        locked_crosshair: gui.UIElement = self.ui_manager.find_by_id(crosshair_id)
        locked_background: gui.UIElement = self.ui_manager.find_by_id(background_id)
        locked_mode: gui.UIElement = self.ui_manager.find_by_id(mode_id)

        locked_list = [locked_target, locked_crosshair, locked_background, locked_mode]

        for locked_button in locked_list:
            locked_button.set_style_attrs(
                bg_color=arcade.color.ASH_GREY,
                border_color=arcade.color.DAVY_GREY,
                bg_color_hover=arcade.color.ASH_GREY,
                border_color_hover=arcade.color.DAVY_GREY
            )

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
        super().on_draw()
        self.player_list.draw()

        arcade.draw_text("Customizations", self.width / 2, self.height / 1.1,
                         arcade.color.WHITE, 50, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_key_press(self, symbol: int, _modifiers):
        if symbol == arcade.key.ESCAPE:
            menu_view = MenuView(background=self.background, player_sprite=self.player_sprite, target=self.target,
                                 height=self.height, width=self.width)
            self.ui_manager.purge_ui_elements()
            menu_view.setup()
            self.window.show_view(menu_view)


def main():
    setup_window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "MapGame - Setup")
    setup_window.set_mouse_visible(False)
    screen_view = ScreenView(player_sprite=DEFAULT_PLAYER_SPRITE)
    screen_view.setup()
    setup_window.show_view(screen_view)
    arcade.run()


if __name__ == "__main__":
    main()
