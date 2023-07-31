from ansys.fluent.core import launch_fluent
import ansys.fluent.core as pyfluent


path=import_filename
#starting fluent in meshing mode
Runcase = "steady" # if it is steady Runcase = "steady" and transient Runcase = "transient"
meshing = pyfluent.launch_fluent(precision="double", processor_count=process_count, mode="meshing",show_gui =True)

#water tight workflow
meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

#importing geometry
meshing.workflow.TaskObject["Import Geometry"].Arguments = {"FileName": path,"LengthUnit": "mm",}

#adding local size
meshing.workflow.TaskObject['Add Local Sizing'].Arguments.setState({r'AddChild': r'yes',r'BOIExecution': r'Body Size',r'BOIFaceLabelList': [r'geom1-srf1'],r'BOISize': 0.6,})
meshing.workflow.TaskObject['Add Local Sizing'].AddChildToTask()
meshing.workflow.TaskObject['Add Local Sizing'].InsertCompoundChildTask()
meshing.workflow.TaskObject['bodysize_1'].Arguments.setState({r'AddChild': r'yes',r'BOIControlName': r'bodysize_1',r'BOIExecution': r'Body Size',r'BOIFaceLabelList': [r'geom1-srf1'],r'BOISize': 0.6,})
meshing.workflow.TaskObject['Add Local Sizing'].Arguments.setState({r'AddChild': r'yes',})
meshing.workflow.TaskObject['bodysize_1'].Execute()

#generating surface mesh
meshing.workflow.TaskObject["Generate the Surface Mesh"].Arguments = {"CFDSurfaceMeshControls": {"MaxSize": max_size,"MinSize":0.6,r'GrowthRate': growth_rate_bl,}}
meshing.workflow.TaskObject["Generate the Surface Mesh"].Execute()

#describing geometry
meshing.workflow.TaskObject['Describe Geometry'].Arguments.setState({r'InvokeShareTopology': r'Yes',r'NonConformal': r'No',r'SetupType': r'The geometry consists of only fluid regions with no voids',r'WallToInternal': r'Yes',})
meshing.workflow.TaskObject['Describe Geometry'].Execute()

#Update boundary (assuming named selections)
meshing.workflow.TaskObject["Update Boundaries"].AddChildToTask()
meshing.workflow.TaskObject["Update Boundaries"].Execute()

#Update Regions
meshing.workflow.TaskObject["Update Regions"].AddChildToTask()
meshing.workflow.TaskObject["Update Regions"].Execute()

#Boundary Layers
meshing.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
meshing.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
meshing.workflow.TaskObject["smooth-transition_1"].Arguments = {r"BLControlName": "smooth-transition_1",r'BLRegionList': [r'srf1', r'solid'],r'BLZoneList': [r'srf1:1', r'solid:1'],r'NumberOfLayers': total_no_of_layers,}
meshing.workflow.TaskObject["Add Boundary Layers"].Arguments = {}
meshing.workflow.TaskObject["smooth-transition_1"].Execute()

#Generate Volume Mesh
meshing.workflow.TaskObject["Generate the Volume Mesh"].Arguments = {"VolumeFill": "polyhedra",}
meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()

#switch to solver
solver = meshing.switch_to_solver()

#mesh check
solver.tui.mesh.check()

#Modify length units to mm, angular velocity to rev/min
solver.tui.define.units("length", "m")
solver.tui.define.units("angular-velocity", "rev/min")

#Enable gravity
solver.tui.define.operating_conditions.gravity("yes",0,0,-9.81)

#Viscous model
solver.tui.define.models.viscous.ke_standard("yes")
solver.tui.define.models.viscous.near_wall_treatment.enhanced_wall_treatment("yes")

#copying water material from fluent database
solver.tui.define.materials.copy("fluid", "water-liquid")

#defining cell zone conditions
#tank
solver.tui.define.boundary_conditions.fluid(
    "solid",
    "yes",
    "water-liquid",
    "no",
    "no",
    "no",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "1",
    "no",
    "no",
    "no",
    "no",
    "no",
)

#MRF zone
solver.tui.define.boundary_conditions.fluid(
    "srf1",
    "yes",
    "water-liquid",
    "no",
    "no",
    "yes",
    "-1",
    "no",
    "400",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "no",
    "0",
    "none",
    "no",
    "no",
    "no",
    "no",
    "no",
)

