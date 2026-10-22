"""T1b: independent numerical re-check of the sign error on p. 441 of the review.

The two determinants are transcribed exactly as printed in the paper:

    |iii| = det [[phi_a(1) alpha_1, phi_b(1) beta_1 ],     |iv| = det [[phi_a(1) beta_1, phi_b(1) alpha_1],
                 [phi_a(2) alpha_2, phi_b(2) beta_2 ]]                  [phi_a(2) beta_2, phi_b(2) alpha_2]]

(rows = electrons, columns = spin orbitals).  Spatial orbitals are random orthonormal vectors on a
grid of M points, spin is a 2-vector, and a two-electron state is a tensor Psi[r1, s1, r2, s2].
The total-spin operator S^2 = (s_1 + s_2)^2 is applied to the spin indices, and each combination is
classified by its S^2 eigenvalue (0 = singlet, 2 = triplet).  No algebraic factorisation is used.
"""
import numpy as np

rng = np.random.default_rng(2015)
M = 7
Q, _ = np.linalg.qr(rng.normal(size=(M, 2)))
phi_a, phi_b = Q[:, 0], Q[:, 1]
alpha, beta = np.array([1.0, 0.0]), np.array([0.0, 1.0])


def spin_orbital(phi, spin):
    return np.einsum("r,s->rs", phi, spin)          # chi[r, s]


def det2(chi1, chi2):
    """det [[chi1(1), chi2(1)], [chi1(2), chi2(2)]] = chi1(1) chi2(2) - chi2(1) chi1(2)."""
    return np.einsum("ab,cd->abcd", chi1, chi2) - np.einsum("ab,cd->abcd", chi2, chi1)


D_iii = det2(spin_orbital(phi_a, alpha), spin_orbital(phi_b, beta))
D_iv = det2(spin_orbital(phi_a, beta), spin_orbital(phi_b, alpha))

# one-electron spin operators
sx = 0.5 * np.array([[0, 1], [1, 0]]); sy = 0.5 * np.array([[0, -1j], [1j, 0]]); sz = 0.5 * np.diag([1.0, -1.0])
I2 = np.eye(2)
S2_spin = sum((np.kron(s, I2) + np.kron(I2, s)) @ (np.kron(s, I2) + np.kron(I2, s)) for s in (sx, sy, sz)).real
S2_spin = S2_spin.reshape(2, 2, 2, 2)              # [s1', s2', s1, s2]


def apply_S2(psi):
    return np.einsum("ABab,rasb->rAsB", S2_spin, psi)


def classify(name, psi):
    psi = psi / np.linalg.norm(psi)
    s2psi = apply_S2(psi)
    lam = np.vdot(psi, s2psi).real
    resid = np.linalg.norm(s2psi - lam * psi)
    antisym = np.allclose(psi, -psi.transpose(2, 3, 0, 1))
    label = {0: "SINGLET (S=0)", 2: "TRIPLET (S=1)"}.get(int(round(lam)), f"mixed, <S2>={lam:.3f}")
    print(f"{name:42s} <S^2> = {lam:+.12f}  eigen-residual = {resid:.1e}  antisymmetric = {antisym}  -> {label}")
    return lam, resid


ok = True
lam, res = classify("paper:   (1/2)(|iii| + |iv|)", 0.5 * (D_iii + D_iv))
ok &= abs(lam - 2) < 1e-12 and res < 1e-12
lam, res = classify("correct: (1/2)(|iv| - |iii|)", 0.5 * (D_iv - D_iii))
ok &= abs(lam) < 1e-12 and res < 1e-12
lam, res = classify("|iii| alone", D_iii)
ok &= abs(lam - 1) < 1e-12 and res > 1e-3               # half singlet, half triplet

# the paper's product form, line 1 of the equation block: sym. space x (beta1 alpha2 - alpha1 beta2)
space_sym = np.einsum("r,s->rs", phi_a, phi_b) + np.einsum("r,s->rs", phi_b, phi_a)
spin_part = np.einsum("a,b->ab", beta, alpha) - np.einsum("a,b->ab", alpha, beta)
product_form = 0.5 * np.einsum("rs,ab->rasb", space_sym, spin_part)
lam, res = classify("paper's product form (line 1)", product_form)
ok &= abs(lam) < 1e-12
same = np.allclose(product_form, 0.5 * (D_iv - D_iii))
print(f"product form == (1/2)(|iv| - |iii|): {same};  == (1/2)(|iii| + |iv|): {np.allclose(product_form, 0.5 * (D_iii + D_iv))}")
ok &= same
print("T1b PASS: the printed '+' combination is the M_S = 0 triplet" if ok else "T1b FAIL")
