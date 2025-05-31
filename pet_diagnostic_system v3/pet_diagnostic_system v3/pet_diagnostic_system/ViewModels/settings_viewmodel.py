import os
import json

class SettingsViewModel:
    def __init__(self, main_app=None):
        self.main_app = main_app
        self.settings_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'data', 'settings.json')
        )
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"theme": "light"}

    def save_settings(self, theme):
        self.settings["theme"] = theme
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def apply_theme(self, theme):
        if self.main_app:
            self.main_app.apply_theme(theme)

    def navigate_to(self, index):
        if self.main_app:
            self.main_app.navigate_to(index)
