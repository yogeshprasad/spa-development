inputData = {'CSYS-2':1130671,
                'CSYS-3':1121163,
                'CSYS-4':1121267,
                'CSYS-5':1115606,
                'CSYS-6':1119227,
                'CSYS-7':1122150,
                'CSYS-8':1122757,
                'CSYS-9':1117382,
                'CSYS-10':1122825,
                'CSYS-11':1123527,
                'CSYS-12':1123306,
                'CSYS-13':1123594,
                'CSYS-14':1124220,
                'CSYS-15':1124066,
                'CSYS-16':1124187,
                'CSYS-17':1124685,
                'CSYS-18':1124714,
                'CSYS-19':1124553,
                'CSYS-20':1120220,
                'CSYS-21':1125271,
                'CSYS-22':1125248,
                'CSYS-23':1125686,
                'CSYS-24':1125748,
                'CSYS-25':1131449,
                'CSYS-26':1125109}

for key, value in inputData.iteritems():
    dtm = session.scratchOdbs['Z:/Stress Analysis/Task01_Ultrafan_PGB/Work In Progress/WIP_06/ADDITIONAL-RUNS/IT1/IT_1_NOLF.odb'].rootAssembly.datumCsyses[key]
    session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
        datumCsys=dtm)
    odb = session.odbs['Z:/Stress Analysis/Task01_Ultrafan_PGB/Work In Progress/WIP_06/ADDITIONAL-RUNS/IT1/IT_1_NOLF.odb']
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
        'LE', INTEGRATION_POINT, ((COMPONENT, 'LE11'), (COMPONENT, 'LE22'), (
        COMPONENT, 'LE33'), )), ), nodeLabels=(('PART-1-1', (str(value), )), ))
    xyp = session.xyPlots['XYPlot-1']
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    curveList = session.curveSet(xyData=xyList)
    chart.setValues(curvesToPlot=curveList)
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    odb = session.odbs['Z:/Stress Analysis/Task01_Ultrafan_PGB/Work In Progress/WIP_06/ADDITIONAL-RUNS/IT1/IT_1_NOLF.odb']
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    import sys
    sys.path.insert(10, r'C:\SIMULIA\Abaqus\6.11-1\abaqus_plugins\excelUtilities')
    import abq_ExcelUtilities.excelUtilities
    abq_ExcelUtilities.excelUtilities.XYtoExcel(
        xyDataNames='_LE:LE11 ('+key+') (Avg: 100%) PI: PART-1-1 N: ' +str(value)+ ',_LE:LE22 ('+key+') (Avg: 100%) PI: PART-1-1 N: ' +str(value)+ ',_LE:LE33 ('+key+') (Avg: 100%) PI: PART-1-1 N: ' + str(value), 
        trueName='')