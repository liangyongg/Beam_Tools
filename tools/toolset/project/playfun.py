#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Config(object):

    ASSET_STEP_TASK_INFO = {"Disign":["Design"],
                            "Model":["HighModel","FacialBs","LowModel"],
                            "Mp":["MattePainting"],
                            "FX":["hair","Cloth"],
                            "Texture":["HighTexture","LowTexture"],
                            "Rig":["LayoutRig","MotionRig","AniRig","RedRig","HairRig","ClothRig"]}

    SHOT_STEP_TASK_INFO = {"model":["LowModel"],
                           "FX":["ClothCache","HairCache","Effect"],
                           "Lighting":["Light"],
                           "Render":["Render"],
                           "Comp":["Composite"],
                           "Mp":["MattePainting"],
                           "Animation":["Animation"]}

    TASK_NAME_SAMPLE_LIB = {"HighModel":"model",
                            "HighTexture":"surface",
                            "AniRig":"rigging",
                            "ClothRig":"clrig",
                            "HairRig":"hairrig",
                            "RedRig":"redrig",
                            "hair":"hair",
                            "Animation":"animation",
                            "ClothCache":"cloth",
                            "HairCache":"hair",
                            "Effect":"efx",
                            "Light":"lighting"
                            }

    STEP_NAME_LIB = {"modeling":"Model",
                     "cfx":"FX",
                     "lgt":"Lighting",
                     "comp":"Comp",
                     "mp":"Mp",
                     "ani":"Animation",
                     "efx":"FX",
                     "srf":"Texture",
                     "rigging":"Rig",
                     "set":"set"
                     }

    TYPE_LIST = ["asset","shot"]
    TYPE_LIB = {"asset":["mode","cfx","srf","rig"],
                "shot":["ani","cfx","lgt","comp","mp","efx"]}