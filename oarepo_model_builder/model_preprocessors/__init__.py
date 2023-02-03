class ModelPreprocessor:
    def __init__(self, builder: "oarepo_model_builder.builder.ModelBuilder"):
        self.builder = builder

    def transform(self, schema, settings):
        pass

    def set(self, settings, name, callable=None):
        if callable:
            if not settings.get(name):
                settings[name] = callable()
            return

        def w(func):
            if not settings.get(name):
                settings[name] = func()

        return w

    def set_default_and_append_if_not_present(self, container, key, value, appended):
        container.setdefault(key, value)
        arr = getattr(container, key)
        if appended not in arr:
            arr.append(appended)

    def set_default_and_prepend_if_not_present(self, container, key, value, prepended):
        container.setdefault(key, value)
        arr = getattr(container, key)
        if prepended not in arr:
            arr.insert(0, prepended)
