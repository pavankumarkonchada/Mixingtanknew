import os
# Open File, this needs to stay like this and will be replaced with the required path in spaceclaim_script2.py
DocumentOpen.Execute(filename)
# EndBlock

# Extrude 1 Face (outlet)
selection = FaceSelection.Create(GetRootPart().Bodies[13].Faces[4])
reference = Selection.Create(GetRootPart().Bodies[13].Edges[4].GetChildren[ICurvePoint]()[0])
options = ExtrudeFaceOptions()
options.KeepMirror = True
options.KeepLayoutSurfaces = False
options.KeepCompositeFaceRelationships = True
options.PullSymmetric = False
options.OffsetMode = OffsetMode.IgnoreRelationships
options.Copy = False
options.ForceDoAsExtrude = False
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ExtrudeFaces.SetDimension(selection, reference, MM(outlet_length), options)
# EndBlock

# Extrude 1 Face (inlet 2)
selection = FaceSelection.Create(GetRootPart().Bodies[13].Faces[12])
reference = Selection.Create(GetRootPart().Bodies[13].Edges[12].GetChildren[ICurvePoint]()[0])
options = ExtrudeFaceOptions()
options.KeepMirror = True
options.KeepLayoutSurfaces = False
options.KeepCompositeFaceRelationships = True
options.PullSymmetric = False
options.OffsetMode = OffsetMode.IgnoreRelationships
options.Copy = False
options.ForceDoAsExtrude = False
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ExtrudeFaces.SetDimension(selection, reference, MM(inlet2_length), options)
# EndBlock

# Extrude 1 Face (inlet 1)
selection = FaceSelection.Create(GetRootPart().Bodies[13].Faces[8])
reference = Selection.Create(GetRootPart().Bodies[13].Edges[8].GetChildren[ICurvePoint]()[0])
options = ExtrudeFaceOptions()
options.KeepMirror = True
options.KeepLayoutSurfaces = False
options.KeepCompositeFaceRelationships = True
options.PullSymmetric = False
options.OffsetMode = OffsetMode.IgnoreRelationships
options.Copy = False
options.ForceDoAsExtrude = False
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ExtrudeFaces.SetDimension(selection, reference, MM(inlet1_length), options)
# EndBlock

# Offset 4 Faces (impeller radius)
selection = FaceSelection.Create([GetRootPart().Bodies[12].Faces[24],
	GetRootPart().Bodies[12].Faces[22],
	GetRootPart().Bodies[12].Faces[23],
	GetRootPart().Bodies[12].Faces[25]])
reference = FaceSelection.Create(GetRootPart().Bodies[12].Faces[26])
options = OffsetFaceOptions()
options.OffsetMode = OffsetMode.MoveFacesTogether
options.Copy = False
options.ExtrudeType = ExtrudeType.ForceIndependent
result = OffsetFaces.SetDimension(selection, MM(Impeller_radius), -Direction.DirX, reference, options)
# EndBlock

# Create Named Selection Group (outlet)
primarySelection =FaceSelection.Create(GetRootPart().Bodies[13].Faces[5])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group1", "outlet")
# EndBlock

# Create Named Selection Group (inlet 1)
primarySelection = FaceSelection.Create(GetRootPart().Bodies[13].Faces[9])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group1", "inlet1")
# EndBlock

# Create Named Selection Group (inlet 2)
primarySelection =  FaceSelection.Create(GetRootPart().Bodies[13].Faces[13])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group1", "inlet2")
# EndBlock

#saving the geometry file, this needs to stay like this and will be replaced with actual location in spaceclaim_script2.py
DocumentSave.Execute(dest)
# EndBlock
