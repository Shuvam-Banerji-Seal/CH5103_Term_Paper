"""T3: K_pq >= 0 for real molecular orbitals.  (D4)
T4: He 1s2s 2^3S vs 2^1S: E, <T>, <V_ne>, <V_ee>, virial ratio, with optimal basis scaling. (D5)
T5: H2 minimal basis: analytic RHF / 2x2 CI / triplet / OSS formulas vs PySCF. (D6)
"""
import numpy as np
from pyscf import gto, scf, fci, ao2mo
from scipy.optimize import minimize_scalar

ok = True

# ---------------------------------------------------------------- T3
mol = gto.M(atom="O 0 0 0; H 0 0.76 0.59; H 0 -0.76 0.59", basis="6-31g", verbose=0)
mf = scf.RHF(mol).run()
eri_mo = ao2mo.restore(1, ao2mo.kernel(mol, mf.mo_coeff), mol.nao)
n = mol.nao
K = np.array([[eri_mo[p, q, p, q] for q in range(n)] for p in range(n)])
J = np.array([[eri_mo[p, p, q, q] for q in range(n)] for p in range(n)])
c = K.min() >= -1e-12 and np.all(J >= K - 1e-12)
print(f"T3 water/6-31G MOs: min K_pq = {K.min():.3e}; all J_pq >= K_pq: {np.all(J >= K - 1e-12)} -> {c}")
ok &= c

# ---------------------------------------------------------------- T4
def he_basis(eta):
    s = [0.02 * 2.2 ** k for k in range(16)]      # 0.02 ... ~2.7e3
    p = [0.04 * 2.6 ** k for k in range(7)]
    d = [0.08 * 3.0 ** k for k in range(4)]
    bas = [[0, [eta**2 * e, 1.0]] for e in s] + [[1, [eta**2 * e, 1.0]] for e in p] \
        + [[2, [eta**2 * e, 1.0]] for e in d]
    return {"He": bas}

def he_state(eta, which):
    """Return E, <T>, <Vne>, <Vee> for which in {'3S','1S'} with exponents scaled by eta^2."""
    m = gto.M(atom="He 0 0 0", basis=he_basis(eta), verbose=0, cart=False)
    S = m.intor("int1e_ovlp")
    # symmetric orthogonalisation (drop tiny eigenvalues)
    w, U = np.linalg.eigh(S); keep = w > 1e-9
    X = U[:, keep] / np.sqrt(w[keep])
    T = X.T @ m.intor("int1e_kin") @ X
    V = X.T @ m.intor("int1e_nuc") @ X
    eri = ao2mo.restore(1, ao2mo.kernel(m, X), X.shape[1])
    h = T + V; n = X.shape[1]
    # Exact two-electron problem in the spatial pair space Psi(1,2) = sum_pq C_pq phi_p(1) phi_q(2):
    #   H[(p,q),(r,s)] = h_pr d_qs + d_pr h_qs + (pr|qs)
    # singlet <-> C symmetric, triplet <-> C antisymmetric (spin factor carries the other symmetry).
    I = np.eye(n)
    H = (np.einsum("pr,qs->pqrs", h, I) + np.einsum("pr,qs->pqrs", I, h)
         + eri.transpose(0, 2, 1, 3)).reshape(n * n, n * n)
    sign = +1 if which == "1S" else -1
    cols = []
    for p in range(n):
        for q in range(p if sign > 0 else p + 1, n):
            v = np.zeros((n, n)); v[p, q] += 1; v[q, p] += sign
            cols.append(v.ravel() / np.linalg.norm(v))
    B = np.array(cols).T
    w, Y = np.linalg.eigh(B.T @ H @ B)
    pick = 1 if which == "1S" else 0          # 1S: root 0 is 1^1S, root 1 is 2^1S ; 3S: root 0 is 2^3S
    e = w[pick]; C = (B @ Y[:, pick]).reshape(n, n)
    Tex = 2 * np.einsum("pq,pr,rq", C, T, C)
    Vne = 2 * np.einsum("pq,pr,rq", C, V, C)
    Vee = np.einsum("pq,prqs,rs", C, eri, C)
    assert np.isclose(Tex + Vne + Vee, e, atol=1e-8)
    return e, Tex, Vne, Vee

