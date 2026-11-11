# Presentation evidence map

Source root: `D:/TELE9782/Project_Final`. Numerical results are CST full-wave outputs or identified calculations from those exports. No experimental dataset was supplied.

The separate TELE9782 Chapter 14 course file was unavailable. The supplied project equations were used. Theory reference: [Balanis, Antenna Theory: Analysis and Design, 4th ed., Wiley, Chapter 14](https://www.wiley.com/en-us/-p-9781119178996).

## Slide 1 · Title and objective

**Displayed claims and values:** 130–170 GHz; Dmax >6.5 dBi.

- `D:/TELE9782/Project_Final/01_CST_Project/TELE9782_DBand_Patch_Final.cst`
- `D:/TELE9782/Project_Final/03_Figures/Antenna_Geometry.png`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. CST model image; supplied course requirement.

## Slide 2 · Requirements

**Displayed claims and values:** 130–170 GHz; 150 GHz nominal; >6.5 dBi.

- `D:/TELE9782/Project_Final/05_Documentation/Engineering_Design_Notes.md`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. The sweep range is distinct from impedance bandwidth.

## Slide 3 · Patch theory

**Displayed claims and values:** TM₁₀, L=Leff−2ΔL and Dmax=4πUmax/Prad.

- `D:/TELE9782/Project_Final/05_Documentation/Analytical_Starting_Design.json`
- `D:/TELE9782/Project_Final/05_Documentation/Engineering_Design_Notes.md`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Transmission-line approximation. The plan view is a schematic.

## Slide 4 · Analytical and final dimensions

**Displayed claims and values:** W/L 0.666/0.520 → 0.667/0.513 mm; h 0.040 mm; 152.000 vs 148.840 GHz, 2.08%; nominal material values.

- `D:/TELE9782/Project_Final/02_Simulation_Results/parameters.json`
- `D:/TELE9782/Project_Final/02_Simulation_Results/S11.csv`
- `D:/TELE9782/Project_Final/05_Documentation/Analytical_Starting_Design.json`
- `D:/TELE9782/Project_Final/04_Automation/Reference_ModelHistory.json`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Frequency comparison uses S11 minimum. Bulk material parameters assumed.

## Slide 5 · CST model and solver

**Displayed claims and values:** 0.090 mm; 50 Ω; 130–170 GHz; 262197 cells; 13 monitors; −60 dB.

- `D:/TELE9782/Project_Final/01_CST_Project/TELE9782_DBand_Patch_Final.cst`
- `D:/TELE9782/Project_Final/03_Figures/Port_Configuration.png`
- `D:/TELE9782/Project_Final/04_Automation/engineering.py`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Mesh_Convergence.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Verification.json`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Same final model. Mode solver uses a lossless approximation for port calculation, while full 3D losses are active.

## Slide 6 · Faults and optimisation

**Displayed claims and values:** −20.92 historical; −10.18 at 148.56; 0.17/−14.18; 0.19/−26.82; L 0.521 → 0.513 mm.

- `D:/TELE9782/Project_Final/05_Documentation/Project_Diagnosis.md`
- `D:/TELE9782/Project_Final/05_Documentation/Iteration_Log.csv`
- `D:/TELE9782/Project_Final/05_Documentation/Simulation_Validation.md`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Diagnostic near-model D values excluded from final compliance.

## Slide 7 · Match and bandwidth

**Displayed claims and values:** 150 GHz −13.424; min −38.859 at 148.840; edges 147.106/150.619; BW 3.513 GHz; 2.36%.

- `D:/TELE9782/Project_Final/02_Simulation_Results/S11.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Impedance_Bandwidth.csv`
- `D:/TELE9782/Project_Final/03_Figures/S11.png`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. 1001 samples; crossing interpolation; deep minimum is mesh-sensitive.

## Slide 8 · Directivity and realized gain

**Displayed claims and values:** 7.460 dBi; +0.960 dB margin; 5.804 dBi, all at 150 GHz.

- `D:/TELE9782/Project_Final/02_Simulation_Results/Directivity.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Realized_Gain.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Validation_Summary.csv`
- `D:/TELE9782/Project_Final/03_Figures/Directivity_vs_Frequency.png`
- `D:/TELE9782/Project_Final/03_Figures/Realized_Gain_vs_Frequency.png`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Thirteen monitor points; lines between points guide the eye.

## Slide 9 · Efficiency and cuts

**Displayed claims and values:** 71.55% at 150 GHz; E yz; H xz; near +z, θ≈4°.

- `D:/TELE9782/Project_Final/02_Simulation_Results/Radiation_Efficiency.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/E_Plane.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/H_Plane.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Farfield_150_Sphere.txt`
- `D:/TELE9782/Project_Final/03_Figures/Radiation_Efficiency.png`
- `D:/TELE9782/Project_Final/03_Figures/E_Plane.png`
- `D:/TELE9782/Project_Final/03_Figures/H_Plane.png`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Cuts are total D. Beam angle resolution is 2°.

## Slide 10 · Validation

**Displayed claims and values:** 0.037 dB; 0.56%; 0.9991; 0.754%; successful rerun.

- `D:/TELE9782/Project_Final/02_Simulation_Results/Mesh_Convergence.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Sphere_Normalization_Check.json`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Power_Consistency.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Verification.json`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Two mesh resolutions; convergence evidence limited to compared quantities.

## Slide 11 · Appendix A · Derivation

**Displayed claims and values:** λ₀ 1.9986 mm; εeff 3.203; Leff 0.5584; ΔL 0.0190; L 0.5204 mm; 152.000 GHz.

- `D:/TELE9782/Project_Final/05_Documentation/Analytical_Starting_Design.json`
- `D:/TELE9782/Project_Final/02_Simulation_Results/parameters.json`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Recomputed in full precision from supplied equations.

## Slide 12 · Appendix B · Parameters

**Displayed claims and values:** W/L, substrate, ground/launch, feed, inset/gap, gold thickness and σ.

- `D:/TELE9782/Project_Final/02_Simulation_Results/parameters.json`
- `D:/TELE9782/Project_Final/04_Automation/engineering.py`
- `D:/TELE9782/Project_Final/04_Automation/Reference_ModelHistory.json`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Material properties are model inputs.

## Slide 13 · Appendix C · Port

**Displayed claims and values:** y −1.2 mm; x ±0.25; z −0.002…0.24; 49.47 Ω line vs 50 Ω ref.

- `D:/TELE9782/Project_Final/04_Automation/engineering.py`
- `D:/TELE9782/Project_Final/03_Figures/Port_Configuration.png`
- `D:/TELE9782/Project_Final/02_Simulation_Results/CST_Raw/1D Results_Port Information_Line Impedance_1(1).csv`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Raw final export 49.4686436 Ω; ~49.9 Ω pertains to baseline.

## Slide 14 · Appendix D · Mesh/power

**Displayed claims and values:** 76,860/262,197 cells; D 7.497/7.460; dips 149.680/148.840; accepted/radiated/loss/residual powers.

- `D:/TELE9782/Project_Final/02_Simulation_Results/Mesh_Convergence.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Power_Consistency.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Sphere_Normalization_Check.json`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Verification.json`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Mesh table stores accepted Box_Fine predecessor; small rerun deltas round to same D.

## Slide 15 · Appendix E · Monitor table

**Displayed claims and values:** 13 rows of GHz, S11, D, realized gain, ηrad, ηtotal.

- `D:/TELE9782/Project_Final/02_Simulation_Results/Validation_Summary.csv`
- `D:/TELE9782/Project_Final/02_Simulation_Results/S11.csv`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Source rows imported directly; results shown to two decimals.

## Slide 16 · Appendix F · Polarisation

**Displayed claims and values:** θ≈4°, φ≈264°, y polarisation and E/H cut angles.

- `D:/TELE9782/Project_Final/02_Simulation_Results/Farfield_150_Sphere.txt`
- `D:/TELE9782/Project_Final/02_Simulation_Results/Sphere_Normalization_Check.json`
- `D:/TELE9782/Project_Final/05_Documentation/Engineering_Design_Notes.md`
- `D:/TELE9782/Project_Final/03_Figures/Farfield_3D.png`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Grid peak coordinates are approximate; azimuth near broadside is weakly conditioned.

## Slide 17 · Appendix G · Diagnostic history / theory

**Displayed claims and values:** Historical −20.92 dBi; rejected 8.54 dBi, sphere mean 1.291; accepted 0.9991.

- `D:/TELE9782/Project_Final/05_Documentation/Project_Diagnosis.md`
- `D:/TELE9782/Project_Final/05_Documentation/Simulation_Validation.md`
- `D:/TELE9782/Project_Final/05_Documentation/Iteration_Log.csv`

**Verification:** Matched saved sources and, where applicable, recalculated from exports. Separate Chapter 14 lecture handout not found. Uses supplied course equations and Balanis 4th ed. Chapter 14 as theory reference.

## Reconciliation

- Final line impedance is 49.4686 Ω. The diagnostic baseline was reported at about 49.9 Ω. Both are distinct from 50 Ω S-parameter normalization.
- Final values use the fresh run. The fine-mesh comparison uses the immediately preceding Box_Fine run of identical geometry and settings. Its differences are below displayed precision for D and match frequency.
- The historical −20.92 and 8.54 dBi values describe rejected diagnostics. The final 7.460 dBi value is the accepted simulated maximum at the matched 150 GHz point.
