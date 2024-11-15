\* Problema exemplo *\

Minimize
 obj: + 4 x01 + 7 x13 + 5 x20 + 6 x21 + 8 x32 + 10 x43

Subject To
 cons_s: + 1 x43 - 1 x24 = 1
 cons_0: + 1 x01 - 1 x20 = 0
 cons_2: + 1 x20 + 1 x21 + 1 x24 - 1 x32 = 0
 cons_3: + 1 x32 - 1 x13 - 1 x43 = 0
 cons_t: + 1 x13 - 1 x01 - 1 x21 = -1

Bounds
  0 <= x01 <= 1
  0 <= x13 <= 1
  0 <= x20 <= 1
  0 <= x21 <= 1
  0 <= x24 <= 1
  0 <= x32 <= 1
  0 <= x43 <= 1
End
