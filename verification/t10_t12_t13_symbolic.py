"""T10: frozen-orbital (Koopmans) orbital energies and the S-T gap as an orbital-energy difference (D11).
T12: 3d/4s average-of-configuration algebra (D15).
T13: [l_1, 1/r12] != 0 but [L = l_1 + l_2, 1/r12] = 0 ; [l_1^2, 1/r12] != 0 (D16).
"""
import sympy as sp

ok = True

# ---------------------------------------------------------------- T10
ha, hb, Jab, Kab = sp.symbols("h_a h_b J_ab K_ab")
E_T = ha + hb + Jab - Kab          # 3Psi
E_S = ha + hb + Jab + Kab          # OSS (pure configuration, frozen orbitals)
E_ion = ha                         # electron removed from b, orbital a frozen
eps_b_T = E_T - E_ion              # = -IP_T  (Koopmans-type definition)
eps_b_S = E_S - E_ion              # = -IP_S
c = sp.simplify((E_S - E_T) - (eps_b_S - eps_b_T)) == 0 and sp.simplify(eps_b_T - (hb + Jab - Kab)) == 0
print(f"T10: E_S - E_T = eps_b(S) - eps_b(T) = 2K: {c}")
ok &= c

# ---------------------------------------------------------------- T12
n = sp.symbols("n", integer=True, nonnegative=True)
hd, hs, Jdd, Jds, Jss = sp.symbols("h_d h_s Jbar_dd Jbar_ds J_ss")
def E(nd, ns):
    """Average energy of configuration d^nd s^ns with average pair repulsions."""
    return nd * hd + ns * hs + sp.binomial(nd, 2) * Jdd + nd * ns * Jds + sp.binomial(ns, 2) * Jss
E_ds2 = sp.expand_func(E(n, 2)); E_d1s = sp.expand_func(E(n + 1, 1))
Delta = sp.simplify(E_d1s - E_ds2)
# orbital energies in d^n s^2 (Koopmans: eps_i = E(N) - E(N-1, frozen))
eps_d = sp.simplify(E_ds2 - sp.expand_func(E(n - 1, 2)))
eps_s = sp.simplify(E_ds2 - sp.expand_func(E(n, 1)))
target = sp.simplify((eps_d - eps_s) + Jdd - Jds)
c1 = sp.simplify(Delta - target) == 0
c2 = sp.simplify(eps_d - (hd + (n - 1) * Jdd + 2 * Jds)) == 0
c3 = sp.simplify(eps_s - (hs + n * Jds + Jss)) == 0
print(f"T12: E(d^(n+1)s) - E(d^n s^2) = {sp.simplify(Delta)}")
print(f"     = (eps_d - eps_s) + (Jdd - Jds): {c1}; eps_d form {c2}; eps_s form {c3}")
# cation: which electron leaves first?  E(d^n s^1) - E(d^(n-1) s^2), the ion analogue
Dion = sp.simplify(sp.expand_func(E(n, 1)) - sp.expand_func(E(n - 1, 2)))
c4 = sp.simplify(Dion - (Delta.subs(n, n - 1))) == 0
print(f"     ion analogue E(d^n s) - E(d^(n-1) s^2) = Delta(n-1): {c4}")
# numerical illustration: eps_d < eps_s yet s^2 configuration lower if Jdd - Jds > eps_s - eps_d
num = {hd: -2.5, hs: -1.5, Jdd: 0.80, Jds: 0.10, Jss: 0.40, n: 2}
print(f"     example: eps_d={float(eps_d.subs(num)):.3f} eps_s={float(eps_s.subs(num)):.3f} "
      f"Delta={float(Delta.subs(num)):.3f}  (eps_d<eps_s and Delta>0 => d^n s^2 lower)")
c_ex = float(eps_d.subs(num)) < float(eps_s.subs(num)) and float(Delta.subs(num)) > 0
ok &= c1 and c2 and c3 and c4 and c_ex

# ---------------------------------------------------------------- T13
x1, y1, z1, x2, y2, z2 = sp.symbols("x1 y1 z1 x2 y2 z2", real=True)
r12 = sp.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
f = sp.Function("f")(x1, y1, z1, x2, y2, z2)       # arbitrary test wavefunction
I = sp.I
def l1(g):  # l_1 = -i r_1 x grad_1  (hbar = 1)
    return [-I * (y1 * sp.diff(g, z1) - z1 * sp.diff(g, y1)),
            -I * (z1 * sp.diff(g, x1) - x1 * sp.diff(g, z1)),
            -I * (x1 * sp.diff(g, y1) - y1 * sp.diff(g, x1))]
def l2(g):
    return [-I * (y2 * sp.diff(g, z2) - z2 * sp.diff(g, y2)),
            -I * (z2 * sp.diff(g, x2) - x2 * sp.diff(g, z2)),
            -I * (x2 * sp.diff(g, y2) - y2 * sp.diff(g, x2))]
V = 1 / r12
comm_l1 = [sp.simplify(a - V * b) for a, b in zip(l1(V * f), l1(f))]          # [l_1, V] f
comm_L = [sp.simplify(a + b - V * (c + d)) for a, b, c, d in zip(l1(V * f), l2(V * f), l1(f), l2(f))]
c5 = any(cm != 0 for cm in comm_l1) and all(cm == 0 for cm in comm_L)
print(f"T13: [l_1z, 1/r12] f = {sp.simplify(comm_l1[2])}")
print(f"     [L_k, 1/r12] f = 0 for k=x,y,z: {all(cm == 0 for cm in comm_L)}")
def l1sq(g):
    comps = l1(g)
    return sum(c_ for c_ in [l1(comps[0])[0], l1(comps[1])[1], l1(comps[2])[2]])
c6 = sp.simplify(l1sq(V * f) - V * l1sq(f)) != 0
print(f"     [l_1^2, 1/r12] != 0: {c6}")
ok &= c5 and c6
print("T10,T12,T13 PASS" if ok else "T10,T12,T13 FAIL")
