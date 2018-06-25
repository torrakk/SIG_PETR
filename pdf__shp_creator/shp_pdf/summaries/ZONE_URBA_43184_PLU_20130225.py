path='C:/SIG/SIG/001_URBANISME/TRAVAIL_IMAGIS/001_VALIDES/SAINT-FERREOL-D-AUROURE/43184_PLU_20130225/Donnees_geographiques/ZONE_URBA.dbf'
zones={'A':[34, 35, 36, 37, 38],
       'Nh':[39, 40, 41, 42],
       'AUc':[24, 25, 26, 27],
       'AUsa':[31, 32, 33],
       'AUca':[24, 25, 26, 27],
       'UCp':[14, 15, 16, 17],
       'AUi':[28, 29, 30],
       'Nhi':[39, 40, 41, 42],
       'AUs':[31, 32, 33],
       'N':[39, 40, 41],
       'AUit':[28, 29, 30],
       'UCe':[14, 15, 16, 17],
       'AU':[21, 22, 23],
       'UCa':[14, 15, 16, 17],
       'UI':[18, 19, 20],
       'UA':[6, 7, 8, 9],
       'UC':[14, 15, 16, 17],
       'UB':[10, 11, 12, 13],
       }
reglementPath='C:/SIG/SIG/001_URBANISME/TRAVAIL_IMAGIS/001_VALIDES/SAINT-FERREOL-D-AUROURE/43184_PLU_20130225/Pieces_ecrites/3_reglement'
date='20130225'
insee='43184'

if __name__ == '__main__':
    for zone, pages in zones.items():
        print "'"+zone+'\':'+str([i-1 for i in pages])+","