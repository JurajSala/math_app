from sympy import symbols
from sympy.combinatorics.fp_groups import (
    free_group, FpGroup, coset_enumeration_c
)


def enumerate_finite_group(generators, relators, max_cosets=10000):
    print(f">>> enumerate_finite_group called with generators={generators}, relators={relators}")
    """
    Enumerate a finite group given by a presentation <generators | relators> using
    the Todd–Coxeter coset enumeration algorithm (via Sympy).

    generators: list[str] e.g. ['a','b']
    relators:  list[str] using '^' or '**' syntax, e.g. ['a^3', 'b^2', 'b*a*b*a']
    max_cosets: int, safety limit for cosets (to avoid non-termination)

    Returns:
      elements: list[str] canonical words for each group element
      table: dict[(str,str), str] multiplication table mapping (e1,e2)->e3
    """
    _fg  = free_group(','.join(generators))
    F    = _fg[0]            # FreeGroup factory
    gens = list(_fg[1:])     # generator symbols

    # 2) Prepare symbol map for eval
    symbol_map = {str(g): g for g in gens}
    # map inverses by uppercase
    for g in gens:
        symbol_map[str(g).upper()] = g**-1
    # map identity symbol 'e' (and 'E') to the trivial coset (identity)
    identity = gens[0]**0  # free_group symbol**0 yields identity element
    symbol_map['e'] = identity  # <<< FIX: allow 'e' as identity
    symbol_map['E'] = identity

    # 3) Parse relators
    rels = []
    for r in relators:
        raw = r.strip()
        raw = raw.replace('^', '**')
        if '=' in raw:
            # support 'lhs = rhs' → lhs*(rhs)^(-1)
            lhs, rhs = (side.strip() for side in raw.split('=', 1))
            lhs_expr = '*'.join(lhs.split())
            rhs_expr = '*'.join(rhs.split())
            expr = f"({lhs_expr})*({rhs_expr})**(-1)"
        else:
            # Sympy power syntax and explicit multiplication
            expr = raw.replace(' ', '*')
        try:
            rel_elem = eval(expr, {}, symbol_map)
        except Exception as e:
            raise ValueError(f"Error parsing relator '{r}' → '{expr}': {e}")
        rels.append(rel_elem)

    # 4) Create presented group
    G = FpGroup(F, rels)

    # 5) Enumerate cosets of trivial subgroup to get group order
    C = coset_enumeration_c(G, [])
    # Sympy's CosetTable may not have 'coset_max'; try alternative attribute
    maxc = getattr(C, 'coset_max', None) or getattr(C, 'ncosets', None) or len(C.table)
    if maxc > max_cosets:
        raise ValueError(f"Too many cosets ({maxc}); group may be infinite or presentation too large.")

    # 6) Extract canonical representatives
        # C.table is list of canonical representatives
    reps = getattr(C, '_coset_reps', None) or getattr(C, 'coset_reps', None)
    if reps is not None:
        elements = [str(reps[i]) for i in range(len(reps))]
    else:
        # fallback: C.table rows (generator action table)
        elements = [str(rep) for rep in C.table]
    order = len(elements)

    # 7) Build multiplication table (skip if coset_mul unavailable)
    table = { e1: {} for e1 in elements }
    if hasattr(C, 'coset_mul'):
        for i, e1 in enumerate(elements):
            for j, e2 in enumerate(elements):
                prod_idx = C.coset_mul(i, j)
                # pokud je index v rozsahu, vezmi přímo prvek, jinak fallback
                rep = elements[prod_idx] if prod_idx < len(elements) else tuple(C.table[prod_idx])
                table[e1][e2] = rep
        print(table)

    return elements, table
