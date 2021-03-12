from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.list import ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivymd.icon_definitions import md_icons
Window.size = (350, 570)

KV = '''
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)
    on_press:
        self.parent.parent.parent.nav_drawer.set_state("close")
        self.parent.parent.parent.screen_manager.current = self.text
    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color
<Tab>:
    ScrollView:
        DrawerList:
            id: scroll
        
<ListItemWithCheckbox>:
    LeftCheckbox:
    MDLabel:
        text:self.text

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "image.jpg"

    MDLabel:
        text: "Todolist"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "test@gmail.com"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        DrawerList:
            id: md_list
           
Screen:
    NavigationLayout:
        ScreenManager:
            id: screen_manager
            Screen:
                name: "Home"
                id: home
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Home"
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                    BoxLayout:        
                        ScrollView:                                                   
                            MDTabs:
                                id: android_tabs
                                on_tab_switch: app.on_tab_switch(*args)              
                        
          

                MDTextField:
                    hint_text: "Add sub task here"
                    #helper_text: "or click on forgot username"
                    helper_text_mode: "on_focus"
                    icon_right: "send-outline"
                    icon_right_color: app.theme_cls.primary_color
                    pos_hint:{'center_x': 0.5, 'center_y': 0.05}
                    size_hint_x:None
                    width:300                                                       
                MDFloatingActionButton:
                    icon: "plus"
                    md_bg_color: app.theme_cls.primary_color
                    user_font_size: "25sp"
                    pos_hint:{"center_x":0.9,"center_y":0.15}
                    on_press: app.add_task_page()     
                       
            Screen:
                name: "Add"
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Add"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                    Widget:
            Screen:
                name: "Add task"
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        size_hint_x: 1
                        size_hint_y: None
                        title: "Add task"
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                        size:(20, 20)
                    Widget:
            Screen:
                name:"Change color"    
            Screen:
                name: "Cài đặt"
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Cài đặt"
                        elevation: 10
                        right_action_items: [["dots-vertical", lambda x: app.callback(x)]]
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                    Widget:
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                screen_manager: screen_manager
                id: content_drawer        
    
'''


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''


class ContentNavigationDrawer(BoxLayout):
    pass


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Todo(MDApp):
    data = {
        "language-python": "add",
    }
    list_task = {"task 1": ['abc', 'dgf', 'hik'],
                 "task 2": ['ee', 'ik', 'ok'],
                 "task 3": ['ee3', 'ik3', 'o3k']}

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def on_start(self):
        icons_item = {
            "home": "Home",
            "plus": "Add task",
            "settings": "Cài đặt",
            "palette": "Change color"
        }
        for task, subtask in self.list_task.items():
            self.root.ids.android_tabs.add_widget(Tab(text=f"{task}"))
        for key, val in self.root.ids.android_tabs.ids.items():
            print("key={0}, val={1}".format(key, val))
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        instance_tab.ids.scroll.clear_widgets()
        for task, subtask in self.list_task.items():
            for i in subtask:
                if(tab_text == task):
                    instance_tab.ids.scroll.add_widget(
                        ListItemWithCheckbox(text=f"{i}"))

    def add_tab(self):
        self.index += 1
        self.root.ids.tabs.add_widget(Tab(text=f"{self.index} tab"))

    def remove_tab(self):
        if self.index > 1:
            self.index -= 1
        self.root.ids.tabs.remove_widget(
            self.root.ids.tabs.get_tab_list()[-1]
        )


Todo().run()
