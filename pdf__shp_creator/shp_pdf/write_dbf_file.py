# coding: utf-8
# -*- coding: utf-8 -*-
import os
from shp_pdf.shape_summary import shapeReadSummary
from string import Formatter
from shp_pdf.utils import reglementPath
from dbfpy import dbf
import re

class WriteDbf(shapeReadSummary):

    def __init__(self, shapefile, field, to_field, pattern):
        '''
        Classe permettant d'ecrire dans le dbf pour mettre a jour les zones du reglement
        :param args: shapefile fields
        '''
        super(WriteDbf, self).__init__(shapefile, field)
        self.to_field = to_field
        self.pattern = pattern
        self.dict_format = {"code_insee": self.getMetadatas(self.shapefile).group('code_insee'),
                           "date":self.getMetadatas(self.shapefile).group('date')}

    def getSettingsFile(self):
        return ""

    @property
    def __writer(self):
        '''

        :return: shapefile reader object
        '''
        if not os.path.exists(self.shapefile):
            raise Exception('Le fichier n\'existe pas')
        self.dbf = dbf.Dbf(self.shapefile)
        return self.dbf

    def completeDict(self, record):
        '''
        Cette methode permet de completer le dictionnaire servant d'argument a la methode de formatage des caractères
        présente dans la fonction wrtiePatern.
        :param record:
        :return:
        '''
        self.complete_dict = self.dict_format.copy()
        list_string = [fn for _, fn, _, _ in Formatter().parse(self.pattern) if fn is not None]
        for champ_manquant in [i for i in list_string if i not in self.dict_format.keys()]:
            try:
                self.complete_dict.update({champ_manquant: record.__getitem__(champ_manquant)})
                return self.complete_dict
            except KeyError:
                raise KeyError('Vous tentez d\'acceder a un champ non-existant')

    def writePatern(self):

        for record in self.__writer:
            try:
                complete_dict = self.completeDict(record)
                record[self.to_field] = self.pattern.format(**complete_dict)
                print record
                record.store()
            except ValueError:
                raise ValueError('Ce champ ne semble pas exister')
        return True
            #print map(record, )
            #print [i for i in Formatter().parse(self.pattern)]
            #record[self.to_field]=self.patern.format(**self.dict_format)



if __name__=="__main__":
    path_list = [
        "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\AUREC_SUR_LOIRE\\43012_PLU_20171207\\Donnees_geographiques\\ZONE_URBA.dbf",
        "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-JUST-MALMONT\\43205_PLU_20170309\\Donnees_geographiques\\ZONE_URBA.dbf",
        "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-DIDIER-EN-VELAY\\43177_PLU_20140630\\Donnees_geographiques\\ZONE_URBA.dbf",
        "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-FERREOL-D-AUROURE\\43184_PLU_20130225\\Donnees_geographiques\\ZONE_URBA.dbf",
        "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-VICTOR-MALESCOURS\\43227_PLU_20120301\\Donnees_geographiques\\ZONE_URBA.dbf",
        "C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\PONT-SALOMON\\43153_PLU_20140306\\Donnees_geographiques\\ZONE_URBA.dbf"
        ]
    for path in path_list:
        a = WriteDbf(
             path,
            'LIBELLE', 'NOMFIC', '{code_insee}_reglement_{LIBELLE}_{date}.pdf')
        a.writePatern()
