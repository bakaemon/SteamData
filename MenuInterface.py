import types


class MenuInterface:
    def __init__(self):
        self._OPTIONS = []

    def add(self, name: str, action):
        instance = {"name": name, "action": action}
        self._OPTIONS.append(instance)
        return self

    def remove(self, name: str = "", action=None):
        if name:
            for option in self._OPTIONS:
                if option["name"] == name:
                    del self._OPTIONS[self._OPTIONS.index(option)]
        elif callable(action):
            for option in self._OPTIONS:
                if option["action"] == action:
                    del self._OPTIONS[self._OPTIONS.index(option)]
        return self

    def options(self):
        return [x["name"] for x in self._OPTIONS]

    def call(self, position=None, name: str = "", parameters=None):
        if parameters is None:
            parameters = {}
        if name:
            for option in self._OPTIONS:
                if option["name"] == name:
                    return option["action"](**parameters)
        elif isinstance(position, int):
            return self._OPTIONS[position]["action"](**parameters)
