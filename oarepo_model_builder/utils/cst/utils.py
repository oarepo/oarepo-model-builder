from oarepo_model_builder.utils.cst.common import real_node, IdentityMerger


def merge_lists_remove_duplicates(existing_list, new_list, cst, mergers):
    ret = []
    new_list = [*new_list]

    for e in existing_list:
        real_existing = real_node(e)

        for idx, n in enumerate(new_list):
            real_new = real_node(n)

            if type(real_existing) is not type(real_new):
                continue

            merger = mergers.get(type(real_existing), IdentityMerger())
            if merger.should_merge(cst, e, n):
                ret.append(merger.merge(cst, e, n))
                del new_list[idx]
                break
        else:
            ret.append(e)
    ret.extend(new_list)
    return ret