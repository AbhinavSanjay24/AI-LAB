# --------- FORWARD REASONING / FORWARD CHAINING ----------

# Knowledge Base: facts and rules
facts = [
    ("Human", "Socrates"),
    ("Human", "Plato"),
    ("Man", "Socrates")
]

# Rules represented as: (premises, conclusion)
rules = [
    ([("Human", "?x")], ("Mortal", "?x")),           # If Human(x) then Mortal(x)
    ([("Man", "?x")], ("Human", "?x")),             # If Man(x) then Human(x)
]

# Check if predicate matches with substitution
def match(pattern, fact):
    if pattern[0] != fact[0]:
        return None
    subst = {}
    for p_arg, f_arg in zip(pattern[1:], fact[1:]):
        if p_arg.startswith("?"):
            subst[p_arg] = f_arg
        elif p_arg != f_arg:
            return None
    return subst

# Apply substitution to a predicate
def substitute(pred, subst):
    return tuple(subst.get(arg, arg) for arg in pred)

# Forward chaining reasoning
def forward_reasoning(query):
    inferred = set(facts)
    added = True
    steps = []

    while added:
        added = False

        for premises, conclusion in rules:
            for fact in list(inferred):
                subst = match(premises[0], fact)
                if subst is not None:
                    new_fact = substitute(conclusion, subst)

                    if new_fact not in inferred:
                        inferred.add(new_fact)
                        steps.append((premises[0], new_fact))
                        if new_fact == query:
                            return True, steps

    return False, steps


# -------- MAIN TEST ---------

# Query to prove
query = ("Mortal", "Socrates")

proven, steps = forward_reasoning(query)

print("Knowledge Base Facts:")
for f in facts:
    print(" ", f)

print("\nReasoning Steps:")
for p, c in steps:
    print(f"From {p} infer {c}")

print("\nQuery:", query)

if proven:
    print("✅ RESULT: Query is proven using forward reasoning!")
else:
    print("❌ RESULT: Query cannot be proven.")
