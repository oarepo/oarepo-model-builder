from collections import namedtuple

from oarepo_model_builder.stack.stack import ModelBuilderStack


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


TSE = namedtuple("TransformStackEntry", "before_transform, key, data")


class DeepTransformationModelPreprocessor(ModelPreprocessor):
    def transform(self, schema, settings):
        self.begin(schema, settings)
        self.deep_transform()
        self.end()

    def begin(self, schema, settings):
        self.schema = schema
        self.settings = settings

    def end(self):
        """Extensibility point called after the processing has ended"""

    def deep_transform(self):
        stack = ModelBuilderStack()
        build_stack = [
            TSE(before_transform=True, key=None, data=self.schema.current_model)
        ]
        while build_stack:
            top = build_stack.pop()
            if top.before_transform:
                stack.push(top.key, top.data)
                self.transform_node(stack, top.data)
                build_stack.append(
                    TSE(before_transform=False, key=top.key, data=top.data)
                )
                if isinstance(top.data, dict):
                    # process children in alphabetical order to be deterministic
                    # - need to reverse as pushing into stack
                    for c in reversed(sorted(top.data.items())):
                        build_stack.append(
                            TSE(before_transform=True, key=c[0], data=c[1])
                        )
            else:
                self.after_transform_node(stack, top.data)
                stack.pop()

    def transform_node(self, stack, data):
        """Called on node before children are transformed. To be implemented in inherited class."""

    def after_transform_node(self, stack, data):
        """Called on node after children are transformed. To be implemented in inherited class."""
