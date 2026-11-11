# TELE9782 · D-Band Microstrip Patch Antenna

Study materials for the TELE9782 project presentation by Hanqing Zhao and Ning Mao.

The CST model achieved **7.460 dBi maximum directivity at 150 GHz**, clearing the **6.5 dBi** requirement by **0.960 dB**. At that same operating point, S11 was **−13.424 dB** and realized gain was **5.804 dBi**. These are simulated results.

## Start here

1. [中文设计教程](06_Presentation/TELE9782_Design_Explained_CN.pdf) — derive the patch dimensions, understand inset matching, and verify the 6.5 dBi target.
2. [Presentation slides](06_Presentation/TELE9782_DBand_Patch_Presentation.pdf) — 10 main slides and 7 technical backup slides.
3. [Two-speaker script](06_Presentation/TELE9782_Presentation_Script.pdf) — five minutes per speaker.
4. [42 technical Q&A](06_Presentation/TELE9782_Technical_QA.pdf) — English oral answers, Chinese explanations and references.
5. [Speaker cue cards](06_Presentation/TELE9782_Speaker_Cue_Cards.docx) — use for the timed rehearsal.

Editable versions are included. The [evidence map](06_Presentation/Presentation_Evidence_Map.md) and [review](06_Presentation/Presentation_Review.md) document verification and refer to the local engineering source files.


## Engineering source files

- [Final CST project](01_CST_Project/TELE9782_DBand_Patch_Final.cst) and its same-name companion directory. Download the repository as a ZIP, extract it, and open the CST file in CST Studio Suite 2024 with the companion directory beside it.
- [Numerical exports](02_Simulation_Results), [figures](03_Figures), [automation](04_Automation), and [design notes](05_Documentation).
- [Optimisation and validation working projects](06_Working). Early and rejected diagnostic runs are documented in the iteration log.
- [Original D-band patch](07_Original_Patch) for comparison with the final model.

Use the scripts in 04_Automation to rebuild or rerun a copy. Installation files, transient CST caches and lock files, and the unrelated dipole lab are outside this repository.
