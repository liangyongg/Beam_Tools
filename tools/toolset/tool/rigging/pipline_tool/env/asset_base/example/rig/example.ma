//Maya ASCII 2016 scene
//Name: example.ma
//Last modified: Thu, Jan 11, 2018 07:55:04 PM
//Codeset: 936
file -rdi 1 -ns "example" -rfn "exampleRN" -op "v=0;p=17;f=0" -typ "mayaAscii"
		 "E:/git_work/Beam_Tools/tools/toolset/tool/rigging/pipline_tool/asset_base/example/mod/example.ma";
file -rdi 1 -ns "example1" -rfn "exampleRN1" -op "v=0;p=17;f=0" -typ "mayaAscii"
		 "E:/git_work/Beam_Tools/tools/toolset/tool/rigging/pipline_tool/asset_base/example/set/example.ma";
file -r -ns "example" -dr 1 -rfn "exampleRN" -op "v=0;p=17;f=0" -typ "mayaAscii"
		 "E:/git_work/Beam_Tools/tools/toolset/tool/rigging/pipline_tool/asset_base/example/mod/example.ma";
file -r -ns "example1" -dr 1 -rfn "exampleRN1" -op "v=0;p=17;f=0" -typ "mayaAscii"
		 "E:/git_work/Beam_Tools/tools/toolset/tool/rigging/pipline_tool/asset_base/example/set/example.ma";
requires maya "2016";
requires -nodeType "ilrOptionsNode" -nodeType "ilrUIOptionsNode" -nodeType "ilrBakeLayerManager"
		 -nodeType "ilrBakeLayer" "Turtle" "2016.0.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2016";
fileInfo "version" "2016";
fileInfo "cutIdentifier" "201502261600-953408";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "20A693F5-46AD-E0C7-3FBB-DEA253C4716E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-014 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "45C2DD2B-497C-EBF8-6FEF-858C04DDAECA";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "072B99CD-4EC9-3FB0-F0CC-349D0DAD8BCE";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "C93981AE-4CD0-9FE0-B970-D2BBBCBD43A1";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "47E5C14F-4B94-6E01-28CD-D3845D8EB051";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "2C902894-41E2-302B-ABBF-3EB44E6887F4";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "CF870916-41DA-AEB3-7E76-A080F63AC062";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "C0BE5566-441E-F6D5-A537-6CA9AB16C27C";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "216AB174-4610-B904-4409-B0A893CC3A7D";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "9CC6212D-4DE7-82AD-7A57-31B11BA9B61E";
createNode displayLayer -n "defaultLayer";
	rename -uid "2C45DE2A-4AEC-9296-387C-488B6CC13A58";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "26BC55E6-4969-38A9-7621-BDA03FC8D2CB";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "39762A4E-4A13-A04D-A052-FA8634CD5911";
	setAttr ".g" yes;
createNode ilrOptionsNode -s -n "TurtleRenderOptions";
	rename -uid "06DD144F-405C-F63E-7B46-1FB371AADB9C";
lockNode -l 1 ;
createNode ilrUIOptionsNode -s -n "TurtleUIOptions";
	rename -uid "3DE8A231-482B-B19C-532F-9D9018F44514";
lockNode -l 1 ;
createNode ilrBakeLayerManager -s -n "TurtleBakeLayerManager";
	rename -uid "FD04CB1D-4DE5-F973-3D43-C096BA63DE76";
lockNode -l 1 ;
createNode ilrBakeLayer -s -n "TurtleDefaultBakeLayer";
	rename -uid "126B3C0F-4356-1FA6-1A40-50A31A69A2E6";
lockNode -l 1 ;
createNode reference -n "exampleRN";
	rename -uid "C2A1197C-407A-8C17-B628-C9BFB7BD1A13";
	setAttr ".ed" -type "dataReferenceEdits" 
		"exampleRN"
		"exampleRN" 0;
	setAttr ".ptag" -type "string" "";
lockNode -l 1 ;
createNode reference -n "exampleRN1";
	rename -uid "C27CF782-46F1-AA6B-E14D-AD888CF0B81A";
	setAttr ".ed" -type "dataReferenceEdits" 
		"exampleRN1"
		"exampleRN1" 0;
	setAttr ".ptag" -type "string" "";
lockNode -l 1 ;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "CC979409-43BD-F57A-165F-0A8AAF924D61";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 0;
	setAttr -av ".unw";
	setAttr -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -k on ".an";
	setAttr -k on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":TurtleDefaultBakeLayer.idx" ":TurtleBakeLayerManager.bli[0]";
connectAttr ":TurtleRenderOptions.msg" ":TurtleDefaultBakeLayer.rset";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of example.ma