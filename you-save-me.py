import sublime, sublime_plugin, os, json, subprocess, sys

# Extends TextCommand so that run() receives a View to modify.
class YouSaveMe(sublime_plugin.EventListener):
    def get_config_by_filetype(self, config_list, filename_extension):
        return list(filter(lambda x: len(list(filter(lambda y: y == filename_extension, x["filetypes"]))) > 0, config_list))

    def apply_config(self, project_directory, config_list, file_name):
        filename_extension = os.path.splitext(file_name)[1][1:]
        config_matches = self.get_config_by_filetype(config_list, filename_extension)
        for config in config_matches:
            command = config["command"];
            command = command.replace("$filename", file_name).replace("$dir", project_directory)
            command = "cd {0} && {1}".format(project_directory, command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            returncode = process.wait()
            for line in process.stdout.readlines():
                print(line.rstrip().decode('utf-8'))
                sys.stdout.flush()

    def load_config(self, config_filename):
        with open(config_filename, "r") as readfile:
            config_string = readfile.read()
            return json.loads(config_string)

    def run_tasks(self, project_directory, file_name):
        config_filename = os.path.join(project_directory, ".yousaveme.json")
        if os.path.isfile(config_filename):
            config_list = self.load_config(config_filename)
            self.apply_config(project_directory, config_list, file_name)

    def on_post_save(self, view):
        file_name = view.file_name()
        project_data = view.window().project_data()
        folders = project_data["folders"]
        matching_projects = list(filter(lambda x: file_name.startswith(x["path"]), folders))

        if len(matching_projects) > 0:
            self.run_tasks(matching_projects[0]["path"], file_name)
