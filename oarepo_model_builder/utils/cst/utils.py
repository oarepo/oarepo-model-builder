from oarepo_model_builder.utils.cst.common import IdentityMerger


def merge_lists_remove_duplicates(existing_list, new_list, context, mergers):
    ret = []
    new_list = [*new_list]

    for e in existing_list:
        for idx, n in enumerate(new_list):

            if type(e) is not type(n):
                continue

            merger = mergers.get(type(e), IdentityMerger())
            if merger.should_merge(context, e, n):
                ret.append(merger.merge(context, e, n))
                del new_list[idx]
                break
        else:
            ret.append(e)
    ret.extend(new_list)
    return ret