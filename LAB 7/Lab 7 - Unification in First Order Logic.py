# ---------- UNIFICATION IN FIRST ORDER LOGIC ----------

# Check if a symbol is a variable
def is_variable(x):
    return isinstance(x, str) and x.startswith("?")

# Check if term is compound (e.g., ("f", "a", "?x"))
def is_compound(x):
    return isinstance(x, tuple) and len(x) > 1

# Occur check (prevents infinite recursive substitutions)
def occur_check(var, term, subst):
    if var == term:
        return True
    if is_variable(term) and term in subst:
        return occur_check(var, subst[term], subst)
    if is_compound(term):
        return any(occur_check(var, arg, subst) for arg in term[1:])
    return False

# Apply substitution to a term
def substitute(term, subst):
    if is_variable(term):
        while is_variable(term) and term in subst:
            term = subst[term]
        return term
    if is_compound(term):
        return (term[0],) + tuple(substitute(a, subst) for a in term[1:])
    return term

# Unification algorithm
def unify(x, y, subst=None):
    if subst is None:
        subst = {}

    x = substitute(x, subst)
    y = substitute(y, subst)

    if x == y:
        return subst
    if is_variable(x):
        if occur_check(x, y, subst):
            return None
        subst[x] = y
        return subst
    if is_variable(y):
        if occur_check(y, x, subst):
            return None
        subst[y] = x
        return subst
    if is_compound(x) and is_compound(y) and x[0] == y[0] and len(x) == len(y):
        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None


# ---------- SAMPLE TEST CASES ----------

tests = [
    (("P", "?x"), ("P", "a")),
    (("P", "?x", "b"), ("P", "a", "?y")),
    (("f", "?x", ("g", "?x")), ("f", "a", "?y")),
    (("f", "?x"), ("f", ("g", "?x")))
]

print("\n=== SAMPLE UNIFICATION OUTPUT ===\n")
for t1, t2 in tests:
    result = unify(t1, t2, {})
    print(f"{t1}  ⟷  {t2}  =>  Substitution: {result}")
