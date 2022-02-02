from typing import Literal

from .utils.cst import ConflictResolution, ConflictResolver, PythonContext

resolution_mapping = {
    "e": ConflictResolution.KEEP_PREVIOUS,
    "n": ConflictResolution.KEEP_NEW,
    "m": ConflictResolution.KEEP_MERGED,
    "r": ConflictResolution.REMOVE,
    "t": ConflictResolution.NEW_AS_TODO,
}


class InteractiveResolver(ConflictResolver):
    def __init__(self, debug: bool):
        self.debug = debug

    def resolve_conflict(self, context: PythonContext, existing_node, new_node, merged_node) -> ConflictResolution:
        if not self.debug:
            if existing_node and not new_node:
                return ConflictResolution.KEEP_PREVIOUS
            if new_node:
                return ConflictResolution.KEEP_NEW
        if existing_node:
            if new_node:
                print("Conflict detected, please decide")
                print("--------------------------------")
                print("Existing node:")
                print(context.to_source_code(existing_node).strip())
                print("New node:")
                print(context.to_source_code(new_node).strip())
                print("Will be merged to:")
                print(context.to_source_code(merged_node).strip())
                print("--------------------------------")

                print("Your decision: ")
                print("   m or enter to keep the merged value")
                print("   e  to keep the existing value")
                print("   n  to keep the new value")
                print("   t  to keep the previous value and add the new value as TODO comment")
                while True:
                    inp = input().strip()
                    if inp in resolution_mapping:
                        return resolution_mapping[inp]
                    elif inp == "":
                        return ConflictResolution.KEEP_MERGED
                    print("Unknown decision")
            else:
                print("Removal detected, please decide")
                print("--------------------------------")
                print("Existing node:")
                print(context.to_source_code(existing_node).strip())
                print("--------------------------------")

                print("Your decision: ")
                print("   e or enter to keep the existing value")
                print("   r  to remove the existing value")
                while True:
                    inp = input().strip()
                    if inp in resolution_mapping:
                        return resolution_mapping[inp]
                    elif inp == "":
                        return ConflictResolution.KEEP_PREVIOUS
                    print("Unknown decision")
        else:
            if new_node:
                print("Addition detected, please decide")
                print("--------------------------------")
                print("New node:")
                print(context.to_source_code(new_node).strip())
                print("--------------------------------")

                print("Your decision: ")
                print("   n or enter to keep the new value")
                print("   t  to keep the previous value and add the new value as TODO comment")
                while True:
                    inp = input().strip()
                    if inp in resolution_mapping:
                        return resolution_mapping[inp]
                    elif inp == "":
                        return ConflictResolution.KEEP_NEW
                    print("Unknown decision")
        return ConflictResolution.KEEP_MERGED


class AutomaticResolver(ConflictResolver):
    def __init__(self, resolution_type: Literal["replace", "keep", "comment"]):
        self.resolution_type = resolution_type

    def resolve_conflict(self, context, existing_node, new_node, merged_node) -> ConflictResolution:
        if existing_node:
            if new_node:
                match self.resolution_type:
                    case "replace":
                        return ConflictResolution.KEEP_NEW
                    case "keep":
                        return ConflictResolution.KEEP_PREVIOUS
                    case "comment":
                        return ConflictResolution.NEW_AS_TODO
            else:
                return ConflictResolution.KEEP_PREVIOUS
        else:
            if new_node:
                return ConflictResolution.KEEP_NEW
        return ConflictResolution.KEEP_MERGED
