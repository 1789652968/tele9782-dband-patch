# TELE9782 final CST engineering project

Open `../01_CST_Project/TELE9782_DBand_Patch_Final.cst` in CST Studio Suite 2024. Keep its same-stem companion directory with it. Select Components for geometry, Ports for the feed, 1D Results → S-Parameters → S1,1 for matching, and Farfields → farfield (f=150) [1] for the operating pattern. Choose Directivity / Abs for directivity, or Realized Gain for realized gain.

The accepted design is a single lossy inset-fed patch at 150 GHz: Dmax=7.460 dBi, S11=-13.424 dB, realized gain=5.804 dBi, radiation efficiency=71.55%. See Engineering_Design_Notes.md for dimensions and Simulation_Validation.md for numerical limits and actual verification status.

To rerun in CST, save a copy, retain the saved HF Time Domain solver settings and monitors, and click Start Simulation. Wait for “Steady state energy criterion met, solver finished successfully.” Save with results. Do not use Calculate Modes Only as a replacement for this run. Results take minutes on this computer; timings vary with hardware.

Automation: `04_Automation/rerun_final.py` opens a working copy, runs CST, exports actual numerical data and records status. `04_Automation/rebuild_final.py` creates the parameterised geometry from bundled model-history material/template definitions and final parameters, then runs the solver. Neither requires the original lab2222 directory. Use the installed compatible CST Python interpreter described in 04_Automation/README.md.

Folders: 01 final CST project; 02 measured-from-simulation CSV/raw exports; 03 figures; 04 executable automation; 05 documentation, inventory, source hashes and iteration log; 06 retained diagnostic and optimization projects. Original sources were preserved. None of these results are physical antenna measurements.
