'# MWS Version: Version 2024.0 - Sep 01 2023 - ACIS 33.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 130 fmax = 170
'# created = '[VERSION]2024.0|33.0.1|20230901[/VERSION]


'@ D-band radiating template

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
'set the units
With Units
    .SetUnit "Length", "mm"
    .SetUnit "Frequency", "GHz"
    .SetUnit "Voltage", "V"
    .SetUnit "Resistance", "Ohm"
    .SetUnit "Inductance", "nH"
    .SetUnit "Temperature",  "K"
    .SetUnit "Time", "ns"
    .SetUnit "Current", "A"
    .SetUnit "Conductance", "S"
    .SetUnit "Capacitance", "pF"
End With

'----------------------------------------------------------------------------

'set the frequency range
Solver.FrequencyRange "130", "170"

'----------------------------------------------------------------------------

Plot.DrawBox True

With Background
     .Type "Normal"
     .Epsilon "1.0"
     .Mu "1.0"
     .XminSpace "0.0"
     .XmaxSpace "0.0"
     .YminSpace "0.0"
     .YmaxSpace "0.0"
     .ZminSpace "0.0"
     .ZmaxSpace "0.0"
End With

With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
End With

' switch on FD-TET setting for accurate farfields

FDSolver.ExtrudeOpenBC "True"

Mesh.FPBAAvoidNonRegUnite "True"
Mesh.ConsiderSpaceForLowerMeshLimit "False"
Mesh.MinimumStepNumber "5"

With MeshSettings
     .SetMeshType "Hex"
     .Set "RatioLimitGeometry", "20"
End With

With MeshSettings
     .SetMeshType "HexTLM"
     .Set "RatioLimitGeometry", "20"
End With

PostProcess1D.ActivateOperation "vswr", "true"
PostProcess1D.ActivateOperation "yz-matrices", "true"

With FarfieldPlot
	.ClearCuts ' lateral=phi, polar=theta
	.AddCut "lateral", "0", "1"
	.AddCut "lateral", "90", "1"
	.AddCut "polar", "90", "1"
End With

'----------------------------------------------------------------------------

Dim sDefineAt As String
sDefineAt = "130;140;150;160;170"
Dim sDefineAtName As String
sDefineAtName = "130;140;150;160;170"
Dim sDefineAtToken As String
sDefineAtToken = "f="
Dim aFreq() As String
aFreq = Split(sDefineAt, ";")
Dim aNames() As String
aNames = Split(sDefineAtName, ";")

Dim nIndex As Integer
For nIndex = LBound(aFreq) To UBound(aFreq)

Dim zz_val As String
zz_val = aFreq (nIndex)
Dim zz_name As String
zz_name = sDefineAtToken & aNames (nIndex)

' Define E-Field Monitors
With Monitor
    .Reset
    .Name "e-field ("& zz_name &")"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Efield"
    .MonitorValue  zz_val
    .Create
End With

' Define H-Field Monitors
With Monitor
    .Reset
    .Name "h-field ("& zz_name &")"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Hfield"
    .MonitorValue  zz_val
    .Create
End With

' Define Farfield Monitors
With Monitor
    .Reset
    .Name "farfield ("& zz_name &")"
    .Domain "Frequency"
    .FieldType "Farfield"
    .MonitorValue  zz_val
    .ExportFarfieldSource "False"
    .Create
End With

Next

'----------------------------------------------------------------------------

With MeshSettings
     .SetMeshType "Hex"
     .Set "Version", 1%
End With

With Mesh
     .MeshType "PBA"
End With

'set the solver type
ChangeSolverType("HF Time Domain")

'----------------------------------------------------------------------------

'@ define material: Gold

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Material
     .Reset
     .Name "Gold"
     .Folder ""
     .FrqType "static"
     .Type "Normal"
     .SetMaterialUnit "Hz", "mm"
     .Epsilon "1"
     .Mu "1.0"
     .Kappa "4.561e+007"
     .TanD "0.0"
     .TanDFreq "0.0"
     .TanDGiven "False"
     .TanDModel "ConstTanD"
     .KappaM "0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstTanD"
     .DispModelEps "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "General 1st"
     .DispersiveFittingSchemeMu "General 1st"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .FrqType "all"
     .Type "Lossy metal"
     .MaterialUnit "Frequency", "GHz"
     .MaterialUnit "Geometry", "mm"
     .MaterialUnit "Time", "s"
     .MaterialUnit "Temperature", "Kelvin"
     .Mu "1.0"
     .Sigma "4.561e+007"
     .Rho "19320.0"
     .ThermalType "Normal"
     .ThermalConductivity "314.0"
     .SpecificHeat "130", "J/K/kg"
     .MetabolicRate "0"
     .BloodFlow "0"
     .VoxelConvection "0"
     .MechanicsType "Isotropic"
     .YoungsModulus "78"
     .PoissonsRatio "0.42"
     .ThermalExpansionRate "14"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "1", "1", "0"
     .Wireframe "False"
     .Reflection "False"
     .Allowoutline "True"
     .Transparentoutline "False"
     .Transparency "0"
     .Create
