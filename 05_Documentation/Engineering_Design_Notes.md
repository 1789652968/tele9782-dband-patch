# TELE9782 D-band microstrip patch — engineering design

This is CST full-wave numerical simulation, not a fabricated or physically measured antenna. The selected architecture is a single inset-fed rectangular patch. An array is unnecessary because the complete lossy single-patch model exceeds the course directivity threshold with margin.

## Final performance

Operating frequency: **150 GHz**. CST maximum directivity **7.460 dBi**, realized gain **5.804 dBi**, S11 **-13.424 dB**, radiation efficiency **71.55%**, total efficiency **68.30%**. These quantities are taken from the same final geometry and solver run.

The S11 minimum is **-38.859 dB at 148.840 GHz** on a 0.04 GHz output grid. The −10 dB crossings are **147.1058 and 150.6186 GHz**, obtained by linear interpolation of adjacent simulated S11-dB samples. Bandwidth is **3.5128 GHz**, or **2.360%** using the crossing midpoint. No claim of matching throughout 130–170 GHz is made.

## Geometry and materials

The patch lies in xy, length along y, ground at z≤0, substrate from z=0 to 0.04 mm. The patch width is 0.667 mm and length 0.513 mm. Main substrate and ground: 1.4 × 1.4 mm. A 0.5 mm-wide, 0.5 mm-long feed launch extends from the negative-y board edge. Feed width 0.09 mm; inset depth 0.19 mm; each side gap 0.02 mm. Patch and ground gold thickness is 0.002 mm.

Polyimide is modelled with εr=3.5 and nominal constant tanδ=0.0027, referenced at 150 GHz. These are inherited, documented engineering assumptions; no measured D-band dielectric dataset was supplied. Gold conductivity is 4.561e7 S/m. Finite conductivity and dielectric loss are included. No artificial lossless substitution or ideal feeding network is used. Surface roughness, anisotropy, temperature and fabrication tolerances are not characterized.

## Analytical starting design and comparison

The supplied transmission-line equations were used: W=c/(2fr)√[2/(εr+1)]; εeff=(εr+1)/2+(εr−1)/(2√(1+12h/W)); ΔL/h=0.412[(εeff+0.3)(W/h+0.264)]/[(εeff−0.258)(W/h+0.8)]; L=c/(2fr√εeff)−2ΔL.

At a 150 GHz target, εr=3.5 and h=0.040 mm, the calculated starting dimensions are W=0.666205 mm and L=0.520369 mm, with εeff=3.202978 and ΔL=0.019001 mm. The original rounded patch was 0.667 × 0.521 mm. Full-wave feed tuning selected a 0.190 mm inset; length tuning selected 0.513 mm.

Using the final W, L and h in the same analytical model gives **152.0003 GHz**, versus the simulated **148.8400 GHz S11 minimum**: absolute difference 3.1603 GHz, or 2.079% relative to theory. The S11 minimum is the reported impedance-match resonance, not a proof of an isolated modal eigenfrequency. The port-reactance zero crossings are separately exported in the numerical audit. The finite ground, inset slots, feed discontinuity, metal thickness, dielectric loss and full-wave fringing explain why the simple cavity/transmission-line estimate is not exact. Here h/W≈0.060 and h/λ0≈0.020, consistent with a thin microstrip starting approximation.

For the feed, the common quasi-static microstrip expression Z0≈120π/[√εeff(u+1.393+0.667 ln(u+1.444))], u=w/h>1, gives a starting width near 0.09 mm. CST's adaptive quasi-TEM port calculation, rather than this zero-thickness estimate, establishes the simulated port impedance. The nominal inset resistance relation Rin(y)≈Redge cos²(πy/L) guided the sweep; the final inset was selected from actual full-wave responses.

## Solver and optimisation

CST Studio Suite 2024 HF Time Domain (Hex), PBA, 130–170 GHz, 50-ohm S-parameter normalization, one quasi-TEM waveguide port feeding in positive y. The port is at y=−1.2 mm, x=±0.25 mm, z=−0.002 to 0.24 mm. It encloses the launch signal, dielectric and ground reference. The five non-feed boundaries use expanded open; ymin is open with the physical feed port. The PML spacing reference is 130 GHz. The final energy-decay criterion is -60 dB. Farfields use the global enclosing calculation surface (MonitorFarFieldsNearToModel=False); the near-model surface was rejected after independent normalization checks. Final monitor definitions and mesh parameters are stored in the project and JSON exports.

