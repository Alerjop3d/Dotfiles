#  $$$$$$\    $$\     $$\ $$\
# $$  __$$\   $$ |    \__|$$ |
# $$ /  $$ |$$$$$$\   $$\ $$ | $$$$$$\
# $$ |  $$ |\_$$  _|  $$ |$$ |$$  __$$\
# $$ |  $$ |  $$ |    $$ |$$ |$$$$$$$$ |
# $$ $$\$$ |  $$ |$$\ $$ |$$ |$$   ____|
# \$$$$$$ /   \$$$$  |$$ |$$ |\$$$$$$$\
#  \___$$$\    \____/ \__|\__| \_______|
#      \___|
#                     
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
from qtile_extras import widget
from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.widget.decorations import RectDecoration
from libqtile import bar, layout, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder



mod = "mod4"
terminal = guess_terminal()


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right",),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    Key([mod], "f12", lazy.spawn("coreshot"), desc="screen shot"),
    Key([mod, "control"], "g", lazy.spawn("google-chrome-stable"), desc="open google chrome"),
    Key([mod, "control"], "down", lazy.spawn("rofi -show"), desc="open spotify"),
    # Toggle between different layouts as defined belo
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "escape", lazy.screen.toggle_group(), desc="go to the last visited window"),
]
   
groups = [
    Group("1",
          matches=[
              Match(
                  wm_class=["Alacritty"]      
            )
        ],
         label="I"     
    ),
    Group("2",
          matches=[
              Match(
                  wm_class=["code"]
            ) 
        ],
          label="II"     
    ),
    Group("3",
          matches=[
              Match(
                  wm_class=["firefox"]
            )
        ],
          label="III" 
    ),


]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            # desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=3, margin=5),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    #layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.floating.Floating(margin=5),
]

widget_defaults = dict( 
    font="UbuntuNerdFont semibold", 
    fontsize=13,
    padding=2,
)
extension_defaults = widget_defaults.copy()

powerline = {
    "decorations": [
        PowerLineDecoration(path="arrow_right", padding=-1)
    ]
}

decoration_group = {
    "decorations": [
        RectDecoration(colour="#E8E8E8", radius=8, filled=True, padding_y=-2, group=True)
    ],
    "padding": 8,
}

@lazy.function
def launch_or_focus(qtile, app_name, group_name):
    try:
        subprocess.check_output(["pgrep", app_name])
    except subprocess.CalledProcessError:
        # El proceso no se encuentra en ejecución, lo lanzamos.
        qtile.cmd_spawn(app_name)
        qtile.groups_map[group_name].cmd_toscreen()
    else:
        # El proceso ya está en ejecución, puedes realizar alguna otra acción si es necesario.
        # Por ejemplo, cambiar el grupo de trabajo a la aplicación:
        qtile.groups_map[group_name].cmd_toscreen()
        
screens = [
    Screen(
        wallpaper="/usr/share/backgrounds/archlinux/waves.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                #widget.Visualiser(),
                widget.GroupBox(
                    margin=4,
                    fontsize=13,
                    padding=2,
                    highlight_method='line',
                    highlight_color=['#000000.00', '#000000.00'],
                    mouse_callbacks={ 
                            "Button1": launch_or_focus("alacritty", "1")
                    },
                ),
                widget.Spacer(length=20),
                widget.Notify(
                    default_timeout=25,
                    max_chars=150
                ),
                widget.Prompt(
                    prompt='>>>   '
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.WindowName(
                    format='',
                ),
                #Spotify(),
                widget.CPU(
                    padding=5,
                    fontsize=11.90,
                    format='{load_percent}%',
                ),
                widget.ThermalZone(
                    padding=5,
                    fontsize=11.90,
                   format='{temp}°C',
               ),
               widget.Clock(
                    padding=10,
                    fontsize=11.90,
                    format="%a %d %b %H:%M", #%b %a 
                ),
                #widget.Spacer(length=10),
                widget.Mpris2(
                    popup_layout=COMPACT_LAYOUT,
                    format='',
                    padding=5,
                    no_metadata_text='',
                    paused_text='',
                    playing_text='',
                    font="feather",
                    fontsize="11.50",
                ),
                widget.Volume(
                    font="feather",
                    fontsize=14.90,
                    emoji=True,
                    emoji_list=['', '', '', ''],
                ),
                widget.ALSAWidget(
                    update_interval=0.5,
                    hide_interval=1,
                    bar_colour_normal="#ffffff",
                    limit_normal=90,
                    bar_width=35,
                    bar_height=6,
                    text_format=(""),
                    step=4,
                    decorations=[
                        RectDecoration(colour="#000000",line_colour="#ffffff",line_width=1.5, radius=3, filled=False, padding_y=4)
                    ],
                ),
                widget.WiFiIcon(
                    padding=3.5,
                    mouse_callbacks={
                        "Button1": lazy.spawn("rofi-wifi-menu")
                    }
                ),
                widget.TextBox(
                    " ",
                    font="feather",
                    fontsize=10,
                    mouse_callbacks={
                        "Button1": lazy.spawn("rofi-bluetooth"),
                    }
                ),
                widget.UPowerWidget(
                    battery_width=18,
                    battery_height=9.5,
                    margin=0,
                    padding=6,               
                ),
                widget.Spacer(length=10), 
            ],
            18,
            background="#000000.85",
            opacity=1
        ),
    )   
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="archmain"),
        Match(wm_class="thunar"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
main = None
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True


dgroups_key_binder = simple_key_binder("mod3")


# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"