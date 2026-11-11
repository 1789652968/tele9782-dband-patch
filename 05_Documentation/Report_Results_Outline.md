# Report and 10–15 minute presentation outline

1. Requirements and interpretation (1 min): D-band microstrip patch, >6.5 dBi at a valid operating frequency; actual achieved impedance bandwidth, not the whole D-band.
2. Diagnosis (2 min): outward-facing original port, invalid negative maximum directivity and misleading broad match; corrected direction exposed insufficient uniform feed; show diagnostic evidence.
3. Theory and geometry (2 min): transmission-line equations, 0.6662 × 0.5204 mm analytical start; final 0.667 × 0.513 mm patch and lossy material assumptions; show Antenna_Geometry and Parameter_List.
4. Solver and optimization (2 min): valid 50-ohm microstrip launch, open boundaries, pre-created monitors, inset sweep, length tuning, mesh study.
5. Results (3 min): S11 and crossing bandwidth; at 150 GHz D=7.46 dBi, realized gain=5.80 dBi, ηrad=71.6%; frequency tables, E/H cuts and native CST 3D pattern.
6. Validation and limits (2 min): power balance, gain identity, full-sphere integration, mesh shifts, reopen/fresh-run comparison, material uncertainty and no experimental measurement.
7. Conclusion/questions (1 min): explain why a single patch is sufficient, what remains to fabricate and measure, and why a low S11 alone does not prove a working antenna.

Suggested report sections: requirements; references actually available; original diagnosis; analytical design; final geometry/materials; simulation methodology; optimization record; final results; numerical validation; limitations; reproduction appendix. Import the figures and CSV tables without changing their quantity definitions or hiding numerical residuals.
