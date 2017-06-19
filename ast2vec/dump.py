from pprint import pprint

import asdf

from ast2vec.df import print_df
from ast2vec.nbow import print_nbow
from ast2vec.id2vec import print_id2vec
from ast2vec.repo2coocc import print_coocc


PRINTERS = {
    "nbow": print_nbow,
    "id2vec": print_id2vec,
    "docfreq": print_df,
    "co-occurrences": print_coocc
}


def dump_model(args):
    tree = asdf.open(args.input).tree
    meta = tree["meta"]
    pprint(meta)
    try:
        PRINTERS[meta["model"]](tree, args.dependency)
    except KeyError:
        pass
