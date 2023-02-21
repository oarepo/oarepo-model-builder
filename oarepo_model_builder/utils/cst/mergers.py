import lazy_object_proxy
from libcst import (
    Arg,
    Assign,
    Call,
    ClassDef,
    Dict,
    Element,
    Expr,
    FunctionDef,
    Import,
    ImportFrom,
    Integer,
    List,
    Module,
    Name,
    Pass,
    SimpleStatementLine,
    SimpleString,
    StarredElement,
    Tuple,
)


@lazy_object_proxy.Proxy
def module_mergers():
    from .indented_nodes import ModuleMerger

    return {Module: ModuleMerger()}


@lazy_object_proxy.Proxy
def indented_block_mergers():
    from .indented_nodes import ClassMerger
    from .simple_nodes import FunctionMerger, SimpleStatementLineMerger

    return {
        SimpleStatementLine: SimpleStatementLineMerger(),
        ClassDef: ClassMerger(),
        FunctionDef: FunctionMerger(),
    }


@lazy_object_proxy.Proxy
def simple_line_mergers():
    from .simple_nodes import (
        AssignMerger,
        ExprMerger,
        ImportFromMerger,
        ImportMerger,
        PassMerger,
    )

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

    return {Arg: ArgMerger()}


@lazy_object_proxy.Proxy
def expression_mergers():
    from oarepo_model_builder.utils.cst.collections import (
        DictMerger,
        ElementMerger,
        ListMerger,
    )

    from .call import CallMerger
    from .simple_nodes import (
        ExprMerger,
        IntegerMerger,
        NameMerger,
        SimpleStringMerger,
        StarredElementMerger,
    )

    return {
        Call: CallMerger(),
        List: ListMerger(),
        Tuple: ListMerger(),
        Integer: IntegerMerger(),
        Element: ElementMerger(),
        SimpleString: SimpleStringMerger(),
        Name: NameMerger(),
        Expr: ExprMerger(),
        Dict: DictMerger(),
        StarredElement: StarredElementMerger(),
    }
