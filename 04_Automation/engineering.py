"""CST 2024 model creation and actual-result extraction. All lengths in mm."""
import json, math, csv, time, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = Path(__file__).with_name('Reference_ModelHistory.json')

def brick(name, material, xr, yr, zr):
    return f'''With Brick
.Reset
.Name "{name}"
.Component "antenna"
.Material "{material}"
.Xrange "{xr[0]}", "{xr[1]}"
.Yrange "{yr[0]}", "{yr[1]}"
.Zrange "{zr[0]}", "{zr[1]}"
.Create
End With
'''

DEFAULT = dict(patch_width=.667, patch_length=.521, substrate_h=.040,
    feed_width=.090, inset_length=.150, inset_gap=.020, ground_width=1.4,
    ground_length=1.4, metal_thickness=.002, launch_length=.5, port_halfwidth=.25,
    mesh_near=20, mesh_box=30, eps_r=3.5, loss_tangent=.0027)

def build(de, name, changes=None, monitors=None):
    pars=DEFAULT.copy();pars.update(changes or {})
    frequencies=monitors or [130,140,150,160,170]
    p=de.new_mws(); m=p.model3d
    for key,value in pars.items():m.StoreParameter(key,str(value))
    history=json.loads(HISTORY.read_text(encoding='utf-8'))['history']
    template='\n'.join(history[0]['code'])
    m.add_to_history('D-band radiating template',template)
    for item in history:
        if item['caption'].startswith('define material:'):
            code='\n'.join(item['code'])
            if 'Polyimide' in item['caption']:
                code=code.replace('.Epsilon "3.5"','.Epsilon "eps_r"').replace('.TanD "0.0027"','.TanD "loss_tangent"')
                code=code.replace('.SetMaterialUnit "MHz", "mm"','.SetMaterialUnit "GHz", "mm"').replace('.TanDFreq "1.0"','.TanDFreq "150"')
            m.add_to_history(item['caption'],code)
    g='Component.New "antenna"\n'
    g+=brick('ground','Gold',('-ground_width/2','ground_width/2'),('-ground_length/2','ground_length/2'),('-metal_thickness','0'))
    g+=brick('substrate','Polyimide (lossy)',('-ground_width/2','ground_width/2'),('-ground_length/2','ground_length/2'),('0','substrate_h'))
    g+=brick('launch_ground','Gold',('-port_halfwidth','port_halfwidth'),('-ground_length/2-launch_length','-ground_length/2'),('-metal_thickness','0'))
    g+=brick('launch_substrate','Polyimide (lossy)',('-port_halfwidth','port_halfwidth'),('-ground_length/2-launch_length','-ground_length/2'),('0','substrate_h'))
    g+='Solid.Add "antenna:ground", "antenna:launch_ground"\nSolid.Add "antenna:substrate", "antenna:launch_substrate"\n'
    g+=brick('patch','Gold',('-patch_width/2','patch_width/2'),('-patch_length/2','patch_length/2'),('substrate_h','substrate_h+metal_thickness'))
    for side,xrange in [('left',('-feed_width/2-inset_gap','-feed_width/2')),('right',('feed_width/2','feed_width/2+inset_gap'))]:
        g+=brick(side,'Vacuum',xrange,('-patch_length/2','-patch_length/2+inset_length'),('substrate_h','substrate_h+metal_thickness'))
        g+=f'Solid.Subtract "antenna:patch", "antenna:{side}"\n'
    g+=brick('feed','Gold',('-feed_width/2','feed_width/2'),('-ground_length/2-launch_length','-patch_length/2+inset_length'),('substrate_h','substrate_h+metal_thickness'))
    g+='Solid.Add "antenna:patch", "antenna:feed"\n'
    m.add_to_history('Finite lossy inset patch with uniform port launch',g)
    code='''With Boundary
.Ymin "open"
.ReflectionLevel "0.0001"
.MinimumDistanceType "Fraction"
.MinimumDistancePerWavelengthNewMeshEngine "4"
.MinimumDistanceReferenceFrequencyType "User"
.FrequencyForMinimumDistance "130"
End With
With Port
.Reset
.PortNumber "1"
.Label "50ohm_microstrip"
.NumberOfModes "1"
.Coordinates "Free"
.Orientation "ymin"
.PortOnBound "True"
.Xrange "-port_halfwidth", "port_halfwidth"
.Yrange "-ground_length/2-launch_length", "-ground_length/2-launch_length"
.Zrange "-metal_thickness", "6*substrate_h"
.ReferencePlaneDistance "0"
.Create
End With
With Solver
.Method "Hexahedral"
.CalculationType "TD-S"
.StimulationPort "1"
.StimulationMode "1"
.SteadyStateLimit "-60"
.MonitorFarFieldsNearToModel "False"
.MeshAdaption "False"
.AutoNormImpedance "False"
.NormingImpedance "50"
.CalculateModesOnly "False"
.RunDiscretizerOnly "False"
End With
With MeshSettings
.SetMeshType "Hex"
.Set "StepsPerWaveNear", "mesh_near"
.Set "StepsPerWaveFar", "15"
.Set "StepsPerBoxNear", "mesh_box"
.Set "StepsPerBoxFar", "1"
.Set "WavelengthRefinementSameAsNear", "0"
.Set "UseRatioLimitGeometry", "1"
.Set "RatioLimitGeometry", "25"
.Set "EdgeRefinementOn", "1"
.Set "EdgeRefinementPolicy", "1"
.Set "EdgeRefinementRatio", "2"
.Set "EdgeRefinementBufferLines", "3"
.Set "UseDielectrics", "1"
End With
Mesh.ConnectivityCheck "True"
'''
    m.add_to_history('Port, radiation boundary and solver accuracy',code)
    for f in frequencies:
        if f not in [130,140,150,160,170]:
            m.add_to_history(f'Farfield at {f} GHz',f'''With Monitor
.Reset
.Name "farfield (f={f})"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "{f}"
.Create
End With''')
    folder=ROOT/'06_Working'/name;folder.mkdir(exist_ok=True)
    p.save(str(folder/f'{name}.cst'))
    (folder/'parameters.json').write_text(json.dumps(pars,indent=2))
    return p

