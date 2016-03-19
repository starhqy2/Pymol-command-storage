#version 11
from pymol.cmd import *
def mdivision(axi="",frames=""):
    return str(round(float(axi)/float(frames), 3))
def msave(prefix="",current_frame="1",mode=1,width="0", height="0",dpi="-1.0",bg_col="white",ray_opaque_background="off",antialias="2",ray="0"):
    if mode==1:
        bg_color(bg_col)
        set("ray_opaque_background",ray_opaque_background)
        png(prefix + str(current_frame).zfill(4),ray=ray)
    elif mode == 2:
        bg_color(bg_col)
        set("antialias", antialias)
        set("ray_opaque_background",ray_opaque_background)
        png(prefix + str(current_frame).zfill(4),width, height, dpi, 1)


def mrotate(axi="y", degrees="360", frames="30"):
    per_frame_degree=mdivision(degrees, frames)
    rotate(axi, per_frame_degree)
    
def mselection(target_object="cyan",of_object="anti1",max_distance="", frames="",current_frame="",mode="within"):
    per_frame_dist=float(mdivision(max_distance, frames))
    current_frame_dist=per_frame_dist * current_frame ### once occur error: attention: string * int = string string string ... 
    if mode=="within":
        return "%s within %s of %s" % (target_object, current_frame_dist, of_object)
    elif mode == "beyond":
        current_frame_dist_rev=max_distance-current_frame_dist
        return "%s beyand %s of %s" % (target_object, current_frame_dist_rev, of_object)
        
def mcolor(color_color="cyan",target_object="cyan",of_object="anti1",max_distance="", frames="",current_frame="",mode="within"):    
    color(color_color,mselection(target_object,of_object,max_distance,frames,current_frame,mode))

def mtransparency(transp_style="surface",begin_transp="", end_transp="", selection="",frames="",current_frame=""):
    per_frame_transp=round((float(end_transp)-float(begin_transp))/float(frames),3)
    if per_frame_transp<0:
        current_frame_transp = 1 + per_frame_transp*float(current_frame)
    else:
        current_frame_transp = per_frame_transp*float(current_frame)
    if transp_style=="surface":
         
        set("transparency", current_frame_transp,selection)
    elif transp_style=="cartoon":

        set("cartoon_transparency", current_frame_transp, selection)

def mtranslate(x="", y="", z="", trans_obj="", frames=""):
    x_per_frame= mdivision(x,frames)
    y_per_frame= mdivision(y,frames)
    z_per_frame= mdivision(z,frames)
    translate("[%s,%s,%s]" % (x_per_frame,y_per_frame, z_per_frame), trans_obj)
def mdisappear(target_obj="anti2", of_obj="yellow",max_distance="68",frames="30",current_frame=""):
    selection=mselection(target_obj, of_obj, max_distance, frames, current_frame,mode=2)
    set("cartoon_transparency",1,selection)

    
    
    

