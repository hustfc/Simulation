Relays= {
"UE1": {"IP":"10.0.0.1","link_e":0.10,"Gains":"100","F_BS":195.43396778377053,"F_UE":78.651537149636575,"N1":28,"b":"5.808983469629878"},
"UE2": {"IP":"10.0.0.2","link_e":0.15,"Gains":"100","F_BS":225.13105279816864,"F_UE":100.58333991774799,"N1":26,"b":"6.868589996836461"},
"UE3": {"IP":"10.0.0.3","link_e":0.20,"Gains":"100","F_BS":247.54588421179346,"F_UE":114.93967520628291,"N1":24,"b":"7.789153133595121"},
"UE4": {"IP":"10.0.0.4","link_e":0.25,"Gains":"100","F_BS":263.82627716639126,"F_UE":125.27621813097173,"N1":22,"b":"8.694373551407805"},
"UE5": {"IP":"10.0.0.5","link_e":0.30,"Gains":"100","F_BS":281.2885847713523,"F_UE":133.2092290621777,"N1":21,"b":"9.343296622008463"},
"UE6": {"IP":"10.0.0.6","link_e":0.35,"Gains":"100","F_BS":295.65261736458785,"F_UE":139.53538286618212,"N1":20,"b":"9.976769143309106"},
"UE7": {"IP":"10.0.0.7","link_e":0.40,"Gains":"100","F_BS":307.3441330874717,"F_UE":144.74137184593536,"N1":19,"b":"10.617966939259755"},
"UE8": {"IP":"10.0.0.8","link_e":0.45,"Gains":"100","F_BS":316.6832853264184,"F_UE":149.12205673189075,"N1":18,"b":"11.284558707327264"},
"UE9": {"IP":"10.0.0.9","link_e":0.50,"Gains":"100","F_BS":323.907429967555,"F_UE":152.86335767704668,"N1":17,"b":"11.991962216296864"}
}
for key,value in Relays.iteritems():
    print(key,value)