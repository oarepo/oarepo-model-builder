import itertools

from libcst import Arg

from .common import MergerBase, PythonContext, merge
from .mergers import call_mergers, expression_mergers


class CallMerger(MergerBase):
    def should_merge(self, context: PythonContext, existing_node, new_node):
        return existing_node.func.value == new_node.func.value

    def merge(self, context: PythonContext, existing_node, new_node):
        existing_args, existing_kwargs = self.extract_args(existing_node)
        new_args, new_kwargs = self.extract_args(new_node)
        args = []
        for e, n in itertools.zip_longest(existing_args, new_args):
            args.append(self.merge_arg(context, e, n))

        for k, e in existing_kwargs.items():
            n = new_kwargs.pop(k, None)
            args.append(self.merge_arg(context, e, n))

        for k, n in new_kwargs.items():
            args.append(n)

        return existing_node.with_changes(args=args)

    def merge_arg(self, context: PythonContext, e, n):
        if e and n:
            merged = self.check_and_merge(context, e, n, call_mergers)
            return merged or e
        return e or n

    def extract_args(self, n):
        args = []
        kwargs = {}
        for arg in n.args:
            if isinstance(arg, Arg):
                if arg.keyword:
                    kwargs[arg.keyword.value] = arg
                else:
                    args.append(arg)
            else:
                raise Exception(f"Unsupported clause in call args {type(arg)}")
        return args, kwargs


class ArgMerger(MergerBase):
    def should_merge(self, context: PythonContext, existing_node, new_node):
        # always merge with another arg
        return True

    def merge(self, context: PythonContext, existing_node, new_node):
        return existing_node.with_changes(
            value=merge(
                context, existing_node.value, new_node.value, mergers=expression_mergers
            )
            or existing_node.value
        )
