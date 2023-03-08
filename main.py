
from arbre import NoeudBinaire

import os


def frequency_file(file):
    """Fonction qui va créer le fichier de fréquence"""
    frequency = tri_global(file)

    with open(f'Fichier huffman/{file}_frequ.txt', 'w') as f:
        for i in frequency: #pour chaque tuple dans la liste
            f.write(f"{i[0]} : {i[1]} \n") #i[0] : lettre, i[1] : fréquennce


def char_occurences(file):
    """
    Retourne un dico avec comme clé la lettre et comme valeur sa fréquence dans le contenu du fichier
    :return: un dico avec les caractères et de l'occurence
    """
    dico_occurences = {}
    with open(f"Fichier huffman/{file}.txt", 'r') as f:
        content = f.read() #on lit caractère par caractère
        number_occurence = 1 #on met cette valeur à 1 car si il y a une lettre dans le texte, elle y sera forcément 1 fois
        for i in content:
            if i in dico_occurences:
                dico_occurences[i] = dico_occurences[i] + 1 #on rajoute 1 si la lettre est déjà apparu auparavant
            else:
                dico_occurences[i] = number_occurence #sinon on met la valeur à 1
        f.close()
    return dico_occurences


def tri_dico_occurence(list_entre):
    """

    :param list_tri_ascii: liste de tuples
    :return: liste de tuples trié selon leur occurences
    """
    #la fonction sorted() créer une liste
    list_trie = sorted(list_entre, key=lambda x: x[1]) #cela permet de trie notre liste par rapport au 2ème éléments des tuples qui sont nos fréquences
    return list_trie


def tri_dico_ascii(dico):
    """
    Fonction qui prend en paramètre un dictionnaire de fréquence et qui va triée selon la table ascii des lettres
    :param dico: dict()
    :return: list of tuple
    """
    res = sorted(dico.items(), key=lambda x: ord(x[0]))
    return res


def tri_global(file):
    """
    Fonction qui prend en paramètre un fichier et qui retourne une liste de tuples correspond
    à la lettre et sa fréquence
    :param file: fichier txt
    :return: list of tuple
    """
    liste = tri_dico_ascii(char_occurences(file))
    liste = tri_dico_occurence(liste)

    return liste


def create_leafs(liste):
    """

    :param liste: list of tuple (liste de tuple triée par ordre d'occurences croissant puis ascii croissant
    :return: Liste de Noeud représentant les feuilles
    """
    return [NoeudBinaire(char[0], char[1]) for char in liste]




def createTree(file):
    """

    :param file: on place toujours le fichier qu'on veut compresser
    :return: NoeudBinaire qui représente la racine de notre arbre
    """
    liste = create_leafs(tri_global(file)) #on récupère notre liste de feuilles

    while len(liste) > 1: #tant qu'il y a plus qu'un arbre dans notre liste
        liste.sort(key=lambda x: x.freq) #à chaque tour de boucle, on retrie notre liste par rapport à la fréquence
        f1 = liste.pop(0) #on supprime puis on récupère le premier élément de la liste
        f2 = liste.pop(0) #on supprime puis on récupère le premier élément de la liste
        new_tree = NoeudBinaire(None, f1.getFreq() + f2.getFreq(), f1, f2) #on crée un nouvel arbre comme demandé dans l'énoncé
        liste.append(new_tree) #on ajoute cette arbre dans la liste

    return liste[0] #on récupère le seul élément de la liste qui est la racine de l'arbre


def generates_code(node: NoeudBinaire, code="", dic_code={}):
    """

    :param node: racine de l'arbre crée
    :param code: valeur en bits
    :param dic_code: dict()
    :return: un dictionnaire correspondant associant chaque lettre à leur valeur en bits
    """
    if node.etiquette: #sous entendu != None
        print(f'{node.etiquette} : {code}')
        dic_code[node.etiquette] = code #on ajoute le code associé à la lettre
    else:
        generates_code(node.getfGauche(), code + "0")
        generates_code(node.getfDroite(), code + "1")

    return dic_code


def encode(file, dic_code):
    """

    :param file: fichier à compresser
    :param dic_code: le dictionnaire créer par generate_code()
    :return: str -> représentant le texte encodée
    """
    code = ""
    with open(f'Fichier huffman/{file}.txt', 'r') as f:
        content = f.read()
        for char in content:
            code += dic_code[char] #pour chaque caractère du texte, on concatène leur code associé dans la variable code
        f.close()

    #on enregistre ce code dans un fichier binaire
    encoded_bytes = bytes(int(code[i:i + 8], 2) for i in range(0, len(code), 8))
    with open(f'Fichier huffman/{file}_comp.bin', 'wb') as b:
        b.write(encoded_bytes)

    return code

def compression_rate(fichier_txt, fichier_bin):
    """

    :param fichier_txt: fichier txt
    :param fichier_bin: fichier binaire
    :return: str
    """
    initial_volume = os.path.getsize(f'Fichier huffman/{fichier_txt}')  # on récupère la taille du fichier txt
    final_volume = os.path.getsize(f'Fichier huffman/{fichier_bin}')  # on récupère la taille du fichier binaire
    return f'Taux de compression : {1-(final_volume/initial_volume)}' # on utilise la formule de l'énoncé

def char_bits_average(dic_code):
    """
    Nombre de bits moyen par caractère
    :param dic_code: notre dictionnaire de code générée à partir de generate_code()
    :return: str
    """
    sum_code = 0
    for code in dic_code.values():
        sum_code += len(code)
    return f'Nombre moyen de bits par caractère : {sum_code/ len(dic_code)}'


def main(file):
    """

    :param file: Fichier à compresser
    :return: void
    """
    frequency_file(file)
    root = createTree(file)
    dic_code = generates_code(root)
    encode(file, dic_code)
    print(compression_rate(f"{file}.txt", f"{file}_comp.bin"))
    print(char_bits_average(dic_code))


if __name__ == '__main__':
    main("alice")