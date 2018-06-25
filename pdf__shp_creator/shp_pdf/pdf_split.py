# coding: utf-8
# -*- coding: utf-8 -*-


import os
import importlib
from PyPDF2 import PdfFileWriter, PdfFileReader
import re

class splitPdf():

    def __init__(self, pdf_source, summary_path):
        self.pdf = pdf_source
        self.summary_path = summary_path
        self.sum_path = importlib.import_module('summaries.{}'.format(summary_path))
        self.zones = self.sum_path.zones
        self.reglementPath = self.sum_path.reglementPath

        if not (os.path.exists(self.pdf)):
            raise Exception('Le chemin ne semblent pas exister')

    def split(self):
        with open(self.pdf, 'rb') as pdf_source:
            input_pdf = PdfFileReader(pdf_source)
            for zone, pages in self.zones.items():
               #print(zone, pages)
                nom_new_pdf = self.getNomNewPdf(zone)
                self.pdf_writer = PdfFileWriter()
                #[pdf_writer.addPage(page) for page in [input_pdf.getPage(page) for page in pages]]
                for page in [input_pdf.getPage(page) for page in pages]:
                    self.pdf_writer.addPage(page)
                #map(self.pdf_writer.addPage, [input_pdf.getPage(page) for page in pages])
                print("Nombre de page(s) selectionnees : ", self.pdf_writer.getNumPages())
                print("Creation du PDF: ", nom_new_pdf)
                with open(nom_new_pdf, 'wb') as self.newpdf:
                    self.pdf_writer.write(self.newpdf)

    def getNomNewPdf(self, zone):
        self.regex_metadatas = re.compile(r'.*(?P<basename>(?P<code_insee>\d{5})_.*_(?P<date>\d{8})).*')
        self.metadatas = self.regex_metadatas.match(self.pdf)
        return os.path.join(self.reglementPath, self.metadatas.group('code_insee')+"_reglement_"+zone+"_"+self.metadatas.group('date')+".pdf")






if __name__=='__main__':
    path_list = {
        "ZONE_URBA_43012_PLU_20171207":"C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\AUREC_SUR_LOIRE\\43012_PLU_20171207\\Pieces_ecrites\\3_Reglement\\43012_reglement_20171207.pdf",
        "ZONE_URBA_43205_PLU_20170309":"C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-JUST-MALMONT\\43205_PLU_20170309\\Pieces_ecrites\\3_Reglement\\43205_reglement_20170309.pdf",
        "ZONE_URBA_43177_PLU_20140630":"C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-DIDIER-EN-VELAY\\43177_PLU_20140630\\Pieces_ecrites\\3_Reglement\\43177_reglement_20140630.pdf",
        "ZONE_URBA_43184_PLU_20130225":"C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-FERREOL-D-AUROURE\\43184_PLU_20130225\\Pieces_ecrites\\3_Reglement\\43184_reglement_20130225.pdf",
        "ZONE_URBA_43227_PLU_20120301":"C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\SAINT-VICTOR-MALESCOURS\\43227_PLU_20120301\\Pieces_ecrites\\3_Reglement\\43227_REGLEMENT_20120301.pdf",
        "ZONE_URBA_43153_PLU_20140306":"C:\\SIG\\SIG\\001_URBANISME\\TRAVAIL_IMAGIS\\001_VALIDES\\PONT-SALOMON\\43153_PLU_20140306\\Pieces_ecrites\\3_Reglement\\43153_reglement_20140306.pdf",
    }
    for conf_file, path in path_list.items():
        a = splitPdf(path,
             conf_file)
        a.split()