exact = {"3S": -2.1752293782367, "1S": -2.1459740460544}   # Drake (via arXiv 2301.05442)
res = {}
for st in ("3S", "1S"):
    opt = minimize_scalar(lambda x: he_state(x, st)[0], bounds=(0.8, 1.2), method="bounded",
                          options={"xatol": 1e-5})
    e, t, vne, vee = he_state(opt.x, st)
    res[st] = (e, t, vne, vee)
    print(f"He 2^{st}: eta*={opt.x:.5f} E={e:.6f} (exact {exact[st]:.6f}, err {e-exact[st]:.1e}) "
          f"<T>={t:.6f} <Vne>={vne:.6f} <Vee>={vee:.6f} -V/T={-(vne+vee)/t:.6f}")
dE = res["3S"][0] - res["1S"][0]
dT = res["3S"][1] - res["1S"][1]; dVne = res["3S"][2] - res["1S"][2]; dVee = res["3S"][3] - res["1S"][3]
print(f"Delta(T - S): dE={dE:.6f} dT={dT:.6f} dVne={dVne:.6f} dVee={dVee:.6f}  "
      f"check dE = -dT = (dVne+dVee)/2: {-dT:.6f}, {(dVne + dVee) / 2:.6f}")
c = (dE < 0 and dVee > 0 and dVne < 0 and abs(dVne) > dVee
     and all(abs(-(r[2] + r[3]) / r[1] - 2) < 1e-4 for r in res.values())
     and all(abs(res[s][0] - exact[s]) < 2e-3 for s in res))
print(f"T4 less-screening pattern (dE<0, dVee>0, dVne<0, |dVne|>dVee, virial ok): {c}")
ok &= c

# ---------------------------------------------------------------- T5
def h2_point(R):
    m = gto.M(atom=f"H 0 0 0; H 0 0 {R}", basis="sto-3g", unit="Bohr", verbose=0)
    mf = scf.RHF(m).run()
    C = mf.mo_coeff; h = C.T @ (m.intor("int1e_kin") + m.intor("int1e_nuc")) @ C
    g = ao2mo.restore(1, ao2mo.kernel(m, C), 2); Vnn = m.energy_nuc()
    h11, h22 = h[0, 0], h[1, 1]
    J11, J22, J12, K12 = g[0, 0, 0, 0], g[1, 1, 1, 1], g[0, 0, 1, 1], g[0, 1, 0, 1]
    E_rhf = 2 * h11 + J11 + Vnn
    H = np.array([[2 * h11 + J11, K12], [K12, 2 * h22 + J22]])
    E_ci = np.linalg.eigvalsh(H)[0] + Vnn
    E_T = h11 + h22 + J12 - K12 + Vnn
    E_OSS = h11 + h22 + J12 + K12 + Vnn
    e_fci = fci.FCI(mf).kernel()[0]
    e_trip = scf.ROHF(gto.M(atom=f"H 0 0 0; H 0 0 {R}", basis="sto-3g", unit="Bohr", spin=2,
                            verbose=0)).run().e_tot
    c = (np.isclose(E_rhf, mf.e_tot) and np.isclose(E_ci, e_fci) and np.isclose(E_T, e_trip)
         and abs(h[0, 1]) < 1e-10 and abs(g[0, 0, 0, 1]) < 1e-6)
    return E_rhf, E_ci, E_T, E_OSS, J11, J22, J12, K12, c
eH = scf.UHF(gto.M(atom="H 0 0 0", basis="sto-3g", spin=1, verbose=0)).run().e_tot
print(f"H atom STO-3G: {eH:.6f}  -> 2E(H) = {2*eH:.6f}")
for R in (1.4, 3.0, 6.0, 20.0):
    E_rhf, E_ci, E_T, E_OSS, J11, J22, J12, K12, c = h2_point(R)
    print(f"R={R:5.1f}: RHF={E_rhf:.6f} CI=FCI={E_ci:.6f} T={E_T:.6f} OSS(1Su+)={E_OSS:.6f} "
          f"J11={J11:.4f} J22={J22:.4f} J12={J12:.4f} K12={K12:.4f} analytic==pyscf {c}")
    ok &= c
E_rhf, E_ci, E_T, *_ , c = h2_point(20.0)
lim = abs(E_ci - 2 * eH) < 1e-6 and abs(E_T - 2 * eH) < 1e-6 and E_rhf - 2 * eH > 0.2
print(f"R->inf: CI and T -> 2E(H) ; RHF error = {E_rhf - 2*eH:.4f} Eh : {lim}")
ok &= lim
print("T3-T5 PASS" if ok else "T3-T5 FAIL")
