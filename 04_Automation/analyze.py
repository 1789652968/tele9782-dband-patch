"""Post-process numerical exports from actual CST simulations (never synthesizes data)."""
from pathlib import Path
import csv,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
def load_curve(folder,key):
    a=np.genfromtxt(folder/(key.replace('\\','_')+'.csv'),delimiter=',',skip_header=1)
    return a[:,0],a[:,1]+1j*a[:,2]

def band_edges(f,db,level=-10):
    edges=[];begin=None
    for i in range(len(f)):
        if db[i]<=level and begin is None:
            begin=float(f[i]) if i==0 else float(np.interp(level,[db[i],db[i-1]],[f[i],f[i-1]]))
            left_censored=(i==0)
        if begin is not None and (db[i]>level or i==len(f)-1):
            end=float(f[i]) if db[i]<=level else float(np.interp(level,[db[i-1],db[i]],[f[i-1],f[i]]))
            edges.append(dict(f_low_GHz=begin,f_high_GHz=end,BW_GHz=end-begin,FBW_percent=100*(end-begin)/((end+begin)/2),left_censored=bool(left_censored),right_censored=bool(db[i]<=level)))
            begin=None
    return edges

def audit(folder):
    s=json.loads((folder/'summary.json').read_text())
    f,g=load_curve(folder,r'1D Results\S-Parameters\S1,1');db=20*np.log10(abs(g));i=np.argmin(abs(g))
    x,z=load_curve(folder,r'1D Results\Z Matrix\Z1,1')
    zx=[]
    for j in range(len(x)-1):
        if z[j].imag*z[j+1].imag<0:
            v=x[j]-z[j].imag*(x[j+1]-x[j])/(z[j+1].imag-z[j].imag)
            zx.append(dict(f_GHz=float(v),R_ohm=float(np.interp(v,x,z.real))))
    a=dict(s11_min_freq_GHz=float(f[i]),s11_min_dB=float(db[i]),matched_bands=band_edges(f,db),max_abs_S11=float(max(abs(g))),port_reactance_zero_crossings=zx,farfield_checks=[])
    for ff in s['farfields']:
        fq=ff['f_GHz'];mag=float(np.interp(fq,f,abs(g)));eta=10**(ff['rad_eff_dB']/10)
        calc=ff['Dmax_dBi']+10*math.log10(eta)+10*math.log10(1-mag**2)
        row=dict(f_GHz=fq,eta_rad=eta,eta_total=10**(ff['total_eff_dB']/10),gain_identity_residual_dB=ff['realized_gain_dBi']-calc)
        def power(name):
            xx,yy=load_curve(folder,'1D Results\\Power\\Excitation [1]\\'+name)
            return float(np.interp(fq,xx,yy.real))
        try:
            row.update(Pstim_W=power('Power Stimulated'),Paccepted_W=power('Power Accepted'),Prad_W=power('Power Radiated'),Pmetal_W=power('Loss in Metals'),Pdielectric_W=power('Loss in Dielectrics'),Poutgoing_W=power('Power Outgoing all Ports'))
            row['power_balance_residual_W']=row['Paccepted_W']-row['Prad_W']-row['Pmetal_W']-row['Pdielectric_W']
            row['power_balance_residual_percent_accepted']=100*row['power_balance_residual_W']/row['Paccepted_W']
            row['eta_power']=row['Prad_W']/row['Paccepted_W']
            row['farfield_power_residual_W']=ff['Prad_W']-row['Prad_W']
        except FileNotFoundError:pass
        a['farfield_checks'].append(row)
    (folder/'numerical_audit.json').write_text(json.dumps(a,indent=2))
    return a

def main():
    rows=[]
    for file in (ROOT/'06_Working').glob('*/summary.json'):
        folder=file.parent;s=json.loads(file.read_text());a=audit(folder)
        row={'Iteration':s['name'],'S11_min_freq_GHz':s['f_min_s11_GHz'],'S11_min_dB':s['min_s11_dB'],'Solver':s['solver']['state'],
             'Assessment':'Diagnostic: near-model farfield surface not accepted' if s['name'].startswith(('Tuned_','Inset_','Single_')) else 'See numerical audit and final validation'}
        p=json.loads((folder/'parameters.json').read_text());row.update(p)
        f150=next(v for v in s['farfields'] if v['f_GHz']==150)
        row.update(D150_dBi=f150['Dmax_dBi'],S11_150_dB=f150['s11_dB'],Gain150_dBi=f150['realized_gain_dBi'])
        rows.append(row)
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with open(ROOT/'05_Documentation'/'Iteration_Log.csv','w',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=keys);w.writeheader();w.writerows(rows)
    print(json.dumps([{k:r[k] for k in ['Iteration','S11_min_freq_GHz','S11_min_dB','D150_dBi']} for r in rows],indent=2))

if __name__=='__main__':main()
