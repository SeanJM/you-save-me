import sublime_plugin, os, json, subprocess, sys, fnmatch

config_names = [ ".yousaveme", ".yousaveme.json" ]

class YouSaveMe(sublime_plugin.EventListener):
    def get_config_by_fnmatch(self, config_list, file_name):
        config_match = []

        for config in config_list:
            included = True
            excluded = False

            if "include" in config:
                included = fnmatch.fnmatch(file_name, config["include"])

            if "exclude" in config:
                excluded = fnmatch.fnmatch(file_name, config["exclude"])

            if (included == True) and (excluded == False):
                config_match.append(config)

        return config_match

    def apply_config(self, project_directory, config_list, file_name):
        config_matches = self.get_config_by_fnmatch(config_list, file_name)
        for config in config_matches:
            command = config["command"];
            command = command.replace("$filename", file_name).replace("$project", project_directory)
            command = "cd {0} && {1}".format(project_directory, command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in process.stdout.readlines():
                print(line.rstrip().decode('utf-8'))
                sys.stdout.flush()

    def load_config(self, config_filename):
        with open(config_filename, "r") as readfile:
            config_string = readfile.read()
            return json.loads(config_string)

    def run_tasks(self, project_directory, file_name):
        for config_name in config_names:
            config_filename = os.path.join(project_directory, config_name)
            if os.path.isfile(config_filename):
                config_list = self.load_config(config_filename)
                self.apply_config(project_directory, config_list, file_name)
                break

    def on_post_save(self, view):
        file_name = view.file_name()
        project_data = view.window().project_data()
        folders = project_data["folders"]
        matching_projects = list(filter(lambda x: file_name.startswith(x["path"]), folders))

        if len(matching_projects) > 0:
            self.run_tasks(matching_projects[0]["path"], file_name)
