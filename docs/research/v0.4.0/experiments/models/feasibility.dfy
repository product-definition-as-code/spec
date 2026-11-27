method Good(x: int) returns (y: int)
  ensures y > x
{ y := x + 1; }

method DeliberatelyFalse(x: int) returns (y: int)
  ensures y > x
{ y := x; }
