'''

History:

2015/09/03 hongqiyang Second release

'''

from pymol import cmd, CmdException

def rmsd(selection = "all", chains = "", doAlign = 1, doPretty = 1, \
         algorithm = 1, guide = 1, method = "super", quiet = 1, colorstyle = "blue_red", colormode = ""):
    """
DESCRIPTION

    Align all structures and show the structural.

ARGUMENTS

    Haves following arguments:
    selection = "all"
    chains = ""  : like {chains = ab"}
    doAlign = 0 or 1 : Superpose selections before calculating distances {default: 1}
    doPretty = 1 
    guide = 1
    algorithm = 0 or 1 :  
    method = "super"
    quiet = 1

EXAMPLE

    fetch

    """
    from chempy import cpv
#initial parameters
    doAlign, doPretty = int(doAlign), int(doPretty)
    guide, quiet = int(guide), int(quiet)
    algorithm = int(algorithm)
    
#get suitable align method
    try:
        align = cmd.keyword[method][0]
    except:
        print "Error: no such method:", method
        raise CmdException

#get object and store each atom's coordinate
    objects = set()
    idx2coords = dict()
    cmd.iterate_state(-1, selection, "objects.add(model) ", space=locals())
#store the compared rmsd tree for each objects, like {obj:{obj1:{(model, index):(model1, index1)}}}

    rmsd_stored = dict()
    for obj in objects:
        rmsd_stored[obj] = {}
        for obj1 in objects:
            if obj != obj1:
                if guide:
                    guide = " and guide"
                else:
                    guide = ""
                rmsd_stored[obj][obj1] = {}
                total_values = {}
                if chains:
                    for eachchain in list(chains):
                        if doAlign:
                            align(obj1 + guide + " and chain " + eachchain, obj + guide + " and chain " + eachchain)
                        align(obj1 + " and chain " + eachchain, obj + " and chain " + eachchain, cycles = 0, transform = 0, object="aln")
                        cmd.iterate_state(-1, selection, "idx2coords[model,index] = (x,y,z)", space=locals())
                        if cmd.count_atoms('?' + "aln", 1, 1) == 0:
                            # this should ensure that "aln" will be available as selectable object
                            cmd.refresh()
                        for col in cmd.get_raw_alignment("aln"):
                            assert len(col) == 2
                            b = cpv.distance(idx2coords[col[0]], idx2coords[col[1]])
                            for idx in col:
                                total_values[idx] = b
                            if col[0][0] == obj:
                                rmsd_stored[obj][obj1][col[0]] = [col[1],b]
                            else:
                                rmsd_stored[obj][obj1][col[1]] = [col[0],b]
                        cmd.delete("aln")
                else:
                    if doAlign:
                        align(obj1 + guide, obj + guide)
                    align(obj1 + guide, obj + guide, cycles=0, transform=0, object="aln")
                    cmd.iterate_state(-1, selection, "idx2coords[model,index] = (x,y,z)", space=locals())
                    if cmd.count_atoms('?' + "aln", 1, 1) == 0:
                        # this should ensure that "aln" will be available as selectable object
                        cmd.refresh()
                    for col in cmd.get_raw_alignment("aln"):
                        assert len(col) == 2
                        b = cpv.distance(idx2coords[col[0]], idx2coords[col[1]])
                        for idx in col:
                                total_values[idx] = b
                        if col[0][0] == obj:
                            rmsd_stored[obj][obj1][col[0]] = [col[1],b]
                        else:
                            rmsd_stored[obj][obj1][col[1]] = [col[0],b]
                    cmd.delete("aln")
    if algorithm:
        def b_replace(model, index):
            n = 0
            bsum = 0

            for obj1 in objects:
                if model != obj1:
                    if (model, index) in rmsd_stored[model][obj1]:
                        nextmodel, nextindex = rmsd_stored[model][obj1][model, index][0]
                        bsum += rmsd_stored[model][obj1][model, index][1]
                        n += 1
                        for nextobj1 in objects:
                            if nextmodel != nextobj1 and nextmodel != obj1 :
                                if (nextmodel, nextindex) in rmsd_stored[nextmodel][nextobj1]:
                                    bsum += rmsd_stored[nextmodel][nextobj1][nextmodel, nextindex][1]
                                    n += 1
            if n == 0 :
                return -1
            else:
                return eval("bsum / n")
                        
        
        
    else:
        
        def b_replace(model, index):
            n = 0
            bsum = 0
           
            for obj1 in objects:
                if model != obj1:
                    if (model, index) in rmsd_stored[model][obj1]:
                        bsum += rmsd_stored[model][obj1][model, index][1]
                        n += 1
               
            if n == 0 :
                return -1
            else:
                return eval("bsum / n")
        
                
    cmd.alter(selection, 'b = b_replace(model, index)', space=locals())
    
           
    if doPretty:
        
        mini = min(total_values.values())
        maxi = max(total_values.values())
        if colormode:
            if colormode == "lowshow":
                maxi = sum(total_values.values()) / len(total_values)
                print("This is lowshow")
            elif colormode == "highshow":
                mini = sum(total_values.values()) / len(total_values)
                print("This is highshow")
            else:
                raise CmdException
                
        cmd.orient(selection)
        cmd.show_as('cartoon', 'byobj ' + selection)
        cmd.color('gray', selection)
        cmd.spectrum('b', "blue_red", selection + ' and b > -0.5',minimum = mini, maximum = maxi)
    if not quiet:
        print " ColorByRMSD: Minimum Distance: %.2f" % (min(total_values.values()))
        print " ColorByRMSD: Maximum Distance: %.2f" % (max(total_values.values()))
        print " ColorByRMSD: Average Distance: %.2f" % (sum(total_values.values()) / len(total_values))
   
   
cmd.extend('rmsd', rmsd)    


