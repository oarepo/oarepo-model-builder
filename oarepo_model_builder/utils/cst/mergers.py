import lazy_object_proxy
from libcst import ClassDef, FunctionDef, Import, ImportFrom, Assign, Expr, \
    Element, Pass, Call, Module, List, Tuple, Integer, Arg, SimpleStatementLine


@lazy_object_proxy.Proxy
def module_mergers():
    from .indented_nodes import ModuleMerger
    return {
        Module: ModuleMerger()
    }


@lazy_object_proxy.Proxy
def indented_block_mergers():
    from .indented_nodes import ClassMerger
    from .simple_nodes import SimpleStatementLineMerger, FunctionMerger

    return {
        SimpleStatementLine: SimpleStatementLineMerger(),
        ClassDef: ClassMerger(),
        FunctionDef: FunctionMerger(),
    }


@lazy_object_proxy.Proxy
def simple_line_mergers():
    from .simple_nodes import AssignMerger, ImportMerger, ImportFromMerger, ExprMerger, PassMerger

    return {
        Assign: AssignMerger(),
        Import: ImportMerger(),
        ImportFrom: ImportFromMerger(),
        Expr: ExprMerger(),
        Pass: PassMerger(),
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
