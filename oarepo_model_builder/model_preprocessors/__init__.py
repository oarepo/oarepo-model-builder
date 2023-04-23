from collections import namedtuple


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
        arr = container.get(key)
        if appended not in arr:
            arr.append(appended)

    def set_default_and_prepend_if_not_present(self, container, key, value, prepended):
        container.setdefault(key, value)
        arr = container.get(key)
        if prepended not in arr:
            arr.insert(0, prepended)


TSE = namedtuple("TransformStackEntry", "before_transform, key, data, extra_data")


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
        build_stack = [
            TSE(
                before_transform=True,
                key=None,
                data=self.schema.current_model,
                extra_data=None,
            )
        ]
        while build_stack:
            top = build_stack.pop()
            if top.before_transform:
                stack.push(top.key, top.data)
                extra_data_to_transform = self.transform_node(stack, top.data)
                build_stack.append(
                    TSE(
                        before_transform=False,
                        key=top.key,
                        data=top.data,
                        extra_data=extra_data_to_transform,
                    )
                )

                if isinstance(top.data, dict):
                    # process children in alphabetical order to be deterministic
                    # - need to reverse as pushing into stack
                    for c in reversed(sorted(top.data.items())):
                        build_stack.append(
                            TSE(
                                before_transform=True,
                                key=c[0],
                                data=c[1],
                                extra_data=None,
                            )
                        )
            else:
                extra_data_to_transform = self.after_transform_node(stack, top.data)
                stack.pop()
                if top.extra_data:
                    build_stack.append(
                        TSE(
                            before_transform=True,
                            key=top.key,
                            data=top.extra_data,
                            extra_data=None,
                        )
                    )

                if extra_data_to_transform:
                    # transform extra data before continuing
                    build_stack.append(
                        TSE(
                            before_transform=True,
                            key=top.key,
                            data=extra_data_to_transform,
                            extra_data=None,
                        )
                    )

    def transform_node(self, stack, data):
        """Called on node before children are transformed. To be implemented in inherited class."""

    def after_transform_node(self, stack, data):
        """Called on node after children are transformed. To be implemented in inherited class."""
