"""Rerun a fresh copy of the delivered CST project; preserve the accepted file."""
import sys,os,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CST=Path(os.environ.get('CST_INSTALLPATH_2024',r'D:\TELE9782\CST Studio Suite 2024'))
_dll=os.add_dll_directory(str(CST/'AMD64'))
sys.path.insert(0,str(CST/'AMD64'/'python_cst_libraries'))
import cst.interface as ci
import engineering
from engineering import run,export_pattern

def main():
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    source=ROOT/'01_CST_Project'/'TELE9782_DBand_Patch_Final.cst'
    p=de.open_project(str(source))
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out=ROOT/'06_Working'/('Reproduction_'+stamp);out.mkdir()
    p.save(str(out/'Reproduction.cst'),include_results=False)
    summary,data=run(p)
    export_pattern(p,150,out)
    p.save();p.close()
    p=de.open_project(str(out/'Reproduction.cst'))
    import cst.results as cr
    r=cr.ProjectFile(p.filename(),allow_interactive=True).get_3d()
    item=r.get_result_item(r'1D Results\S-Parameters\S1,1')
    result=dict(reopened=True,project=p.filename(),S11_sample_count=len(item.get_xdata()),solver=p.model3d.get_solver_run_info())
    (out/'Reopen_Check.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    print('Saved reproduction copy:',out)

if __name__=='__main__':main()
