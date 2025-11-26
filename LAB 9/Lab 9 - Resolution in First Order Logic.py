# ---------- UNIFICATION + RESOLUTION IN FOL ----------

# Check if a variable
def is_var(x):
    return isinstance(x, str) and x.startswith("?")

# Unify two literals
def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if x == y:
        return subst
    if is_var(x):
        subst[x] = y
        return subst
    if is_var(y):
        subst[y] = x
        return subst
    if isinstance(x, tuple) and isinstance(y, tuple) and x[0] == y[0]:
        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None

# Apply substitution
def substitute(literal, subst):
    if not subst:
        return literal
    pred = literal[0]
    args = []
    for a in literal[1:]:
        args.append(subst.get(a, a))
    return (pred,) + tuple(args)

# Resolution step
def resolve(c1, c2):
    resolvents = []
    for l1 in c1:
        for l2 in c2:
            # Check complementary literals
            if l1[0] == "~" + l2[0] or l2[0] == "~" + l1[0]:
                subst = unify(l1[1:], l2[1:])
                if subst is not None:
                    new_clause = set(
                        substitute(l, subst) for l in (c1 | c2)
                        if l != l1 and l != l2
                    )
                    resolvents.append(frozenset(new_clause))
    return resolvents


# ---------- KNOWLEDGE BASE ----------

# CNF clauses represented as sets of literals
# Predicates stored as tuples: ("P", "a"), ("~P", "a")

KB = [
    frozenset({("~Human", "Socrates"), ("Mortal", "Socrates")}),
    frozenset({("~Man", "Socrates"), ("Human", "Socrates")}),
    frozenset({("Man", "Socrates")})
]

# Query
query = ("Mortal", "Socrates")

# Add negated query
KB.append(frozenset({("~Mortal", "Socrates")}))


# ---------- RESOLUTION PROCEDURE ----------

def resolution(KB):
    new = set()

    while True:
        pairs = [(KB[i], KB[j]) for i in range(len(KB)) for j in range(i+1, len(KB))]

        for (c1, c2) in pairs:
            resolvents = resolve(c1, c2)
            if frozenset() in resolvents:
                return True
            new.update(resolvents)

        if new.issubset(KB):
            return False

        for clause in new:
            if clause not in KB:
                KB.append(clause)


# ---------- MAIN ----------

print("\nKnowledge Base Clauses:")
for c in KB:
    print(" ", c)

result = resolution(KB)

print("\nQuery:", query)

if result:
    print("✅ RESULT: Query is proven by Resolution (empty clause derived)!")
else:
    print("❌ RESULT: Query cannot be proven.")
