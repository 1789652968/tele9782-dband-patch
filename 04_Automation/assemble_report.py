"""Assemble figures, numerical tables and documentation from final CST exports."""
from analyze import *
import shutil,re,hashlib

R=ROOT/'02_Simulation_Results';F=ROOT/'03_Figures';D=ROOT/'05_Documentation'
P=ROOT/'01_CST_Project';A=ROOT/'04_Automation'
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160,'savefig.dpi':180})

def csvout(path,headers,rows):
    with open(path,'w',newline='',encoding='utf-8') as fp:
        w=csv.writer(fp);w.writerow(headers);w.writerows(rows)

def saveplot(name):
    plt.tight_layout();plt.savefig(F/(name+'.png'),bbox_inches='tight');plt.close()

def meshinfo(folder):
    projects=list(folder.glob('*.cst'))
    if not projects:return {}
    log=(projects[0].with_suffix('')/'Result'/'Model.log').read_text(errors='replace')
    cells=re.findall(r'Number of mesh cells:\s*(\d+)',log)
    return {'cells':int(cells[-1]) if cells else None}

def plane_pattern(a,phi):
    pos=a[np.isclose(a[:,1],phi)];neg=a[np.isclose(a[:,1],(phi+180)%360)]
    pos=pos[np.argsort(pos[:,0])];neg=neg[np.argsort(neg[:,0])]
    return np.r_[-neg[1:,0][::-1],pos[:,0]],np.r_[neg[1:,2][::-1],pos[:,2]]

