import sys
import os
import subprocess


class VirtualEnv:
    def __init__(self):
        self.venv_folder_name = 'venv'
        self.script_folder = os.path.join(sys.path[0])
        self.venv_folder_path = os.path.join(self.script_folder, self.venv_folder_name)

    def __enter__(self):
        self.init_venv()
        # venv_activate_cmd = os.path.join(self.venv_folder_path, 'bin', 'activate')
        # self.run_cmd(venv_activate_cmd, cmd_folder=self.script_folder, shell=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # venv_deactivate_cmd = os.path.join('deactivate')
        # self.run_cmd(venv_deactivate_cmd, cmd_folder=self.script_folder, shell=True)

    @staticmethod
    def run_cmd(input_cmd, cmd_folder='.', shell=True):
        return subprocess.run(input_cmd,
                              shell=shell,
                              stdout=subprocess.PIPE,
                              encoding='utf-8',
                              cwd=cmd_folder).stdout

    def init_venv(self):
        def pip_upgrade(target_script_folder, target_venv_folder_path):
            venv_activate_path = os.path.join(target_venv_folder_path, 'bin', 'activate')
            pip_install_cmd = f'. {venv_activate_path} && pip install -r requirements.txt && deactivate'
            self.run_cmd(pip_install_cmd, cmd_folder=target_script_folder, shell=True)

        # create venv if not exist
        if not os.path.isdir(self.venv_folder_path):
            venv_setup_script = f'python -m venv {self.venv_folder_path}'
            subprocess.run(venv_setup_script, shell=True)

        pip_upgrade(self.script_folder, self.venv_folder_path)
