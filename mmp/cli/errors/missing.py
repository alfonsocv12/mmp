class MissingFiles(Exception):
    def __init__(self, file_name):
        super().__init__("Missing File: %s" % file_name)

        self.file = file_name

class MissingValue(Exception):
    def __init__(self, file_name, value_name):
        super().__init__(f"Missing value on file {file_name}: {value_name}")

        self.file_name = file_name
        self.value_name = value_name

class NotSuchScript(Exception):
    def __init__(self, script_name):
        super().__init__(f"Not such script: {script_name}")

        self.script_name = script_name
