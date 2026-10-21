"""T11a: high-spin ROHF stationarity conditions and canonicalisation-dependence of orbital ordering (D14).
T11b: SOMO-HOMO conversion in a distonic radical anion, tested by the observable (Delta-SCF)
      criterion the review recommends, and switched off by protonation (D12).
"""
import numpy as np
from pyscf import gto, scf, dft
from pyscf.geomopt.geometric_solver import optimize
from rdkit import Chem
from rdkit.Chem import AllChem

ok = True

# ---------------------------------------------------------------- T11a
def rohf_blocks(atom, spin, charge=0, basis="6-31g*"):
    mol = gto.M(atom=atom, spin=spin, charge=charge, basis=basis, verbose=0)
    mf = scf.ROHF(mol).run(conv_tol=1e-11)
    dm = mf.make_rdm1()
    vhf = mf.get_veff(mol, dm)
    h1 = mf.get_hcore()
    C = mf.mo_coeff
    Fa = C.T @ (h1 + vhf[0]) @ C; Fb = C.T @ (h1 + vhf[1]) @ C
    occ = mf.mo_occ
    c, o, v = np.where(occ == 2)[0], np.where(occ == 1)[0], np.where(occ == 0)[0]
    return mol, mf, Fa, Fb, c, o, v

def canonical_energies(Fa, Fb, c, o, v, A):
    """Diagonal blocks R_xx = A_xx * Fa + (1 - A_xx) * Fb ; returns block eigenvalues."""
    out = {}
    for name, idx in (("c", c), ("o", o), ("v", v)):
        R = A[name] * Fa[np.ix_(idx, idx)] + (1 - A[name]) * Fb[np.ix_(idx, idx)]
        out[name] = np.sort(np.linalg.eigvalsh(R))
    return out

schemes = {
    "all (Fa+Fb)/2 [PySCF default]": {"c": .5, "o": .5, "v": .5},
    "open block = Fa (alpha-like)": {"c": .5, "o": 1.0, "v": .5},
    "open block = Fb (beta-like)": {"c": .5, "o": 0.0, "v": .5},
    "closed=Fb, open=Fa, virt=Fa": {"c": 0.0, "o": 1.0, "v": 1.0},
}
molecules = {
    "H2NO (aminoxyl)": ("N 0 0 0; O 0 0 1.28; H 0.95 0 -0.35; H -0.95 0 -0.35", 1),
    "NO2": ("N 0 0 0; O 0 1.10 0.46; O 0 -1.10 0.46", 1),
    "CH3": ("C 0 0 0; H 1.08 0 0; H -0.54 0.935 0; H -0.54 -0.935 0", 1),
    "allyl": ("C 0 0 0; C 1.24 0.70 0; C -1.24 0.70 0; H 0 -1.09 0; H 2.17 0.15 0; H 1.27 1.79 0;"
              "H -2.17 0.15 0; H -1.27 1.79 0", 1),
}
print("T11a ROHF/6-31G*: stationarity blocks and canonicalisation dependence")
flip_seen = True
for name, (atom, spin) in molecules.items():
    mol, mf, Fa, Fb, c, o, v = rohf_blocks(atom, spin)
    g_co = np.abs(Fb[np.ix_(c, o)]).max(); g_ov = np.abs(Fa[np.ix_(o, v)]).max()
    g_cv = np.abs((Fa + Fb)[np.ix_(c, v)]).max()
    n_co = np.abs(Fa[np.ix_(c, o)]).max(); n_ov = np.abs(Fb[np.ix_(o, v)]).max()
    stat = max(g_co, g_ov, g_cv) < 1e-5 and max(n_co, n_ov) > 1e-3
    print(f"  {name}: E={mf.e_tot:.8f}  |Fb_co|={g_co:.1e} |Fa_ov|={g_ov:.1e} |(Fa+Fb)_cv|={g_cv:.1e} "
          f"(non-vanishing |Fa_co|={n_co:.2e}, |Fb_ov|={n_ov:.2e}) stationarity {stat}")
    ok &= stat
    for sname, A in schemes.items():
        e = canonical_energies(Fa, Fb, c, o, v, A)
        somo, homo = e["o"][-1], e["c"][-1]
        order = "SOMO > HOMO (aufbau-looking)" if somo > homo else "SOMO < HOMO (non-aufbau-looking)"
        print(f"     {sname:32s} eps_SOMO={somo:+.4f} eps_HOMO(closed)={homo:+.4f} -> {order}")
    # The open-open block is arbitrary: R_oo = A Fa_oo + (1-A) Fb_oo leaves E unchanged for every real A.
    # With one open orbital eps_SOMO(A) is linear in A; find the crossing with the (Fa+Fb)/2 closed HOMO.
    fa, fb = Fa[o[0], o[0]], Fb[o[0], o[0]]
    homo = canonical_energies(Fa, Fb, c, o, v, schemes["all (Fa+Fb)/2 [PySCF default]"])["c"][-1]
    A_star = (homo - fb) / (fa - fb)
    flips = all((A * fa + (1 - A) * fb < homo) == (A > A_star) for A in (0.0, 0.5, 1.0, A_star + 0.05))
    print(f"     crossing weight A* = {A_star:.3f}: SOMO drops below HOMO for A > A*; flip verified {flips}")
    flip_seen &= flips and A_star > 1.0
