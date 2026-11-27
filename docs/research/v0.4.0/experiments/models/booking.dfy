// Handwritten experimental implementation contract; not generated from prose.
method Reserve(used: int, capacity: int) returns (next: int)
  requires 0 <= used < capacity
  ensures next == used + 1
  ensures 0 <= next <= capacity
{ next := used + 1; }

method Release(used: int, capacity: int) returns (next: int)
  requires 0 < used <= capacity
  ensures next == used - 1
  ensures 0 <= next <= capacity
{ next := used - 1; }

method ReserveMutant(used: int, capacity: int) returns (next: int)
  requires 0 <= used < capacity
  ensures 0 <= next <= capacity
{ next := used + 2; }
