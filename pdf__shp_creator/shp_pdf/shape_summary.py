# coding: utf-8
# -*- coding: utf-8 -*-

import shapefile as shpr
import os
import re
from shp_pdf.settings import *
from shp_pdf.utils import reglementPath

class shapeReadSummary(object):
    '''
    Cette classe permet de generer un fichier python avec un dictionnaire permettant d'avoir des valeurs uniques
    pour la colonne demandee
    '''
    def __init__(self, shapefile, field):
        '''

        :param shapefile: chemin vers le shapefile
        :param field: champs a intéroger
        '''
        self.shapefile = shapefile
        self.field = field
        self.metadatas = re.compile(r'.*(?P<basename>(?P<code_insee>\d{5})_PLU_(?P<date>\d{8})).*')

    @property
    def __reader(self):
        '''

        :return: shapefile reader object
        '''
        if not os.path.exists(self.shapefile):
            raise Exception('Le fichier n\'existe pas')
        self.shpfile  = open(self.shapefile, 'rb')
        return shpr.Reader(dbf=self.shpfile)

    def searchField(self):
        '''
        Permet de lire le fichier shapefile et retourne les valeurs uniques du champ
        :return: liste de valeurs uniques (list)
        '''
        obj = self.__reader
        try:
            return {champ[0]: index for index, champ in enumerate(obj.fields)}[self.field]-1
        except(KeyError):
            raise Exception("Le champ n'est pas présent, vous devez préciser une valeur dans le plage suivante \n{}".format(obj.fields))

    def getUniqueValuesFromfield(self):

        '''
        Permet d'obtenir une liste de valeurs uniques à partir d'une champ
        :return: list of unique values
        '''
        uniques_values = sorted(set([value[self.searchField()] for value in self.__reader.records()]))
        return uniques_values

    def getMetadatas(self, url):
        return self.metadatas.match(url)

    def writeSummaryFile(self):
        if not os.path.exists(SUMMARY_FOLDER):
            raise Exception('Le repertoire contenant l\'inventaire des fichiers est absent')
        basename = self.getMetadatas(self.shapefile).group('basename')
        with open(os.path.join(SUMMARY_FOLDER, os.path.splitext(os.path.basename(self.shapefile))[0]+"_"+basename+".py"), 'w') as fichier:
            fichier.write('path=\''+self.shapefile.replace('\\', '/')+'\'\n')
            fichier.write('zones='+str({ zone : "" for zone in self.getUniqueValuesFromfield()})+'\n')
            fichier.write('reglementPath=\''+reglementPath(self.shapefile.replace('\\', '/'))+'\'\n')
            fichier.write('date=\'' + self.getMetadatas(self.shapefile).group('date') + '\'\n')
            fichier.write('insee=\'' + self.getMetadatas(self.shapefile).group('code_insee') + '\'\n')

    @property
    def getFieldsList(self):
        return self.__reader.fields

    def __exit__(self):
        self.shpfile.close()

if __name__ == '__main__':
    path_list = ["C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\AUREC_SUR_LOIRE\\43012_PLU_20171207\\Donnees_geographiques\\ZONE_URBA.dbf",
                 "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-JUST-MALMONT\\43205_PLU_20170309\\Donnees_geographiques\\ZONE_URBA.dbf",
                 "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-DIDIER-EN-VELAY\\43177_PLU_20140630\\Donnees_geographiques\\ZONE_URBA.dbf",
                 "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-FERREOL-D-AUROURE\\43184_PLU_20130225\\Donnees_geographiques\\ZONE_URBA.dbf",
                 "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-VICTOR-MALESCOURS\\43227_PLU_20120301\\Donnees_geographiques\\ZONE_URBA.dbf",
                 "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\PONT-SALOMON\\43153_PLU_20140306\\Donnees_geographiques\\ZONE_URBA.dbf"
                 ]
    for path in path_list:
        sh = shapeReadSummary(
        path,
        'LIBELLE')
        print(sh.getUniqueValuesFromfield())
        sh.writeSummaryFile()

