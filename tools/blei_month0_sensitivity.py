#!/usr/bin/env python3
"""Month 0 BLEI sensitivity for Profile A (basic-living-economic-index.html, Table 2, Appendix B.2).
BLEI0 = (cash + h_AE*AE + gamma*Y + BU_food*eps) / (C_basic/30); AE = 0 at entry."""
Y, cash, BU, C = 2083, 1000, 360, 950/30
def b(eps=2.75, gamma=0.12, c=C): return (cash + gamma*Y + BU*eps)/c
print("base (eps 2.75, B.2)", round(b(),1)); print("eps 2.64", round(b(eps=2.64),1))
print("eps 1.50 / 3.00", round(b(eps=1.5),1), round(b(eps=3.0),1))
print("gamma 0.12 / 0.28", round(b(gamma=.12),1), round(b(gamma=.28),1))
print("C 28 / 45 / 52", *(round(b(c=x),1) for x in (28,45,52)))
