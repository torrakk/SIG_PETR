import os

def reglementPath(path):
    '''
    :param path: chemin de destination
    :return: path destination des reglements decoupes
    '''
    pieces_ecrites = 'Pieces_ecrites/3_reglement'
    return os.path.dirname(path.replace('Donnees_geographiques', pieces_ecrites))