def result_data(p):
    import cst.results as cr
    p.save()
    r=cr.ProjectFile(p.filename(),allow_interactive=True).get_3d()
    data={}
    for name in r.get_tree_items():
        if any(t in name for t in ['S-Parameters','Power\\','Efficiencies','Balance','Z Matrix','Line Impedance','Reference Impedance']):
            try:
                q=r.get_result_item(name)
                data[name]={'x':list(q.get_xdata()),'y':list(q.get_ydata()),'xlabel':q.xlabel,'ylabel':q.ylabel}
            except Exception as e: print('RESULT_UNAVAILABLE',name,str(e),flush=True)
    return data

def extract(p, label=None):
    m=p.model3d; folder=Path(p.filename()).parent
    data=result_data(p)
    for key,v in data.items():
        filename=key.replace('\\','_').replace('/','_').replace(':','_')+'.csv'
        with open(folder/filename,'w',newline='') as fp:
            w=csv.writer(fp);w.writerow(['x','real','imag']);w.writerows((x,complex(y).real,complex(y).imag) for x,y in zip(v['x'],v['y']))
    v=data[r'1D Results\S-Parameters\S1,1'];x=v['x'];y=v['y']
    k=min(range(len(y)),key=lambda i:abs(y[i]))
    summary={'name':label or Path(p.filename()).stem,'project':p.filename(),'solver':m.get_solver_run_info(),
        'f_min_s11_GHz':x[k],'min_s11_dB':20*math.log10(abs(y[k])), 'farfields':[],'messages':p.get_messages()}
    ff=m.FarfieldPlot
    for item in m.get_tree_items():
        if item.startswith('Farfields\\farfield (f=') and item.endswith('[1]'):
            f=float(item.split('(f=')[1].split(')')[0])
            m.SelectTreeItem(item)
            ff.Reset();ff.Plottype('3d');ff.SetPlotMode('directivity');ff.SelectComponent('Abs');ff.SetScaleLinear(False)
            ff.SetPlotRangeOnly(False);ff.Step(2);ff.Step2(2);ff.Plot()
            row={'f_GHz':f,'Dmax_dBi':ff.GetMax(),'rad_eff_dB':ff.GetRadiationEfficiency(),'total_eff_dB':ff.GetTotalEfficiency(),'Prad_W':ff.GetTRP()}
            ff.ASCIIExportSummary(str(folder/f'farfield_{f:g}_summary.txt'))
            ff.SetPlotMode('realized gain');ff.Plot();row['realized_gain_dBi']=ff.GetMax()
            row['s11_dB']=20*math.log10(abs(y[min(range(len(x)),key=lambda i:abs(x[i]-f))]))
            summary['farfields'].append(row)
    (folder/'summary.json').write_text(json.dumps(summary,indent=2,default=str))
    print('SUMMARY',json.dumps({k:v for k,v in summary.items() if k!='messages'}),flush=True)
    return summary,data

def run(p):
    p.save()
    print('SOLVER_START',p.filename(),flush=True)
    t=time.time()
    try:p.model3d.run_solver()
    except Exception:
        Path(p.filename()).parent.joinpath('failure_messages.json').write_text(json.dumps(p.get_messages(),indent=2))
        raise
    p.save()
    print('SOLVER_END',round(time.time()-t,1),p.model3d.get_solver_run_info(),flush=True)
    return extract(p)

def variant(p,name,changes):
    folder=ROOT/'06_Working'/name;folder.mkdir(exist_ok=True)
    p.save(str(folder/f'{name}.cst'),include_results=False)
    for k,v in changes.items():p.model3d.StoreParameter(k,str(v))
    p.model3d.full_history_rebuild()
    p.save()
    pars={p.model3d.GetParameterName(i):p.model3d.GetParameterSValue(i) for i in range(p.model3d.GetNumberOfParameters())}
    (folder/'parameters.json').write_text(json.dumps(pars,indent=2))
    return p

def add_monitors(p,frequencies):
    existing=p.model3d.get_tree_items()
    for f in frequencies:
        if f'Field Monitors\\farfield (f={f})' not in existing:
            p.model3d.add_to_history(f'Matched-band farfield {f} GHz',f'''With Monitor
.Reset
.Name "farfield (f={f})"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "{f}"
.Create
End With''')
    p.save()

def export_pattern(p,f,folder):
    m=p.model3d;folder=Path(folder);folder.mkdir(exist_ok=True)
    assert m.SelectTreeItem(f'Farfields\\farfield (f={f:g}) [1]')
    ff=m.FarfieldPlot;ff.Reset();ff.Plottype('3d');ff.SetPlotMode('directivity');ff.SelectComponent('Abs');ff.SetScaleLinear(False)
    ff.SetPlotRangeOnly(False);ff.Step(2);ff.Step2(2);ff.Plot()
    ff.ASCIIExportSummary(str(folder/f'Farfield_{f:g}_Summary.txt'))
    a=m.ASCIIExport;a.Reset();a.FileName(str(folder/f'Farfield_{f:g}_Sphere.txt'));a.Execute()
    m.Plot.DrawWorkplane('False');m.Plot.ZoomToStructure()
    m.Plot.ExportImage(str(folder/f'Farfield_{f:g}_CST.png'),1400,1000)
    print('PATTERN_EXPORTED',f,flush=True)
