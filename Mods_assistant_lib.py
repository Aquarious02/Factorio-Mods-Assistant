import json
import os


class ModsHandler:
    def __init__(self, mods_path: str = None, mods_file_path: str = None):
        try:
            self.mods = {}
            self.mods_path = mods_path or fr'{os.environ["appdata"]}\Factorio\mods'
            self._mods_file_path = mods_file_path or self.mods_path + r'\mod-list.json'
            self.update_mods()
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
        self.update_mods()

    @staticmethod
    def mods_list_to_dict(list_from_mods_file) -> dict:
        """
        Returns dict of mods with pairs: "mod_name": enabled(bool)
        :return:
        """
        mods_names = {}
        for mod in list_from_mods_file:
            mods_names[mod['name']] = mod['enabled']
        return mods_names

    @staticmethod
    def mods_dict_to_list(dict_with_mods) -> list:
        """
        Creates list of mods to save in .json.
        :return: [{"name": "mod1", "enabled": true}, {"name": "mod2", "enabled": false}, ...]
        """
        mods = []
        for mod_name, mod_state in dict_with_mods.items():
            mods.append({'name': mod_name, 'enabled': mod_state})
        return mods

    def update_mods(self):
        """
        Updates mods from file
        """
        if self.mods_file_path is not None:
            with open(self.mods_file_path, 'r') as f:
                self.mods = self.mods_list_to_dict(json.load(f)['mods'])
        else:
            raise FileNotFoundError

    @staticmethod
    def open_json(file_path: str) -> list:
        """
        Opens json file
        :param file_path: open file with path from handler if None
        :return: json file in list
        """
        with open(file_path, 'r') as f:
            mods = json.load(f)['mods']
        return mods

    def save_mods(self, file_path: str = None, file_name: str = None):
        """
        saves mods in .json file
        """
        file_path = file_path or self.mods_file_path
        if file_name is not None:
            file_path = file_path.replace('mod-list', file_name)

        with open(file_path, 'w') as f:
            json.dump({'mods': self.mods_dict_to_list(self.mods)}, f)

    def make_base(self):
        """
        Turn off all modes to load faster. Creates "mod-list-initial" - copy of current state of mods-list
        """
        self.save_mods(file_name='mod-list-initial')
        for mod in self.mods:
            if mod['name'] != 'base' and mod['enabled']:
                mod['enabled'] = False

        self.save_mods(file_name='mod-list')

    def merge_modes(self):
        """
        Merge new modes with 'initial'
        :return:
        """
        new_modes = self.open_json()
        old_modes_names = self.mods_dict
        for new_mode in new_modes:
            if new_mode['name'] not in old_modes_names:
                self.mods.append({new_mode['name']: new_mode['enabled']})

        self.save_mods(file_name='mod-list')
