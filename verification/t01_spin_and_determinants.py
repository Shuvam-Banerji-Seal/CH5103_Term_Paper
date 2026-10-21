"""T1: two-electron spin eigenfunctions and the Figure-1 determinant combinations (D1, D2)."""
import sympy as sp

# --- spin space of two electrons: basis |a a>, |a b>, |b a>, |b b>  (a = alpha, b = beta)
half = sp.Rational(1, 2)
sz = sp.Matrix([[half, 0], [0, -half]])
sp_ = sp.Matrix([[0, 1], [0, 0]])          # s+ |beta> = |alpha>
sm = sp_.T
I2 = sp.eye(2)
kron = sp.kronecker_product
Sz = kron(sz, I2) + kron(I2, sz)
Sp = kron(sp_, I2) + kron(I2, sp_)
Sm = kron(sm, I2) + kron(I2, sm)
S2 = Sm * Sp + Sz * Sz + Sz                # S^2 = S-S+ + Sz^2 + Sz

aa, ab, ba, bb = (sp.Matrix([1 if i == k else 0 for i in range(4)]) for k in range(4))
r2 = sp.sqrt(2)
spin_states = {
    "T+1 aa": (aa, 2, 1),
    "T0 (ab+ba)/r2": ((ab + ba) / r2, 2, 0),
    "T-1 bb": (bb, 2, -1),
    "S (ab-ba)/r2": ((ab - ba) / r2, 0, 0),
}
ok = True
for name, (v, s2, ms) in spin_states.items():
    c1 = sp.simplify(S2 * v - s2 * v) == sp.zeros(4, 1)
    c2 = sp.simplify(Sz * v - ms * v) == sp.zeros(4, 1)
    print(f"{name:16s} S^2={s2} Ms={ms}: {c1 and c2}")
    ok &= c1 and c2

# --- spatial x spin, Figure 1 determinants (unnormalised 2x2 Slater determinants)
a1, a2, b1, b2, A1, A2, B1, B2 = sp.symbols("phia1 phia2 phib1 phib2 al1 al2 be1 be2")
def det(o1, o2):
    """|o1 o2| with o(i) the spin orbital evaluated for electron i."""
    return sp.Matrix([[o1[0], o2[0]], [o1[1], o2[1]]]).det()
pa_al, pa_be = (a1 * A1, a2 * A2), (a1 * B1, a2 * B2)
pb_al, pb_be = (b1 * A1, b2 * A2), (b1 * B1, b2 * B2)
D = {
    "i": det(pa_al, pa_be), "ii": det(pb_al, pb_be),
    "iii": det(pa_al, pb_be), "iv": det(pa_be, pb_al),
    "v": det(pa_al, pb_al), "vi": det(pa_be, pb_be),
}
sym = a1 * b2 + b1 * a2; anti = a1 * b2 - b1 * a2
targets = {
    "3Psi(+1) = v/sqrt2": (D["v"] / r2, anti * A1 * A2 / r2),
    "3Psi(-1) = vi/sqrt2": (D["vi"] / r2, anti * B1 * B2 / r2),
    "3Psi(0)  = (iii+iv)/2": ((D["iii"] + D["iv"]) / 2, anti * (A1 * B2 + B1 * A2) / 2),
    "1Psi_OSS = (iv-iii)/2": ((D["iv"] - D["iii"]) / 2, sym * (B1 * A2 - A1 * B2) / 2),
    "paper's (iii+iv)/2 == OSS ? (expect False)": ((D["iii"] + D["iv"]) / 2, sym * (B1 * A2 - A1 * B2) / 2),
    "1Psi_CS(a^2) = i/sqrt2": (D["i"] / r2, a1 * a2 * (A1 * B2 - B1 * A2) / r2),
}
for name, (lhs, rhs) in targets.items():
    res = sp.expand(lhs - rhs) == 0
    print(f"{name:45s}: {res}")
    if "expect False" in name:
        ok &= not res
    else:
        ok &= res
print("T1 PASS" if ok else "T1 FAIL")
