# Final acceptance checklist

All 19 requested acceptance items have been completed using actual CST numerical results. These are full-wave simulations, not physical measurements.

- [x] **Actual CST engineering project created** — Native .cst plus same-stem companion results in 01_CST_Project; reopened twice.
- [x] **Saved in D:/TELE9782/Project_Final** — 01_CST_Project/TELE9782_DBand_Patch_Final.cst
- [x] **Microstrip patch structure verified** — Single inset-fed rectangular patch; geometry and parameter figures.
- [x] **Operating frequency within 130-170 GHz** — 150 GHz.
- [x] **Directivity exceeds 6.5 dBi at valid operating point** — 7.4602 dBi at 150 GHz, with S11=-13.4245 dB.
- [x] **S11 meets -10 dB at selected frequency** — -13.4245 dB at 150 GHz.
- [x] **Actual -10 dB bandwidth calculated** — 147.1058-150.6186 GHz; 3.5128 GHz (2.3598%); interpolated threshold crossings.
- [x] **Theory and simulation resonance compared** — Final dimensions: analytical 152.0003 GHz versus S11-minimum match resonance 148.8400 GHz; difference 3.1603 GHz / 2.0791%. Not an eigenmode measurement.
- [x] **Directivity versus frequency available** — Directivity.csv and Directivity_vs_Frequency.png; 13 actual monitor frequencies.
- [x] **Realized gain versus frequency available** — Realized_Gain.csv and Realized_Gain_vs_Frequency.png.
- [x] **Radiation efficiency versus frequency available** — Radiation_Efficiency.csv and Radiation_Efficiency.png; total efficiency distinguished.
- [x] **E-plane and H-plane patterns available** — 150 GHz: E plane yz, H plane xz; numerical cuts, plots and native 3D farfield.
- [x] **Solver warnings reviewed** — SUCCESS; retained non-commercial licence notice and timestamped memory-usage warnings; port material approximation documented. No unresolved short-port or farfield-normalization failure.
- [x] **Power and farfield consistency checked** — Power residual 0.7535% of accepted power; spherical mean directivity 0.9991083; realized-gain identity checked.
- [x] **Mesh sensitivity evaluated** — Two accepted enclosing-surface meshes: directivity change 0.03728 dB and match-resonance change 0.56436%. Deep S11 null and off-band details remain more sensitive.
- [x] **Simulation data exported** — 02_Simulation_Results includes raw CST exports and numerical validation table.
- [x] **Final CST project successfully reopened** — Reopened before and after a fresh final solver run; Verification.json.
- [x] **Final results verified against saved project** — Reopen complex-S11 difference exactly zero; rerun max difference 4.986e-6; max directivity difference 2.963e-5 dB.
- [x] **Reproducibility documentation completed** — README.md, 04_Automation/README.md, native rerun/rebuild/extraction scripts. Final saved-project rerun was executed; packaged entry-point wrappers are syntax-checked and use the exercised native functions.

## Scope and remaining limits

The validated operating point is 150 GHz; matching over all of 130-170 GHz is not claimed. Polyimide and gold use documented material assumptions, without measured D-band material characterization or manufacturing tolerance validation. The independent checks are numerical, not an independent solver or experiment. The historical invalid near-model-surface results are retained only as rejected diagnostics. Original source integrity is recorded separately.
