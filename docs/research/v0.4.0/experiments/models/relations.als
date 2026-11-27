module relations
sig Node { next: set Node }
assert Acyclic { no n: Node | n in n.^next }
check Acyclic for exactly 3 Node
