"""
Tools for indexing docs by tag (taxonomy).
"""
from lettersmith import util
from datetime import datetime
from lettersmith import path as pathtools
from lettersmith.doc import doc


_EMPTY_TUPLE = tuple()
DEFAULT_TAXONOMIES = ("tags",)
ARCHIVE_PATH_TEMPLATE = "{taxonomy}/{term}/all/index.html"


def items_with_keys(d, keys):
    """
    Yield item pairs with keys matching `keys`.
    """
    for key, value in d.items():
        if key in keys:
            yield key, value


def gen_taxonomy_archives(docs,
    output_path_template=None,
    taxonomies=None, templates=_EMPTY_TUPLE):
    """
    Creates a full archive page for each taxonomy term. One page per term.
    """
    output_path_template = output_path_template or ARCHIVE_PATH_TEMPLATE
    tax_index = index_by_taxonomy(docs, taxonomies)
    for taxonomy, terms in tax_index.items():
        for term, docs in terms.items():
            output_path = output_path_template.format(
                taxonomy=pathtools.to_slug(taxonomy),
                term=pathtools.to_slug(term)
            )
            tax_templates = (
                "taxonomy/{}/all.html".format(taxonomy),
                "taxonomy/{}/list.html".format(taxonomy),
                "taxonomy/all.html",
                "taxonomy/list.html",
                "list.html"
            )
            meta = {"docs": docs}
            yield doc(
                id_path=output_path,
                output_path=output_path,
                created=datetime.now(),
                modified=datetime.now(),
                title=term,
                section=taxonomy,
                templates=templates + tax_templates,
                meta=meta
            )


def index_by_taxonomy(docs, taxonomies=DEFAULT_TAXONOMIES):
    """
    Create a new index by taxonomy.
    `taxonomies` is an indexable whitelist of meta keys that should
    be treated as taxonomies.

    Returns a dict that looks like:

        {
            "tags": {
                "term_a": [doc, ...],
                "term_b": [doc, ...]
            }
        }
    """
    tax_index = {}
    for doc in docs:
        for tax, terms in items_with_keys(doc.meta, taxonomies):
            if not tax_index.get(tax):
                tax_index[tax] = {}
            for term in terms:
                if not tax_index[tax].get(term):
                    tax_index[tax][term] = []
                tax_index[tax][term].append(doc)
    return tax_index