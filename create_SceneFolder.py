### ---D-facto standard construct scene --- ###

# A tool must provide the ability to add or clean remove a new layer
# - add layout geo context, add light context with light group, add geo group, add image layered
# - add ALL to lightgroup, light group to layer , connect geo group to layer,

# TODO: Add holdout combiner, SEt framerange and save path string, set framerange

# --- Scene check if save
respond, filename = ix.check_need_save()
if respond.is_yes():
    ix.application.save_project(filename)

if not respond.is_cancelled():
    # create an empty project
    ix.application.new_project()
    # clear and reset all Clarisse windows
    # ix.application.reset_windows_layout()

# --- Time control (setup in and out as well as fps)
# dynamic once a ftrack integration would come along !

# ix.cmds.SetFps(25)
ix.cmds.SetCurrentFrameRange(1001.0, 1101.0)  # python command ? API ? dynamic variable with FTRACK
ix.application.get_factory().get_time().set_current_frame(float(1001))  # set currentframe to 1001 (API)
ix.application.get_factory().get_time().set_fps(float(25))  # set fps to PAL(25) (API)

##-- create the context list --##
start_ctx = ix.application.get_current_context()  # capture the current active context to bring back

# --Create the list with all context names --#
contextList = ["support", "CAMS", "LAYOUT", "LIGHTS", "SCENE","templates","utilityMat"]
sceneList = ["RENDER", "RULES", "PATH_TRACER"]
LayoutList = ["ACTIVE","shading","pCams","assembly","scatters","IMPORT"]
llist = ["sets", "volume","bg"]

for i in contextList:
    ix.create_context(i)

# contextList = [["support",""], ["CAMS","blue"], ["LAYOUT","green"], ["LIGHTS","yellow"], ["SCENE","red"],["templates",""],["utilityMat",""]]
### t= len(contextList) ## optional
# for i in contextList:
#     print (i)


# --- lights context

ix.application.cd("/LIGHTS")
current_ctx = ix.application.get_current_context()
ix.cmds.ColorTagItems (current_ctx, "green")
ix.create_context(current_ctx.get_name() + "/default")

# --- RENDER context

ix.application.cd("/LAYOUT")
current_ctx = ix.application.get_current_context()

for l in LayoutList:
    ix.create_context(current_ctx.get_name() + "/" + l)
# add rendering setup folder

ix.application.cd("/LAYOUT")
current_ctx = ix.application.get_current_context()

ix.create_context(current_ctx.get_name() + "/scene")
ix.create_context(current_ctx.get_name() + "/scene/ACTIVE")
ix.create_context(current_ctx.get_name() + "/scene/shading")
ix.create_context(current_ctx.get_name() + "/scene/pCams")
ix.create_context(current_ctx.get_name() + "/scene/assembly")
ix.create_context(current_ctx.get_name() + "/scene/scatterers")
ix.create_context(current_ctx.get_name() + "/scene/import")

#create basic light
ix.application.cd("/LIGHTS/default")
lgt = ix.create_object('lgt_sun_generic', 'LightPhysicalDistant')
lgt.attrs.display_color = 14
lgt.attrs.light_path_expression_label[0] = "lgt_sun"
lgtgrp = ix.create_object("LGT_ALL", "Group")
ix.cmds.SetValues([str(lgtgrp) + ".inclusion_rule[0]"], ["./*"])

for l in llist:
    ix.application.cd("/render/lighting/"+ l )
    lgtgrp = ix.create_object("lgt_" + l, "Group")
    ix.cmds.SetValues([str(lgtgrp) + ".inclusion_rule[0]"], ["./*"])
    ix.cmds.AddValues(["project://render/lighting/"+ l +"/lgt_"+l+".inclusion_items"], ["project://render/lighting/ALL/LGT_ALL"])


# create a basic camera
ix.application.cd("/render")
camera = ix.create_object('camera', 'CameraPerspectiveAdvanced')  # standart for rendering

#create basic renderer
renderer = ix.create_object('renderer_GLOBAL', 'RendererRaytracer')
renderer.attrs.anti_aliasing_sample_count = 8  # set a value for the render

# Add a render Image
img = ix.create_object('beauty', 'Image')  # new render image object
img.attrs.resolution[0] = 1920
img.attrs.resolution[1] = 1080
img.attrs.resolution_multiplier = 2

# create the layer
for t in llist:
    lay = img.get_module().add_layer('Layer3d', t).get_object()  # adding new layer to the image
    lay.attrs.active_camera = camera
    lay.attrs.renderer = renderer

#create a group for each layer
ix.application.cd("/groups")
for g in llist:
    geogrp = ix.create_object(g + "_grp", "Group")
    ix.cmds.SetValues([str(geogrp) + ".inclusion_rule[0]"], ["project://render/layout/"+ g + "/*"])
    ix.cmds.SetValues(["project://render/beauty."+ g +".geometries"], ["project://render/groups/" + g + "_grp"]) # set the geometry group
    ix.cmds.SetValues(["project://render/beauty."+ g +".lights"], ["project://render/lighting/" + g +"/lgt_" + g])



# --- revert to selection
ix.application.cd(start_ctx.get_full_name())
