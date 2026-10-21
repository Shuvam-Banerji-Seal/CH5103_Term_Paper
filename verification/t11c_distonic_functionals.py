"""T11c: does the Delta-SCF verdict for distonic radical anions depend on the functional and on the
radical-anion separation?  (resolves DIS13 from T11b)

Geometries: UB3LYP/6-31G* optimised radicals (cheaper than 6-31+G*; vertical energies are then evaluated
at 6-31+G*).  For each radical X (anion or protonated acid) and functional F:
   IE_T  = E_F(oxidised, triplet)          - E_F(X)
   IE_CS = E_F(oxidised, closed-shell RKS)  - E_F(X)
Non-aufbau (SOMO-HOMO converted) behaviour <=> IE_T < IE_CS.
"""
import json, pathlib
import numpy as np
from pyscf import gto, dft
from pyscf.geomopt.geometric_solver import optimize
from rdkit import Chem
from rdkit.Chem import AllChem

out = pathlib.Path(__file__).parent / "logs"
systems = {
    "short anion  .ON(Me)CH2CH2COO-": ("C[N]([O])CCC(=O)[O-]", -1),
    "short acid   .ON(Me)CH2CH2COOH": ("C[N]([O])CCC(=O)O", 0),
    "TEMPO-4-COO-": ("CC1(C)CC(C(=O)[O-])CC(C)(C)N1[O]", -1),
    "TEMPO-4-COOH": ("CC1(C)CC(C(=O)O)CC(C)(C)N1[O]", 0),
}
functionals = ["b3lyp", "camb3lyp"]

def embed(smi):
    m = Chem.AddHs(Chem.MolFromSmiles(smi))
    AllChem.EmbedMolecule(m, randomSeed=11); AllChem.MMFFOptimizeMolecule(m)
    c = m.GetConformer()
    return [(a.GetSymbol(), tuple(c.GetAtomPosition(a.GetIdx()))) for a in m.GetAtoms()]

def ks(atom, charge, spin, basis, xc, unit="Angstrom"):
    mol = gto.M(atom=atom, charge=charge, spin=spin, basis=basis, unit=unit, verbose=0)
    mf = (dft.UKS(mol) if spin else dft.RKS(mol)); mf.xc = xc; mf.conv_tol = 1e-9; mf.max_cycle = 200
    return mf

results = {}
for name, (smi, q) in systems.items():
    mf = ks(embed(smi), q, 1, "6-31g*", "b3lyp")
    mol_eq = optimize(mf, maxsteps=150)
    xyz = mol_eq.atom_coords(unit="Angstrom"); syms = [mol_eq.atom_symbol(i) for i in range(mol_eq.natm)]
    atom = [(s, tuple(x)) for s, x in zip(syms, xyz)]
    (out / f"geom_{name.split()[0]}_{name.split()[1] if len(name.split())>1 else ''}.xyz".replace(" ", "")).write_text(
        f"{len(atom)}\n{name}\n" + "\n".join(f"{s} {x:.6f} {y:.6f} {z:.6f}" for s, (x, y, z) in atom) + "\n")
    results[name] = {}
    for xc in functionals:
        rad = ks(atom, q, 1, "6-31+g*", xc).run()
        trip = ks(atom, q + 1, 2, "6-31+g*", xc).run()
        cs = ks(atom, q + 1, 0, "6-31+g*", xc).run()
        # orbital-level check: alpha SOMO position among occupied alpha orbitals
        na = int(rad.nelec[0]); dmd = rad.make_rdm1(); S = rad.mol.intor("int1e_ovlp")
        Ca = rad.mo_coeff[0][:, :na]
        w = np.einsum("mi,mn,nk,kl,li->i", Ca, S, dmd[0] - dmd[1], S, Ca)
        i_somo = int(np.argmax(w))
        IE_T = (trip.e_tot - rad.e_tot) * 27.211386
        IE_CS = (cs.e_tot - rad.e_tot) * 27.211386
        s2 = trip.spin_square()[0]
        results[name][xc] = dict(IE_T=IE_T, IE_CS=IE_CS, somo_rank_from_top=na - 1 - i_somo, S2_trip=s2)
        print(f"{name:34s} {xc:9s} IE_T={IE_T:6.3f} IE_CS={IE_CS:6.3f} eV  "
              f"Delta(T-CS)={IE_T-IE_CS:+.3f}  alpha-SOMO is {na-1-i_somo} below alpha-HOMO  <S2>_T={s2:.3f}",
              flush=True)
(out / "t11c.json").write_text(json.dumps(results, indent=1))
print("T11c DONE")
