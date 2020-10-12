import json
import os


class Mods:
    def __init__(self, mods_file_path: str = ''):
        self.mods_path = mods_file_path if mods_file_path != '' else fr'{os.environ["appdata"]}\Factorio\mods'
        self.mods_path += r'\mod-list.json'
        self.mods = self.open_json()

    @property
    def mods_names(self):
        """
        Returns dict of mod with pair "mod_name": enabled(bool)
        :return:
        """
        mods_names = {}
        for mod in self.mods:
            mods_names[mod['name']] = mod['enabled']
        return mods_names

    def open_json(self, file_path: str = '') -> list:
        """
        Opens json file
        :param file_path:
        :return: json file in list
        """
        file_path = self.mods_path if file_path == '' else file_path
        with open(file_path, 'r') as f:
            mods = json.load(f)['mods']
        return mods

    def save_json(self, file_path: str ='', file_name: str='mod-list_new'):
        """
        saves .json file
        """
        file_path = self.mods_path if file_path == '' else file_path
        file_path = file_path.replace('mod-list', file_name)

        with open(file_path, 'w') as f:
            json.dump({'mods': self.mods}, f)

    def make_base(self):
        """
        Turn of all modes to load faster
        :return:
        """

        self.save_json(file_name='mod-list-initial')
        for mod in self.mods:
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


if __name__ == '__main__':
    my_mods = Mods()
    my_mods.make_base()
    pass