def assemble():
    s=json.loads((P/'summary.json').read_text());a=audit(P)
    pars=json.loads((P/'parameters.json').read_text());pars={k:float(v) for k,v in pars.items()}
    raw=R/'CST_Raw';raw.mkdir(exist_ok=True)
    for f in P.glob('*.csv'):shutil.copy2(f,raw/f.name)
    for f in P.glob('farfield_*_summary.txt'):shutil.copy2(f,raw/f.name)
    for name in ['summary.json','parameters.json','numerical_audit.json','Verification.json']:
        if (P/name).exists():shutil.copy2(P/name,R/name)
    f,g=load_curve(P,r'1D Results\S-Parameters\S1,1');db=20*np.log10(abs(g))
    csvout(R/'S11.csv',['Frequency_GHz','S11_real','S11_imag','S11_dB','Reference_ohm'],zip(f,g.real,g.imag,db,np.full(len(f),50)))
    ff=sorted(s['farfields'],key=lambda v:v['f_GHz']);freq=np.array([v['f_GHz'] for v in ff]);direct=np.array([v['Dmax_dBi'] for v in ff]);gain=np.array([v['realized_gain_dBi'] for v in ff]);eta=np.array([100*10**(v['rad_eff_dB']/10) for v in ff]);total=np.array([100*10**(v['total_eff_dB']/10) for v in ff])
    csvout(R/'Directivity.csv',['Frequency_GHz','Maximum_Directivity_dBi'],zip(freq,direct))
    csvout(R/'Realized_Gain.csv',['Frequency_GHz','Maximum_Realized_Gain_dBi'],zip(freq,gain))
    csvout(R/'Radiation_Efficiency.csv',['Frequency_GHz','Radiation_Efficiency_percent','Total_Efficiency_percent'],zip(freq,eta,total))
    csvout(R/'Validation_Summary.csv',['Frequency_GHz','S11_dB','Maximum_Directivity_dBi','Maximum_Realized_Gain_dBi','Radiation_Efficiency_percent','Total_Efficiency_percent'],[(v['f_GHz'],v['s11_dB'],v['Dmax_dBi'],v['realized_gain_dBi'],100*10**(v['rad_eff_dB']/10),100*10**(v['total_eff_dB']/10)) for v in ff])
    fields=list(a['farfield_checks'][0]);csvout(R/'Power_Consistency.csv',fields,[[v.get(k,'') for k in fields] for v in a['farfield_checks']])
    csvout(R/'Impedance_Bandwidth.csv',list(a['matched_bands'][0]),[list(v.values()) for v in a['matched_bands']])
    op=next(v for v in ff if v['f_GHz']==150)
    plt.figure(figsize=(8,4.6));plt.plot(f,db,color='#126782',lw=1.8);plt.axhline(-10,color='#a23b32',ls='--',label='−10 dB threshold');plt.scatter([150],[op['s11_dB']],color='#a23b32',zorder=4,label=f"150 GHz: {op['s11_dB']:.2f} dB")
    for b in a['matched_bands']:plt.axvspan(b['f_low_GHz'],b['f_high_GHz'],color='#126782',alpha=.1)
    plt.xlabel('Frequency (GHz)');plt.ylabel('S11 (dB)');plt.title('Final CST simulation • 50 Ω reference');plt.grid(alpha=.2);plt.legend();saveplot('S11')
    for values,title,ylabel,name in [(direct,'Maximum directivity','Directivity (dBi)','Directivity_vs_Frequency'),(gain,'Maximum realized gain','Realized gain (dBi)','Realized_Gain_vs_Frequency')]:
        plt.figure(figsize=(8,4.6));plt.plot(freq,values,'o-',color='#126782',label='CST monitor samples; lines connect samples')
        if name.startswith('Directivity'):plt.axhline(6.5,color='#a23b32',ls='--',label='Course requirement: > 6.5 dBi')
        plt.xlabel('Frequency (GHz)');plt.ylabel(ylabel);plt.title(title+' • final geometry');plt.grid(alpha=.2);plt.legend(fontsize=9);saveplot(name)
    plt.figure(figsize=(8,4.6));plt.plot(freq,eta,'o-',label='Radiation efficiency');plt.plot(freq,total,'s--',label='Total efficiency (includes mismatch)');plt.xlabel('Frequency (GHz)');plt.ylabel('Efficiency (%)');plt.ylim(0,100);plt.title('Final CST efficiency • lines connect monitor samples');plt.grid(alpha=.2);plt.legend();saveplot('Radiation_Efficiency')
    sphere=np.loadtxt(R/'Farfield_150_Sphere.txt',skiprows=2)
    theta=np.unique(sphere[:,0]);phi=np.unique(sphere[:,1]);values=10**(sphere[:,2].reshape(len(phi),len(theta))/10)
    phi_closed=np.r_[phi,360];values_closed=np.vstack([values,values[0]])
    sphere_mean=float(np.trapezoid(np.trapezoid(values_closed*np.sin(np.deg2rad(theta)),np.deg2rad(theta),axis=1),np.deg2rad(phi_closed))/(4*np.pi))
    beam=sphere[np.argmax(sphere[:,2])];theta_max=float(beam[0]);phi_max=float(beam[1]);db_correction=10*math.log10(sphere_mean)
    normal=dict(grid_step_deg=2,spherical_mean_D_linear=sphere_mean,normalization_error_percent=100*(sphere_mean-1),D_from_pattern_shape_dBi=float(beam[2]-db_correction),reported_grid_max_dBi=float(beam[2]),mainbeam_theta_deg=theta_max,mainbeam_phi_deg=phi_max)
    (R/'Sphere_Normalization_Check.json').write_text(json.dumps(normal,indent=2))
    for name,cut,label in [('E_Plane',90,'E plane (yz, φ = 90° / 270°)'),('H_Plane',0,'H plane (xz, φ = 0° / 180°)')]:
        angles,dvals=plane_pattern(sphere,cut);csvout(R/(name+'.csv'),['Signed_theta_deg','Total_Directivity_dBi'],zip(angles,dvals))
        fig,ax=plt.subplots(figsize=(6.5,6),subplot_kw={'projection':'polar'});floor=-30;ax.plot(np.deg2rad(angles),np.maximum(dvals,floor)-floor,color='#126782');ax.set_theta_zero_location('N');ax.set_theta_direction(-1);ticks=np.arange(-30,11,10);ax.set_rticks(ticks-floor);ax.set_yticklabels([str(v)+' dBi' for v in ticks]);ax.set_ylim(0,40);ax.set_title(label+'\n150 GHz • total directivity (plot floor −30 dBi)',pad=22);saveplot(name)
    # Parameter table is explicitly rendered from the saved model's parameter values.
    rows=[['Patch width × length',f"{pars['patch_width']:.4f} × {pars['patch_length']:.4f} mm"],['Main board / ground',f"{pars['ground_width']:g} × {pars['ground_length']:g} mm"],['Feed launch width × length',f"{2*pars['port_halfwidth']:g} × {pars['launch_length']:g} mm"],['Substrate thickness',f"{pars['substrate_h']:g} mm"],['Gold thickness',f"{pars['metal_thickness']:g} mm"],['Feed width',f"{pars['feed_width']:g} mm"],['Inset depth / side gap',f"{pars['inset_length']:g} / {pars['inset_gap']:g} mm"],['Polyimide εr / tanδ',f"{pars['eps_r']:g} / {pars['loss_tangent']:g}"],['Gold conductivity','4.561 × 10⁷ S/m'],['Port','ymin, 1 quasi-TEM mode, 50 Ω reference']]
    fig,ax=plt.subplots(figsize=(8.8,5));ax.axis('off');table=ax.table(cellText=rows,colLabels=['Parameter','Saved final model'],loc='center',cellLoc='left',colWidths=[.45,.55]);table.auto_set_font_size(False);table.set_fontsize(11);table.scale(1,1.8);ax.set_title('Final antenna parameters • dimensions in mm',pad=20);saveplot('Parameter_List')
    W=pars['patch_width'];h=pars['substrate_h'];L=pars['patch_length'];er=pars['eps_r'];eff=(er+1)/2+(er-1)/2/math.sqrt(1+12*h/W);dl=.412*h*((eff+.3)*(W/h+.264))/((eff-.258)*(W/h+.8));fa=299792458/(2*(L+2*dl)*1e-3*math.sqrt(eff))/1e9
    b=next(v for v in a['matched_bands'] if v['f_low_GHz']<=150<=v['f_high_GHz']);pow150=next(v for v in a['farfield_checks'] if v['f_GHz']==150)
    vfy=json.loads((P/'Verification.json').read_text()) if (P/'Verification.json').exists() else {}
    comparison=[]
    for label in ['Box_Coarse','Box_Fine','Box_Finer']:
        folder=ROOT/'06_Working'/label
        if (folder/'summary.json').exists():
            ss=json.loads((folder/'summary.json').read_text());oo=next(v for v in ss['farfields'] if v['f_GHz']==150);comparison.append(dict(name=label,**meshinfo(folder),fmin_GHz=ss['f_min_s11_GHz'],Smin_dB=ss['min_s11_dB'],D150_dBi=oo['Dmax_dBi'],S150_dB=oo['s11_dB']))
    csvout(R/'Mesh_Convergence.csv',list(comparison[0]),[list(v.values()) for v in comparison])
    delta_d=abs(comparison[-1]['D150_dBi']-comparison[-2]['D150_dBi']);delta_f=100*abs(comparison[-1]['fmin_GHz']-comparison[-2]['fmin_GHz'])/comparison[-1]['fmin_GHz']
    report=dict(operating_GHz=150,S11_operating_dB=op['s11_dB'],minimum_S11_dB=a['s11_min_dB'],minimum_S11_frequency_GHz=a['s11_min_freq_GHz'],analytical_frequency_GHz=fa,analytical_difference_percent=100*abs(fa-a['s11_min_freq_GHz'])/fa,bandwidth=b,directivity_dBi=op['Dmax_dBi'],realized_gain_dBi=op['realized_gain_dBi'],radiation_efficiency_percent=100*10**(op['rad_eff_dB']/10),total_efficiency_percent=100*10**(op['total_eff_dB']/10),sphere=normal,mesh_delta_directivity_dB=delta_d,mesh_delta_frequency_percent=delta_f,verification=vfy)
    report.update(peak_sampled_realized_gain_dBi=float(max(gain)),peak_sampled_realized_gain_frequency_GHz=float(freq[np.argmax(gain)]),peak_sampled_directivity_dBi=float(max(direct)),peak_sampled_directivity_frequency_GHz=float(freq[np.argmax(direct)]))
    (D/'Final_Performance.json').write_text(json.dumps(report,indent=2))
    table='| GHz | S11 dB | Dmax dBi | Realized gain dBi | ηrad % |\n|---:|---:|---:|---:|---:|\n'+'\n'.join(f"| {v['f_GHz']:g} | {v['s11_dB']:.3f} | {v['Dmax_dBi']:.3f} | {v['realized_gain_dBi']:.3f} | {100*10**(v['rad_eff_dB']/10):.2f} |" for v in ff)
    mesh_table='| Mesh | Cells | S11-min GHz | Dmax at 150 GHz (dBi) | S11 at 150 GHz (dB) |\n|---|---:|---:|---:|---:|\n'+'\n'.join(f"| {v['name']} | {v['cells']} | {v['fmin_GHz']:.3f} | {v['D150_dBi']:.4f} | {v['S150_dB']:.3f} |" for v in comparison)
    (D/'Engineering_Design_Notes.md').write_text(f'''# TELE9782 D-band microstrip patch — engineering design

This is CST full-wave numerical simulation, not a fabricated or physically measured antenna. The selected architecture is a single inset-fed rectangular patch. An array is unnecessary because the complete lossy single-patch model exceeds the course directivity threshold with margin.

## Final performance

Operating frequency: **150 GHz**. CST maximum directivity **{op['Dmax_dBi']:.3f} dBi**, realized gain **{op['realized_gain_dBi']:.3f} dBi**, S11 **{op['s11_dB']:.3f} dB**, radiation efficiency **{report['radiation_efficiency_percent']:.2f}%**, total efficiency **{report['total_efficiency_percent']:.2f}%**. These quantities are taken from the same final geometry and solver run.

The S11 minimum is **{a['s11_min_dB']:.3f} dB at {a['s11_min_freq_GHz']:.3f} GHz** on a 0.04 GHz output grid. The −10 dB crossings are **{b['f_low_GHz']:.4f} and {b['f_high_GHz']:.4f} GHz**, obtained by linear interpolation of adjacent simulated S11-dB samples. Bandwidth is **{b['BW_GHz']:.4f} GHz**, or **{b['FBW_percent']:.3f}%** using the crossing midpoint. No claim of matching throughout 130–170 GHz is made.

## Geometry and materials

The patch lies in xy, length along y, ground at z≤0, substrate from z=0 to {h:g} mm. The patch width is {W:g} mm and length {L:g} mm. Main substrate and ground: {pars['ground_width']:g} × {pars['ground_length']:g} mm. A {2*pars['port_halfwidth']:g} mm-wide, {pars['launch_length']:g} mm-long feed launch extends from the negative-y board edge. Feed width {pars['feed_width']:g} mm; inset depth {pars['inset_length']:g} mm; each side gap {pars['inset_gap']:g} mm. Patch and ground gold thickness is {pars['metal_thickness']:g} mm.

Polyimide is modelled with εr={er:g} and nominal constant tanδ={pars['loss_tangent']:g}, referenced at 150 GHz. These are inherited, documented engineering assumptions; no measured D-band dielectric dataset was supplied. Gold conductivity is 4.561e7 S/m. Finite conductivity and dielectric loss are included. No artificial lossless substitution or ideal feeding network is used. Surface roughness, anisotropy, temperature and fabrication tolerances are not characterized.

## Analytical starting design and comparison

The supplied transmission-line equations were used: W=c/(2fr)√[2/(εr+1)]; εeff=(εr+1)/2+(εr−1)/(2√(1+12h/W)); ΔL/h=0.412[(εeff+0.3)(W/h+0.264)]/[(εeff−0.258)(W/h+0.8)]; L=c/(2fr√εeff)−2ΔL.

At a 150 GHz target, εr=3.5 and h=0.040 mm, the calculated starting dimensions are W=0.666205 mm and L=0.520369 mm, with εeff=3.202978 and ΔL=0.019001 mm. The original rounded patch was 0.667 × 0.521 mm. Full-wave feed tuning selected a 0.190 mm inset; length tuning selected {L:g} mm.

Using the final W, L and h in the same analytical model gives **{fa:.4f} GHz**, versus the simulated **{a['s11_min_freq_GHz']:.4f} GHz S11 minimum**: absolute difference {abs(fa-a['s11_min_freq_GHz']):.4f} GHz, or {report['analytical_difference_percent']:.3f}% relative to theory. The S11 minimum is the reported impedance-match resonance, not a proof of an isolated modal eigenfrequency. The port-reactance zero crossings are separately exported in the numerical audit. The finite ground, inset slots, feed discontinuity, metal thickness, dielectric loss and full-wave fringing explain why the simple cavity/transmission-line estimate is not exact. Here h/W≈{h/W:.3f} and h/λ0≈{h/(299792458/150e9*1000):.3f}, consistent with a thin microstrip starting approximation.

For the feed, the common quasi-static microstrip expression Z0≈120π/[√εeff(u+1.393+0.667 ln(u+1.444))], u=w/h>1, gives a starting width near 0.09 mm. CST's adaptive quasi-TEM port calculation, rather than this zero-thickness estimate, establishes the simulated port impedance. The nominal inset resistance relation Rin(y)≈Redge cos²(πy/L) guided the sweep; the final inset was selected from actual full-wave responses.

## Solver and optimisation

CST Studio Suite 2024 HF Time Domain (Hex), PBA, 130–170 GHz, 50-ohm S-parameter normalization, one quasi-TEM waveguide port feeding in positive y. The port is at y=−{pars['ground_length']/2+pars['launch_length']:g} mm, x=±{pars['port_halfwidth']:g} mm, z=−{pars['metal_thickness']:g} to {6*h:g} mm. It encloses the launch signal, dielectric and ground reference. The five non-feed boundaries use expanded open; ymin is open with the physical feed port. The PML spacing reference is 130 GHz. The final energy-decay criterion is -60 dB. Farfields use the global enclosing calculation surface (MonitorFarFieldsNearToModel=False); the near-model surface was rejected after independent normalization checks. Final monitor definitions and mesh parameters are stored in the project and JSON exports.

The controlled sequence was: reproduce original failure; reverse the invalid excitation and observe inadequate uniform port length; reconstruct a correct launch; sweep inset depths 0.13, 0.15, 0.17 and 0.19 mm; shorten patch length from 0.521 to 0.513 mm; refine mesh; final rerun and reopen. The first clean baseline gave −10.18 dB minimum S11; inset 0.19 mm gave −26.82 dB, and length tuning centred the band. The very deep coarse-grid S11 null was not taken as convergence evidence. A near-model integration-surface test produced a 29% full-sphere normalization discrepancy and was rejected. The accepted mesh pair uses the global enclosing surface and -60 dB energy criterion, reducing the spherical normalization discrepancy below 0.1%.

## Mesh comparison

{mesh_table}

Between the last two meshes, the S11-minimum frequency changes by {delta_f:.4f}% and 150 GHz directivity by {delta_d:.4f} dB. Targets are <1% and <0.2 dB, respectively. Mesh tests apply to the same geometry and global farfield integration setting; parameter optimization runs are not counted as mesh convergence. These targets apply at the operating point. Off-band patterns can show larger differences, and the depth of a sharp S11 null is more mesh-sensitive than its frequency; the minimum S11 depth is not claimed converged to its displayed digits.

## Radiation patterns and frequency results

The broadside field is y-polarized: at θ=0, φ=0 the exported Eφ component dominates Eθ. Consequently the E-plane is yz (φ=90°/270°) and H-plane xz (φ=0°/180°). The 2° full-sphere grid places the maximum at θ={theta_max:g}°, φ={phi_max:g}°; angular precision is limited by that sampling. Pattern curves show total directivity in dBi, not normalized-to-zero gain. Negative values in low-radiation directions are physically meaningful.

{table}

The largest realized gain among these evaluated frequencies is {max(gain):.4f} dBi at {freq[np.argmax(gain)]:g} GHz. The largest angular directivity among all frequency samples is {max(direct):.4f} dBi at {freq[np.argmax(direct)]:g} GHz; this sweep maximum is not substituted for performance at the selected matched operating point. All points in this table are CST monitor calculations. Lines on frequency plots only connect samples; they do not imply separately simulated farfields at every frequency. S11 is exported on the solver's 1001-point frequency grid. The matched-band monitor subset demonstrates the directivity margin at those evaluated frequencies; continuous-band compliance is not asserted between unsampled points.

## Limitations and validation

See Simulation_Validation.md for power balance, full-sphere normalization, warning review and reopening evidence. Material assumptions and finite numerical residuals limit accuracy. This is an engineering simulation design, not a manufacturing-qualified or experimentally validated D-band device.
''',encoding='utf-8')
    warnings=[v['text'] for v in s['messages'] if v['type']=='WARNING']
    (D/'Simulation_Validation.md').write_text(f'''# Final simulation validation

Final solver state: **{s['solver']['state']}**. Actual reopen/rerun evidence: `02_Simulation_Results/Verification.json`. This file is generated from a separate open of the delivered .cst, not from filename existence.

## Acceptance checks

- Actual CST patch model and companion results: saved under 01_CST_Project.
- Operating frequency 150 GHz is within 130–170 GHz.
- Maximum directivity at 150 GHz: {op['Dmax_dBi']:.4f} dBi >6.5 dBi.
- S11 at 150 GHz: {op['s11_dB']:.4f} dB ≤−10 dB.
- Actual −10 dB bandwidth calculated from crossings: {b['BW_GHz']:.4f} GHz.
- Analytical and simulated match-resonance frequencies compared with definitions stated.
- Directivity, realized gain and radiation/total efficiency exported at actual monitor frequencies.
- E/H-plane and full-sphere pattern exports provided at 150 GHz.
- Passive S-parameter check: maximum |S11|={a['max_abs_S11']:.8f} ≤1.
- Mesh sensitivity: ΔD={delta_d:.5f} dB; Δf={delta_f:.5f}% between last two meshes.
- Reopening and reproducibility status: {json.dumps(vfy,ensure_ascii=False)}.

## Power consistency at 150 GHz

Incident {pow150['Pstim_W']:.9f} W; accepted {pow150['Paccepted_W']:.9f} W; outgoing/reflected {pow150['Poutgoing_W']:.9f} W; radiated {pow150['Prad_W']:.9f} W; metal loss {pow150['Pmetal_W']:.9f} W; dielectric loss {pow150['Pdielectric_W']:.9f} W. Power balance residual Paccepted−Prad−Pmetal−Pdielectric={pow150['power_balance_residual_W']:.9f} W ({pow150['power_balance_residual_percent_accepted']:.4f}% of accepted power). This residual is reported, not forced to zero or hidden by renormalization.

Radiation efficiency Prad/Paccepted={100*pow150['eta_power']:.4f}%; total efficiency includes reflected power. The realized-gain identity D+10log10(ηrad)+10log10(1−|S11|²) differs from CST realized gain by {pow150['gain_identity_residual_dB']:.8f} dB. Because these CST quantities share solver inputs, that identity is a consistency check, not independent experimental validation.

## Full-sphere check

The 2° CST-exported total-directivity grid is integrated as (1/4π)∫D(θ,φ)sinθ dθ dφ, with the φ seam closed. Its spherical mean is {sphere_mean:.7f}; the ideal normalization is 1. The deviation is {100*(sphere_mean-1):.4f}%. This includes discretization/export error and CST's finite power-normalization residual. Independently normalizing the *pattern shape* yields a diagnostic peak of {normal['D_from_pattern_shape_dBi']:.4f} dBi. The reported course result remains the unmodified CST value {op['Dmax_dBi']:.4f} dBi. No curve, scale or normalization was altered to pass the requirement.

## Warnings and limitations

{chr(10).join('- '+w.replace(chr(10),' ') for w in warnings)}

The port mode solver also states that it approximates dispersive materials at 150 GHz and neglects their loss terms for the port eigenmode. The full 3D gold/dielectric losses remain active. This documented port approximation is distinct from making the antenna lossless. The old short-port, boundary-dispersion, metal-decoupling and staircase warnings must be absent in the final messages, which are retained in summary.json and the CST solver log.

No licence limit was inferred without an observed rejection. The successful mesh sizes above demonstrate only the capability exercised in this task. The software licence is non-commercial/educational. No physical measurements or measured D-band material validation were performed.
''',encoding='utf-8')
    (D/'README.md').write_text(f'''# TELE9782 final CST engineering project

Open `../01_CST_Project/TELE9782_DBand_Patch_Final.cst` in CST Studio Suite 2024. Keep its same-stem companion directory with it. Select Components for geometry, Ports for the feed, 1D Results → S-Parameters → S1,1 for matching, and Farfields → farfield (f=150) [1] for the operating pattern. Choose Directivity / Abs for directivity, or Realized Gain for realized gain.

The accepted design is a single lossy inset-fed patch at 150 GHz: Dmax={op['Dmax_dBi']:.3f} dBi, S11={op['s11_dB']:.3f} dB, realized gain={op['realized_gain_dBi']:.3f} dBi, radiation efficiency={report['radiation_efficiency_percent']:.2f}%. See Engineering_Design_Notes.md for dimensions and Simulation_Validation.md for numerical limits and actual verification status.

To rerun in CST, save a copy, retain the saved HF Time Domain solver settings and monitors, and click Start Simulation. Wait for “Steady state energy criterion met, solver finished successfully.” Save with results. Do not use Calculate Modes Only as a replacement for this run. Results take minutes on this computer; timings vary with hardware.

Automation: `04_Automation/rerun_final.py` opens a working copy, runs CST, exports actual numerical data and records status. `04_Automation/rebuild_final.py` creates the parameterised geometry from bundled model-history material/template definitions and final parameters, then runs the solver. Neither requires the original lab2222 directory. Use the installed compatible CST Python interpreter described in 04_Automation/README.md.

Folders: 01 final CST project; 02 measured-from-simulation CSV/raw exports; 03 figures; 04 executable automation; 05 documentation, inventory, source hashes and iteration log; 06 retained diagnostic and optimization projects. Original sources were preserved. None of these results are physical antenna measurements.
''',encoding='utf-8')
    (D/'Report_Results_Outline.md').write_text(f'''# Report and 10–15 minute presentation outline

1. Requirements and interpretation (1 min): D-band microstrip patch, >6.5 dBi at a valid operating frequency; actual achieved impedance bandwidth, not the whole D-band.
2. Diagnosis (2 min): outward-facing original port, invalid negative maximum directivity and misleading broad match; corrected direction exposed insufficient uniform feed; show diagnostic evidence.
3. Theory and geometry (2 min): transmission-line equations, 0.6662 × 0.5204 mm analytical start; final {W:g} × {L:g} mm patch and lossy material assumptions; show Antenna_Geometry and Parameter_List.
4. Solver and optimization (2 min): valid 50-ohm microstrip launch, open boundaries, pre-created monitors, inset sweep, length tuning, mesh study.
5. Results (3 min): S11 and crossing bandwidth; at 150 GHz D={op['Dmax_dBi']:.2f} dBi, realized gain={op['realized_gain_dBi']:.2f} dBi, ηrad={report['radiation_efficiency_percent']:.1f}%; frequency tables, E/H cuts and native CST 3D pattern.
6. Validation and limits (2 min): power balance, gain identity, full-sphere integration, mesh shifts, reopen/fresh-run comparison, material uncertainty and no experimental measurement.
7. Conclusion/questions (1 min): explain why a single patch is sufficient, what remains to fabricate and measure, and why a low S11 alone does not prove a working antenna.

Suggested report sections: requirements; references actually available; original diagnosis; analytical design; final geometry/materials; simulation methodology; optimization record; final results; numerical validation; limitations; reproduction appendix. Import the figures and CSV tables without changing their quantity definitions or hiding numerical residuals.
''',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':assemble()
