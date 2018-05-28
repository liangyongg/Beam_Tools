import maya.cmds as cmds

#edo_connectBlendShapeToBlendShape('body_collide_sk__BLENDSHAPE',['cloth_2__BLENDSHAPE'])
def edo_connectBlendShapeToBlendShape(bsa,others):
    #bsa='body_collide_sk__BLENDSHAPE'
    #others=['body_body_sk__BLENDSHAPE']
    mesha=''
    if '__' in bsa:
        mesha=bsa.split('__')[0]+'_'
    for other in others:
        #other=others[0]
        mesho=''
        if '__' in other:
            mesho=other.split('__')[0]+'_'
        wc=cmds.blendShape(bsa,q=1,wc=1)
        for i in range(0,wc):
            #i=73
            atname=cmds.aliasAttr(bsa+'.weight['+str(i)+']',q=1)
            if not atname=='':
                if cmds.objExists(other+'.'+atname):
                    try:
                        cmds.connectAttr(bsa+'.'+atname,other+'.'+atname,f=1)
                    except:
                        print 'pass connection'
                else:
                    natname=atname.replace(mesha,mesho)
                    if cmds.objExists(other+'.'+natname):
                        try:
                            cmds.connectAttr(bsa+'.'+atname,other+'.'+natname,f=1)
                        except:
                            print 'pass connection'