End With

'@ define material: Polyimide (lossy)

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Material
     .Reset
     .Name "Polyimide (lossy)"
     .Folder ""
     .FrqType "all"
     .Type "Normal"
     .SetMaterialUnit "GHz", "mm"
     .Epsilon "eps_r"
     .Mu "1.0"
     .Kappa "0.0"
     .TanD "loss_tangent"
     .TanDFreq "150"
     .TanDGiven "True"
     .TanDModel "ConstTanD"
     .KappaM "0.0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstKappa"
     .DispModelEps "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "General 1st"
     .DispersiveFittingSchemeMu "General 1st"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .Rho "1400.0"
     .ThermalType "Normal"
     .ThermalConductivity "0.20"
     .SpecificHeat "1000", "J/K/kg"
     .SetActiveMaterial "all"
     .MechanicsType "Isotropic"
     .YoungsModulus "2.5"
     .PoissonsRatio "0.4"
     .ThermalExpansionRate "25"
     .Colour "0.94", "0.82", "0.76"
     .Wireframe "False"
     .Transparency "0"
     .Create
End With

'@ Finite lossy inset patch with uniform port launch

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Component.New "antenna"
With Brick
.Reset
.Name "ground"
.Component "antenna"
.Material "Gold"
.Xrange "-ground_width/2", "ground_width/2"
.Yrange "-ground_length/2", "ground_length/2"
.Zrange "-metal_thickness", "0"
.Create
End With
With Brick
.Reset
.Name "substrate"
.Component "antenna"
.Material "Polyimide (lossy)"
.Xrange "-ground_width/2", "ground_width/2"
.Yrange "-ground_length/2", "ground_length/2"
.Zrange "0", "substrate_h"
.Create
End With
With Brick
.Reset
.Name "launch_ground"
.Component "antenna"
.Material "Gold"
.Xrange "-port_halfwidth", "port_halfwidth"
.Yrange "-ground_length/2-launch_length", "-ground_length/2"
.Zrange "-metal_thickness", "0"
.Create
End With
With Brick
.Reset
.Name "launch_substrate"
.Component "antenna"
.Material "Polyimide (lossy)"
.Xrange "-port_halfwidth", "port_halfwidth"
.Yrange "-ground_length/2-launch_length", "-ground_length/2"
.Zrange "0", "substrate_h"
.Create
End With
Solid.Add "antenna:ground", "antenna:launch_ground"
Solid.Add "antenna:substrate", "antenna:launch_substrate"
With Brick
.Reset
.Name "patch"
.Component "antenna"
.Material "Gold"
.Xrange "-patch_width/2", "patch_width/2"
.Yrange "-patch_length/2", "patch_length/2"
.Zrange "substrate_h", "substrate_h+metal_thickness"
.Create
End With
With Brick
.Reset
.Name "left"
.Component "antenna"
.Material "Vacuum"
.Xrange "-feed_width/2-inset_gap", "-feed_width/2"
.Yrange "-patch_length/2", "-patch_length/2+inset_length"
.Zrange "substrate_h", "substrate_h+metal_thickness"
.Create
End With
Solid.Subtract "antenna:patch", "antenna:left"
With Brick
.Reset
.Name "right"
.Component "antenna"
.Material "Vacuum"
.Xrange "feed_width/2", "feed_width/2+inset_gap"
.Yrange "-patch_length/2", "-patch_length/2+inset_length"
.Zrange "substrate_h", "substrate_h+metal_thickness"
.Create
End With
Solid.Subtract "antenna:patch", "antenna:right"
With Brick
.Reset
.Name "feed"
.Component "antenna"
.Material "Gold"
.Xrange "-feed_width/2", "feed_width/2"
.Yrange "-ground_length/2-launch_length", "-patch_length/2+inset_length"
.Zrange "substrate_h", "substrate_h+metal_thickness"
.Create
End With
Solid.Add "antenna:patch", "antenna:feed"

'@ Port, radiation boundary and solver accuracy

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Boundary
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
.SteadyStateLimit "-50"
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

'@ set PBA version

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Discretizer.PBAVersion "2023090124"

'@ Matched-band farfield 146 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=146)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "146"
.Create
End With

'@ Matched-band farfield 147 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=147)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "147"
.Create
End With

'@ Matched-band farfield 148 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=148)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "148"
.Create
End With

'@ Matched-band farfield 149 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=149)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "149"
.Create
End With

'@ Matched-band farfield 151 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=151)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "151"
.Create
End With

'@ Matched-band farfield 152 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=152)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "152"
.Create
End With

'@ Matched-band farfield 153 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=153)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "153"
.Create
End With

'@ Matched-band farfield 154 GHz

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
With Monitor
.Reset
.Name "farfield (f=154)"
.Domain "Frequency"
.FieldType "Farfield"
.MonitorValue "154"
.Create
End With

'@ Evaluate farfields on global enclosing surface

'[VERSION]2024.0|33.0.1|20230901[/VERSION]
Solver.MonitorFarFieldsNearToModel "False"
Solver.SteadyStateLimit "-60"

