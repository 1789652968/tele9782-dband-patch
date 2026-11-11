"""Rebuild the final geometry from bundled definitions, then actually run CST."""
import os,sys,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CST=Path(os.environ.get('CST_INSTALLPATH_2024',r'D:\TELE9782\CST Studio Suite 2024'))
_dll=os.add_dll_directory(str(CST/'AMD64'))
sys.path.insert(0,str(CST/'AMD64'/'python_cst_libraries'))
import cst.interface as ci
from engineering import build,run,export_pattern

def main():
    pars=json.loads((ROOT/'02_Simulation_Results'/'parameters.json').read_text())
    pars={k:float(v) for k,v in pars.items()}
    summary=json.loads((ROOT/'02_Simulation_Results'/'summary.json').read_text())
    monitors=[float(x['f_GHz']) for x in summary['farfields']]
    name='Rebuild_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    p=build(de,name,changes=pars,monitors=monitors)
    run(p);export_pattern(p,150,Path(p.filename()).parent);p.save()
    print('Rebuilt and simulated:',p.filename())

if __name__=='__main__':main()
