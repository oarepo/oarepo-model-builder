import lazy_object_proxy
from libcst import ClassDef, FunctionDef, Import, ImportFrom, Assign, Expr, \
    Element, Pass, Call, Module, List, Tuple, Integer, Arg


@lazy_object_proxy.Proxy
def general_mergers():
    from .indented_nodes import ModuleMerger, ClassMerger
    from .simple_nodes import AssignMerger, ImportMerger, ImportFromMerger, ExprMerger, FunctionMerger, PassMerger

    return {
        Module: ModuleMerger(),
        ClassDef: ClassMerger(),
        Assign: AssignMerger(),
        Import: ImportMerger(),
        ImportFrom: ImportFromMerger(),
        Expr: ExprMerger(),
        FunctionDef: FunctionMerger(),
        Pass: PassMerger()
    }


@lazy_object_proxy.Proxy
def call_mergers():
    from .call import ArgMerger
    return {
        Arg: ArgMerger()
    }


@lazy_object_proxy.Proxy
def expression_mergers():
    from .call import CallMerger
    from .simple_nodes import ListMerger, IntegerMerger, ElementMerger, ExprMerger
    return {
        Call: CallMerger(),
        List: ListMerger(),
        Tuple: ListMerger(),
        Integer: IntegerMerger(),
        Element: ElementMerger(),
        Expr: ExprMerger()
    }
