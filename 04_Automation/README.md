# Reproducible CST automation

The native CST scripts use the installed CST 2024 Python API. The tested compatible interpreter is:
`D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe` (Python 3.9.15).

In PowerShell, from this folder:

```powershell
& 'D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe' .\rerun_final.py
```

This creates a timestamped reproduction copy under 06_Working, runs the actual solver, exports S11, powers and monitor results, and checks reopening. It preserves the delivered final .cst. Keep the CST window available if an interactive warning requires review. Solver success is explicitly checked; script execution by itself is not success evidence.

To reconstruct from geometry definitions, use the same interpreter with `rebuild_final.py`. The bundled Reference_ModelHistory.json supplies the original material/template definitions, and 02_Simulation_Results/parameters.json supplies the accepted geometry and mesh parameters. No access to lab2222 or the old F: drive is required. The global enclosing farfield integration surface and -60 dB energy criterion are included in the builder.

The software location can be changed with `CST_INSTALLPATH_2024`. Use a Python version supported by that CST installation. Do not pip-install an unrelated package named cst as a substitute for the vendor libraries.

Optional analysis/report scripts require NumPy and Matplotlib. They read genuine CST CSV/farfield exports and never synthesize antenna data. On this computer these were run with the Spyder runtime Python 3.12, NumPy 2.4.3 and Matplotlib 3.10.8; its Library/bin directory must be on PATH. These plotting dependencies are not needed to open or rerun the .cst in CST.

The retained iteration projects under 06_Working and Iteration_Log.csv document the actual feed sweep and mesh tests. Early near-model-surface runs are explicitly diagnostic and rejected for final farfield normalization. Original-source hashes and an integrity check are in 05_Documentation.