print(f"  ordering is convention-dependent (flips at A*), but not within 0<=A<=1 for these radicals: {flip_seen}")
ok &= flip_seen

# ---------------------------------------------------------------- T11b
def build(smiles, charge, spin):
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(m, randomSeed=11); AllChem.MMFFOptimizeMolecule(m)
    conf = m.GetConformer()
    atom = [(a.GetSymbol(), tuple(conf.GetAtomPosition(a.GetIdx()))) for a in m.GetAtoms()]
    return gto.M(atom=atom, charge=charge, spin=spin, basis="6-31+g*", verbose=0)

def uks(mol, xc="b3lyp"):
    mf = dft.UKS(mol); mf.xc = xc; mf.conv_tol = 1e-9
    return mf

systems = {
    # distonic radical anion: aminoxyl radical + remote (non-conjugated) carboxylate
    "anion  •ON(Me)CH2CH2COO-": ("C[N]([O])CCC(=O)[O-]", -1),
    "acid   •ON(Me)CH2CH2COOH": ("C[N]([O])CCC(=O)O", 0),
}
print("T11b UB3LYP/6-31+G*: vertical oxidation at the optimised radical geometry")
results = {}
for name, (smi, q) in systems.items():
    mol = build(smi, q, 1)
    mf = uks(mol)
    mol_eq = optimize(mf, maxsteps=100)
    mf = uks(mol_eq).run()
    E_rad = mf.e_tot
    # alpha orbital energies: is the SOMO (largest alpha-beta density difference) below the alpha-HOMO?
    ea = mf.mo_energy[0]; na = int(mf.nelec[0])
    spin_dens = mf.make_rdm1()[0] - mf.make_rdm1()[1]
    S = mol_eq.intor("int1e_ovlp")
    Ca = mf.mo_coeff[0][:, :na]
    # SOMO = occupied alpha orbital with largest overlap with the spin density
    w = np.einsum("mi,mn,nk,kl,li->i", Ca, S, spin_dens, S, Ca)
    i_somo = int(np.argmax(w))
    # vertical oxidised states at the same geometry
    trip = uks(gto.M(atom=mol_eq.atom, unit="Bohr", charge=q + 1, spin=2, basis="6-31+g*", verbose=0)).run()
    rks = dft.RKS(gto.M(atom=mol_eq.atom, unit="Bohr", charge=q + 1, spin=0, basis="6-31+g*", verbose=0))
    rks.xc = "b3lyp"; rks.conv_tol = 1e-9; rks.run()
    dT = (trip.e_tot - E_rad) * 27.211386; dCS = (rks.e_tot - E_rad) * 27.211386
    results[name] = (dT, dCS)
    print(f"  {name}: alpha SOMO index {i_somo} of {na} occupied alpha (HOMO index {na-1}); "
          f"eps_SOMO={ea[i_somo]*27.2114:+.2f} eV eps_aHOMO={ea[na-1]*27.2114:+.2f} eV")
    print(f"     vertical IE -> triplet diradical: {dT:.3f} eV ; -> closed-shell singlet: {dCS:.3f} eV ; "
          f"lower product: {'TRIPLET (electron taken from below-SOMO-->non-aufbau)' if dT < dCS else 'CLOSED SHELL (SOMO ionised-->aufbau)'}")
a_T, a_CS = results["anion  •ON(Me)CH2CH2COO-"]; n_T, n_CS = results["acid   •ON(Me)CH2CH2COOH"]
c = a_T < a_CS and n_CS < n_T
print(f"  pH switch (anion non-aufbau, protonated acid aufbau): {c}")
ok &= c
print("T11 PASS" if ok else "T11 FAIL")
