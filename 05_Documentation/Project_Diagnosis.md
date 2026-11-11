# Existing project diagnosis

Inspection date: 10 November 2026, Australia/Sydney. All original files under `D:\TELE9782\lab2222` were treated as read-only. Work was performed on separate copies.

## Inventory and starting point

`lab_projevt.cst` is the existing D-band inset-fed rectangular patch. The spelling is the actual filename; `lab_project.cst` was not found. Its companion directory contains model history, parameter definitions, port modes, time-domain solver logs and farfield results at 130, 140, 150, 160 and 170 GHz. `lab2222.cst` is a 2.4 GHz dipole laboratory project, not a patch reference. The parent `Export` directory contains dipole laboratory screenshots. No TELE9782 Lab 5 handout, Chapter 14 slide deck or previous automation script was found outside the software installation. Consequently, the assignment and design equations supplied in the request are the course requirements used here; unavailable slides have not been cited as if inspected.

The installation is CST Studio Suite 2024.0, release 1 September 2023, build/change 1164796, located at `D:\TELE9782\CST Studio Suite 2024`. The GUI identifies it as “For Education”; solver output states non-commercial use only. It is not assumed to have the restrictions of the separate Student Edition. The installed Python 3.9 interpreter and `cst.interface`/`cst.results` libraries were successfully exercised. The selected solver is HF Time Domain (Hex), PBA. Other solver entries in an installation do not by themselves demonstrate licence availability.

## Original geometry and settings

| Quantity | Existing setting |
|---|---|
| Patch width / length | 0.667 / 0.521 mm |
| Substrate thickness | 0.040 mm |
| Substrate | Polyimide, epsilon_r 3.5, nominal constant tan(delta) 0.0027 |
| Original material reference | 1 MHz; no D-band material measurements supplied |
| Conductors | Gold, sigma 4.561e7 S/m |
| Patch metal thickness | 0.002 mm |
| Ground | Hard-coded 1 x 1 mm, thickness 0.0004 mm |
| Feed width | 0.090 mm |
| Inset depth / side gap | 0.150 / 0.020 mm |
| Last port location | y = -0.45 mm, internal |
| Last port orientation | ymax (excitation toward negative y) |
| Port x / z span | +/-0.135 mm; -0.002 to 0.122 mm |
| Sweep | 130–170 GHz |
| Boundaries | ymin open; other five expanded open |
| PML spacing reference | 130 GHz |
| Accuracy / mesh | -40 dB energy; 60,030 cells in the reproduced baseline |

## Reproduced failure and causal evidence

A fresh run of the unmodified working copy finished with CST solver state SUCCESS and reproduced the pathological farfield. The 150 GHz directivity result was approximately -20.912 dBi with radiation efficiency approximately -0.4295 dB (90.6%). The S11 minimum was approximately -26.72 dB at the upper sweep endpoint, rather than a credible isolated patch resonance. The total-Abs, both-angle farfield evaluation remained negative; merely selecting a different cut did not resolve it. These outputs are retained only as diagnostic evidence and are not accepted antenna performance.

The installed CST Port Object documentation explicitly defines orientation by excitation direction: `ymin` feeds positive y and `ymax` feeds negative y, including for internal ports. The old port feeds away from the patch into the short feed-side termination. This is a concrete configuration error. The solver also reported metal on boundaries while searching for decoupling planes, dispersive material at the ymin open boundary, and 377 mesh edges filled with PEC in staircase representation. Its reported radiated power therefore cannot be used as a trustworthy normalization for the antenna pattern. The exact internal contribution of each warning has not been separately quantified.

Changing the direction to `ymin`, at both the physical edge and the previous internal plane, exposed another error: “Waveguide for port number 1 is too short. The waveguide must be homogeneous for at least three equidistant mesh planes along propagation direction.” These controlled failed runs establish why changing only the coordinate or sign was insufficient.

The history contains a temporary `CalculateModesOnly=True` configuration and repeated port changes. A mode-only run does not create new full-wave farfields, and geometry/port edits invalidate prior field results. This provides a plausible explanation for unavailable monitors; the exact sequence of the earlier greyed-out UI was not recorded and is not asserted as proven.

## Repair strategy

A clean, parameterised single patch was reconstructed using the original dielectric and finite-conductivity gold assumptions. The board and ground are parameterised together and use consistent metal thickness. A uniform 0.5 mm feed launch leads into the finite board. The launch substrate and ground fit wholly within the port cross-section, so the dispersive substrate does not continue across the adjacent open boundary. The waveguide port faces positive y and has a quasi-TEM mode close to 50 ohms. The original inset topology is retained, with no ideal divider or artificial array factor.

Farfield monitors are created before each relevant solver run. The final model uses explicitly normalised 50-ohm S parameters, stricter energy decay and mesh comparisons. No lossless material substitution was used to produce the accepted performance. The polyimide constant loss tangent is an engineering assumption inherited from the project, not a verified material characterization at D-band. Gold roughness, process tolerances and measurement fixtures remain outside this simulation model.

The first reconstructed model ran successfully without the old port, boundary or staircase warnings. Its adaptive port impedance was approximately 49.9 ohms. Its directivity was 7.719 dBi at 150 GHz; its S11 minimum was -10.185 dB at 148.56 GHz. These baseline numbers are not the final optimized results; later iterations and final verification are recorded separately.

## Additional normalization defect found during mesh validation

The first reconstruction used CST's default "Monitor farfields near to model" option. Refining the mesh from 20/30 to 30/45 wavelength/box settings changed the 150 GHz directivity from approximately 7.61 to 8.54 dBi. Independent integration of the exported full-sphere pattern yielded a mean linear directivity of 1.291 instead of 1, and the fine-grid power balance residual was approximately 16.9% of accepted power. Therefore that fine-grid result was rejected, even though its displayed directivity exceeded the assignment requirement.

The antenna geometry and lossy materials were retained. `Solver.MonitorFarFieldsNearToModel False` moved the integration surface to the enclosing global calculation box, and the energy-decay criterion was tightened to -60 dB. The resulting Box_Fine run gave 7.4602 dBi at 150 GHz, full-sphere mean directivity 0.99911 and accepted-power balance residual 0.7535%. A matching Box_Coarse configuration gave 7.4974 dBi; the match-frequency shift between the two meshes was 0.56%. This controlled comparison supports a near-model integration-surface discretization problem. It does not justify treating the rejected 8.54 dBi value as antenna improvement.

An extra Tuned_Finer run was interrupted before acceptance, and a first Box_Fine attempt was aborted. They are not used as final evidence. The accepted Box_Fine run completed successfully and was subsequently selected for final save/reopen/fresh-run verification. The final delivery's verification record establishes the actual status of those last operations.

## Documentation actually used

- Installed CST help: `Online Help\mergedProjects\VBA_3D\special_vbaports\special_vbaports_port_object.htm` (port orientation and placement).
- Installed CST help: `Online Help\mergedProjects\VBA_3D\special_vbapostproc\special_vbapostproc_farfieldploto.htm` (farfield quantities, scaling and extraction).
- Installed CST help: `Online Help\Python\source\cst.interface.html` and `cst.results.html` (native automation and results).
- Existing CST model history and solver logs; analytical equations supplied in the task.

Full inventory and original-file SHA-256 values accompany this note. No physical antenna measurements were performed.
