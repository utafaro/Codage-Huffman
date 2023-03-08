class NoeudBinaire:
    """
    Classe qui va représenter à la fois nos feuilles mais aussi l'arbre de Huffman
    """
    def __init__(self, etiquette, freq, fGauche=None, fDroite=None):
        self.etiquette = etiquette
        self.fGauche = fGauche
        self.fDroite = fDroite
        self.freq = freq

    def getfDroite(self):
        return self.fDroite

    def getfGauche(self):
        return self.fGauche

    def setfDroite(self, fDroite):
        self.fDroite = fDroite

    def setfGauche(self, fGauche):
        self.fGauche = fGauche

    def getFreq(self):
        return self.freq

    def __str__(self):
        return f"char : {self.etiquette} | frequence : {self.freq}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, node):
        return self.freq < node.freq






