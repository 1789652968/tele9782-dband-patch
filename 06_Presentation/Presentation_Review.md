# Presentation review

## Timing and presenter allocation

| Slides | Presenter | Clock | Assigned time | Spoken words |
|---|---|---|---:|---:|
| 1–5 | Hanqing Zhao | 00:00–05:00 | 300 s | 601 |
| 6–10 | Ning Mao | 05:00–10:00 | 300 s | 570 |

The 1,171-word count includes transitions and excludes pronunciation notes and appendix responses. The script uses a 5:00 handover and a 10:00 close. Timing is planned from the script. The presenters should confirm it with a spoken rehearsal. Slides 11–17 and 42 bilingual technical questions are for the separate Q&A.

## Coverage of assessed results

| Requirement | Main slides | Evidence |
|---|---|---|
| Analytical frequency compared with simulation | 3–4, 7 | 152.000 GHz final-size estimate versus 148.840 GHz simulated match dip, 2.08% below theory |
| S11 and −10 dB bandwidth | 7 | 1001-point trace, −13.424 dB at 150 GHz, 147.106–150.619 GHz, 3.513 GHz / 2.36% |
| Directivity and realized gain versus frequency | 8 | 13 sampled monitors, 7.460 dBi and 5.804 dBi at 150 GHz |
| Radiation efficiency versus frequency | 9 | 71.55% at 150 GHz; radiation and total efficiency distinguished |
| E- and H-plane patterns | 9 | Actual total-directivity cuts at 150 GHz, yz and xz respectively |

## Engineering and document checks

- Matched all 1001 S11 values to the original complex CST trace and all 13 reported monitor rows to the directivity, realized gain and efficiency exports.
- Recomputed the analytical starting size, the 152.000 GHz estimate, bandwidth crossings, fractional bandwidth, gain identity, power residual and spherical normalization. The independent integration of the saved 2° angular export gives a linear mean of 0.9991082861 and finds the peak at θ = 4°, φ = 264°.
- Checked parameter/material definitions, solver and mesh history, iteration records, saved rerun verification and CST project hash. The final project SHA-256 agrees with the prior delivery manifest. No engineering file was written or simulation rerun during presentation preparation.
- Historical −20.92 dBi and near-model 8.54 dBi values are rejected diagnostic outputs. The final 49.47 Ω mode impedance is distinguished from the approximate 49.9 Ω baseline and 50 Ω reporting reference.
- Validated the 17-slide, 16:9 editable PowerPoint package. Exported PDFs with desktop PowerPoint and Word and rasterized their pages for layout review. The script follows the 10 main slides and supplies conditional appendix responses. Cue cards were also rendered for review.
- The two-mesh comparison supports the operating-point result. Sharp S11 depth, off-band details, fabricated tolerances and material characterization remain outside that conclusion. All performance is simulated.

## Rehearsal

1. Both presenters read lessons 2–5 and 8–9. Each explains the length calculation, feed matching and directivity/realized-gain distinction aloud without the script.
2. Run the presentation with a timer. At 05:00, Hanqing hands over to Ning. At 10:00, Ning ends on slide 10. Use the cue cards in a second run.
3. Swap roles for the technical Q&A and answer randomly selected questions. Start with the physics, give one numerical result, and use the appendix to show the evidence.
4. Bring the editable PowerPoint and the PDF copy. If asked to demonstrate the solver, open the saved CST model and use the existing results.

The separate TELE9782 Chapter 14 handout was unavailable in the inspected material. The deck uses the transmission-line equations supplied in the project request and cites the published Balanis reference. No lecture-slide content is quoted.