The controlled sequence was: reproduce original failure; reverse the invalid excitation and observe inadequate uniform port length; reconstruct a correct launch; sweep inset depths 0.13, 0.15, 0.17 and 0.19 mm; shorten patch length from 0.521 to 0.513 mm; refine mesh; final rerun and reopen. The first clean baseline gave −10.18 dB minimum S11; inset 0.19 mm gave −26.82 dB, and length tuning centred the band. The very deep coarse-grid S11 null was not taken as convergence evidence. A near-model integration-surface test produced a 29% full-sphere normalization discrepancy and was rejected. The accepted mesh pair uses the global enclosing surface and -60 dB energy criterion, reducing the spherical normalization discrepancy below 0.1%.

## Mesh comparison

| Mesh | Cells | S11-min GHz | Dmax at 150 GHz (dBi) | S11 at 150 GHz (dB) |
|---|---:|---:|---:|---:|
| Box_Coarse | 76860 | 149.680 | 7.4974 | -23.963 |
| Box_Fine | 262197 | 148.840 | 7.4602 | -13.424 |

Between the last two meshes, the S11-minimum frequency changes by 0.5644% and 150 GHz directivity by 0.0373 dB. Targets are <1% and <0.2 dB, respectively. Mesh tests apply to the same geometry and global farfield integration setting; parameter optimization runs are not counted as mesh convergence. These targets apply at the operating point. Off-band patterns can show larger differences, and the depth of a sharp S11 null is more mesh-sensitive than its frequency; the minimum S11 depth is not claimed converged to its displayed digits.

## Radiation patterns and frequency results

The broadside field is y-polarized: at θ=0, φ=0 the exported Eφ component dominates Eθ. Consequently the E-plane is yz (φ=90°/270°) and H-plane xz (φ=0°/180°). The 2° full-sphere grid places the maximum at θ=4°, φ=264°; angular precision is limited by that sampling. Pattern curves show total directivity in dBi, not normalized-to-zero gain. Negative values in low-radiation directions are physically meaningful.

| GHz | S11 dB | Dmax dBi | Realized gain dBi | ηrad % |
|---:|---:|---:|---:|---:|
| 130 | -0.707 | 5.143 | -7.443 | 36.70 |
| 140 | -1.582 | 6.553 | -1.014 | 57.36 |
| 146 | -6.428 | 7.207 | 4.581 | 70.72 |
| 147 | -9.542 | 7.283 | 5.328 | 71.71 |
| 148 | -15.908 | 7.350 | 5.818 | 72.12 |
| 149 | -30.146 | 7.410 | 5.982 | 72.05 |
| 150 | -13.424 | 7.460 | 5.804 | 71.55 |
| 151 | -8.540 | 7.500 | 5.332 | 70.57 |
| 152 | -5.971 | 7.532 | 4.658 | 69.04 |
| 153 | -4.435 | 7.557 | 3.887 | 67.13 |
| 154 | -3.444 | 7.570 | 3.088 | 65.06 |
| 160 | -1.381 | 7.491 | -1.080 | 51.03 |
| 170 | -0.889 | 6.993 | -4.702 | 36.57 |

The largest realized gain among these evaluated frequencies is 5.9816 dBi at 149 GHz. The largest angular directivity among all frequency samples is 7.5703 dBi at 154 GHz; this sweep maximum is not substituted for performance at the selected matched operating point. All points in this table are CST monitor calculations. Lines on frequency plots only connect samples; they do not imply separately simulated farfields at every frequency. S11 is exported on the solver's 1001-point frequency grid. The matched-band monitor subset demonstrates the directivity margin at those evaluated frequencies; continuous-band compliance is not asserted between unsampled points.

## Limitations and validation

See Simulation_Validation.md for power balance, full-sphere normalization, warning review and reopening evidence. Material assumptions and finite numerical residuals limit accuracy. This is an engineering simulation design, not a manufacturing-qualified or experimentally validated D-band device.