#boundary conditions
#mass flow inlet1
solver.tui.define.boundary_conditions.zone_type("inlet1","mass-flow-inlet")
solver.tui.define.boundary_conditions.mass_flow_inlet("inlet1","yes","yes","no",in_vel,"no",0,"no","yes","no","no","yes",5,10)

#mass flow inlet2
solver.tui.define.boundary_conditions.zone_type("inlet2","mass-flow-inlet")
solver.tui.define.boundary_conditions.mass_flow_inlet("inlet1","yes","yes","no",0.5,"no",0,"no","yes","no","no","yes",5,10)

#pressure outlet
solver.tui.define.boundary_conditions.pressure_outlet("outlet","yes","no",0,"no","yes","no","no","yes",5,10,"yes","no","no","no")

#hybrid initialization
solver.tui.solve.initialize.hyb_initialization()

#monitor points-mass avg velocity at outlet
solver.tui.solve.monitors.residual.plot("yes")
solver.tui.solve.report_definitions.add(
    "outlet-velocity",
    "surface-massavg",
    "field",
    "velocity-magnitude",
    "surface-names",
    "outlet",
    "()",
    "quit",
)

#writing case file
solver.tui.file.write_case("mixing_tank.cas.h5")

#defining number of iterations
solver.tui.solve.iterate(300)

#writing dat file
solver.tui.file.write_data("mixing_tank.dat.h5")
solver.tui.display.set.picture.use_window_resolution("no")
solver.tui.display.set.picture.x_resolution(1920)
solver.tui.display.set.picture.y_resolution(1080)

#creating contours of pressure at the wall
solver.tui.display.objects.create("contour","pressure","surfaces-list","solid:1",[],"field","pressure")
solver.tui.display.objects.edit("pressure","color-map","font-size",0.1)
solver.tui.display.objects.edit("pressure","color-map","format","%3.2f")
solver.tui.display.objects.edit("pressure","range-option","auto-range-on","global-range","no")

#displaying and saving the pressure contour created
solver.tui.display.objects.display("pressure")
solver.tui.views.restore_view("isometric")
solver.tui.views.auto_scale()
solver.tui.display.objects.edit("pressure","color-map","width",6)
solver.tui.display.objects.display("pressure")
solver.tui.views.camera.zoom_camera(0.9)
solver.tui.display.save_picture("pressure")

#create a vertical plane in YZ
solver.tui.surface.plane_surface("YZ-plane","yz-plane",0)

#creating Qcriteria contour using the YZ plane
solver.tui.display.objects.create("contour","Q-criteria","surfaces-list","YZ-plane",[],"field","q-criterion")
solver.tui.display.objects.edit("q-criteria","color-map","font-size",0.1)
solver.tui.display.objects.edit("q-criteria","color-map","format","%3.2f")
solver.tui.display.objects.edit("q-criteria","range-option","auto-range-on","global-range","no")

#displaying and saving the Q-criteria contour created
solver.tui.display.objects.display("q-criteria")
solver.tui.views.restore_view("right")
solver.tui.views.auto_scale()
solver.tui.display.objects.edit("q-criteria","color-map","width",7)
solver.tui.display.objects.display("q-criteria")
solver.tui.views.camera.zoom_camera(0.7)
solver.tui.display.save_picture("q-criteria")

#calculating area weighted average pressure at inlet1
pavg=eval(solver.scheme_eval.exec(('/report/surface-integrals/area-weighted-avg inlet1 () pressure no',)).split(' ')[-1])

#calculating area weighted average wall shear at the tank wall
wallshear=eval(solver.scheme_eval.exec(('/report/surface-integrals/area-weighted-avg solid:1 () wall-shear no',)).split(' ')[-1])

#creating line to create plot
solver.tui.surface.line_surface("line-1",0.33,0,0.11,-0.33,0,0.11)

#creating velocity plot using the created line
solver.tui.display.objects.create("xy-plot","vel_plot","surfaces-list","line-1",[])
solver.tui.display.objects.edit("vel_plot","y-axis-function","velocity-magnitude")
solver.tui.display.objects.edit("vel_plot","axes","numbers","float",3,"float",3,"q")

#displaying and saving the velocity plot created
solver.tui.views.camera.zoom_camera(0.5)
solver.tui.display.objects.display("vel_plot")
solver.tui.display.save_picture("vel_plot")


#creating text file with the results from fluent, it contains area average pressure on walls and wall shear on walls
outstring=str(pavg)+","+str(wallshear)
print(outstring)
file2= open(r"C:\check\result.txt","wt")
file2.write(str(outstring))
file2.close()