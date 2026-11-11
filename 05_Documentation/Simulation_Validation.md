# Final simulation validation

Final solver state: **SUCCESS**. Actual reopen/rerun evidence: `02_Simulation_Results/Verification.json`. This file is generated from a separate open of the delivered .cst, not from filename existence.

## Acceptance checks

- Actual CST patch model and companion results: saved under 01_CST_Project.
- Operating frequency 150 GHz is within 130–170 GHz.
- Maximum directivity at 150 GHz: 7.4602 dBi >6.5 dBi.
- S11 at 150 GHz: -13.4245 dB ≤−10 dB.
- Actual −10 dB bandwidth calculated from crossings: 3.5128 GHz.
- Analytical and simulated match-resonance frequencies compared with definitions stated.
- Directivity, realized gain and radiation/total efficiency exported at actual monitor frequencies.
- E/H-plane and full-sphere pattern exports provided at 150 GHz.
- Passive S-parameter check: maximum |S11|=0.92181989 ≤1.
- Mesh sensitivity: ΔD=0.03728 dB; Δf=0.56436% between last two meshes.
- Reopening and reproducibility status: {"selected_working_project": "D:\\TELE9782\\Project_Final\\06_Working\\Box_Fine\\Box_Fine.cst", "delivered_project": "D:\\TELE9782\\Project_Final\\01_CST_Project\\TELE9782_DBand_Patch_Final.cst", "reopened_before_fresh_run": true, "reopened_after_fresh_run": true, "parameters_match": true, "port_present": true, "farfield_monitor_count": 13, "S11_sample_count": 1001, "reopen_max_complex_S11_difference": 0.0, "rerun_max_complex_S11_difference": 4.985546416924428e-06, "rerun_max_directivity_difference_dB": 2.96341473182693e-05, "final_reopen_max_complex_S11_difference": 0.0, "solver": {"message": null, "state": "SUCCESS"}}.

## Power consistency at 150 GHz

Incident 0.500000000 W; accepted 0.477274084 W; outgoing/reflected 0.022725916 W; radiated 0.341504645 W; metal loss 0.089537419 W; dielectric loss 0.042635663 W. Power balance residual Paccepted−Prad−Pmetal−Pdielectric=0.003596356 W (0.7535% of accepted power). This residual is reported, not forced to zero or hidden by renormalization.

Radiation efficiency Prad/Paccepted=71.5532%; total efficiency includes reflected power. The realized-gain identity D+10log10(ηrad)+10log10(1−|S11|²) differs from CST realized gain by -0.00000000 dB. Because these CST quantities share solver inputs, that identity is a consistency check, not independent experimental validation.

## Full-sphere check

The 2° CST-exported total-directivity grid is integrated as (1/4π)∫D(θ,φ)sinθ dθ dφ, with the φ seam closed. Its spherical mean is 0.9991083; the ideal normalization is 1. The deviation is -0.0892%. This includes discretization/export error and CST's finite power-normalization residual. Independently normalizing the *pattern shape* yields a diagnostic peak of 7.4639 dBi. The reported course result remains the unmodified CST value 7.4602 dBi. No curve, scale or normalization was altered to pass the requirement.

## Warnings and limitations

- This software is licensed for non-commercial use only.
- 2026-11-11 03:07:56   current system memory usage reached 90% (15 GB)
- 2026-11-11 03:08:28   current system memory usage reached 90% (15 GB)
- 3 warnings occurred.

The memory warnings above carry the original 03:07-03:08 timestamps in the retained CST message history. The later fresh final solver run completed successfully; these entries are retained transparently rather than removed. They do not indicate an unresolved port or normalization error.

The port mode solver also states that it approximates dispersive materials at 150 GHz and neglects their loss terms for the port eigenmode. The full 3D gold/dielectric losses remain active. This documented port approximation is distinct from making the antenna lossless. The old short-port, boundary-dispersion, metal-decoupling and staircase warnings must be absent in the final messages, which are retained in summary.json and the CST solver log.

No licence limit was inferred without an observed rejection. The successful mesh sizes above demonstrate only the capability exercised in this task. The software licence is non-commercial/educational. No physical measurements or measured D-band material validation were performed.
