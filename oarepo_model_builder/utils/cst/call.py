import itertools

from libcst import Arg

from .common import IdentityMerger, MergerBase, PythonContext, merge
from .mergers import call_mergers, expression_mergers


class CallMerger(MergerBase):
    def identity(self, context: PythonContext, node):
        return node.func

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        existing_args, existing_kwargs = self.extract_args(existing_node)
        new_args, new_kwargs = self.extract_args(new_node)
        args = []
        merger = ArgMerger()
        for e, n in itertools.zip_longest(existing_args, new_args):
            args.append(merger.merge(context, e, n))

        for k, e in existing_kwargs.items():
            n = new_kwargs.pop(k, None)
            args.append(merger.merge(context, e, n))

        for k, n in new_kwargs.items():
            args.append(merger.merge(context, None, n))

        args = [x for x in args if x is not context.REMOVED]

        return existing_node.with_changes(args=args)

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
    def identity(self, context: PythonContext, node):
        return node

    def merge_internal(self, context: PythonContext, existing_node, new_node):
        existing_value = existing_node.value
        new_value = new_node.value
        merger = expression_mergers.get(type(existing_value), IdentityMerger())
        merged_value = merger.merge(context, existing_value, new_value)
        return existing_node.with_changes(value=merged_value)
