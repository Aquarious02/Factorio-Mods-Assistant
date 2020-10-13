import json
import os


class ModsHandler:
    def __init__(self, mods_path: str = None, mods_file_path: str = None):
        try:
            self.mods_path = mods_path or fr'{os.environ["appdata"]}\Factorio\mods'
            self._mods_file_path = mods_file_path or self.mods_path + r'\mod-list.json'
            self.mods = {'current': self.open_json()}
        except FileNotFoundError:
            self.mods_path, self._mods_file_path = None, None
            print("Can't find mods in AppData...")

    @property
    def mods_file_path(self):
        return self._mods_file_path

    @mods_file_path.setter
    def mods_file_path(self, value):
        header, tail = os.path.split(value)

        if self.mods_path is None:
            self.mods_path = header
        self._mods_file_path = value




    @property
    def mods_names(self):
        """
        Returns dict of mod with pair "mod_name": enabled(bool)
        :return:
        """
        mods_names = {}
        for mod in self.mods['current']:
            mods_names[mod['name']] = mod['enabled']
        return mods_names

    def open_json(self, file_path: str = None) -> list:
        """
        Opens json file
        :param file_path:
        :return: json file in list
        """
        file_path = file_path or self.mods_file_path
        with open(file_path, 'r') as f:
            mods = json.load(f)['mods']
        return mods

    def save_json(self, file_path: str = None, file_name: str = 'mod-list_new'):
        """
        saves .json file
        """
        file_path = file_path or self.mods_file_path
        file_path = file_path.replace('mod-list', file_name)

        with open(file_path, 'w') as f:
            json.dump({'mods': self.mods}, f)

    def make_base(self):
        """
        Turn off all modes to load faster. Creates "mod-list-initial" - copy of current state of mods-list
        """
        self.save_json(file_name='mod-list-initial')
        for mod in self.mods['current']:
            if mod['name'] != 'base' and mod['enabled']:
                mod['enabled'] = False

        self.save_json(file_name='mod-list')

    def merge_modes(self):
        """
        Merge new modes with 'initial'
        :return:
        """
        new_modes = self.open_json()
        old_modes_names = self.mods_names
        for new_mode in new_modes:
            if new_mode['name'] not in old_modes_names:
                self.mods.append({new_mode['name']: new_mode['enabled']})

        self.save_json(file_name='mod-list')


