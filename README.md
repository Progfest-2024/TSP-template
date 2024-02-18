# DefiProgFest2024-Admin

## Introduction
Dans l'objectif de mettre en pratique les connaissances acquises lors du ProgFest 2024, nous vous proposons 
d'effectuer un projet pouvant être réalisé en équipe. Nous recommandons des équipes de 2 à 4 personnes. Le projet 
consiste à résoudre un problème, tout en collaborant avec vos coéquipiers et en utilisant de 
bonnes pratiques de programmation. Le défi sera de créer un algorithme afin de résoudre le problème du vendeur vagabond. 

Le problème du vendeur vagabond (TSP, acronyme de Traveling Salesman Problem en anglais) est un problème 
mathématique et algorithmique dans le domaine de l'optimisation combinatoire. L'objectif du TSP est de trouver le 
trajet le plus court possible qui permet à un voyageur de visiter un ensemble de villes d'un coup et de 
revenir à sa ville de départ.

En d'autres termes, le TSP consiste à déterminer la séquence optimale des villes à visiter de manière à minimiser la 
distance totale parcourue par le voyageur. Ce problème est souvent illustré en imaginant un vendeur qui doit parcourir 
différentes villes pour vendre ses produits, tout en minimisant les coûts de déplacement.

Le TSP est un problème NP-difficile, ce qui signifie qu'il peut devenir rapidement très complexe à résoudre lorsque le 
nombre de villes à visiter augmente. Il a de nombreuses applications pratiques, notamment dans la logistique, la 
planification des itinéraires, l'optimisation des réseaux de livraison et d'autres domaines où la minimisation des 
distances est cruciale. De nombreuses méthodes et algorithmes ont été développés pour résoudre le TSP, mais il demeure 
un problème d'importance en recherche.

La version recommandée de python est 3.10 et peut être téléchargée [ici](https://www.python.org/downloads/). 

## But du défi

Pour résoudre ce type de problème en utilisant la programmation et python, nous allons vous fournir une matrice 
d'adjacence qui représente les distances entre les villes. Une matrice d'adjacence est une matrice carrée de taille
`N` par `N` où `N` est le nombre de villes. La valeur à la position `(i, j)` de la matrice représente la distance entre 
la ville `i` et la ville `j`. Si la valeur est égale à `numpy.NaN` ou `numpy.inf`, cela signifie que 
la ville `i` et la ville `j` ne sont pas
connectées. Voici un exemple de matrice d'adjacence pour 4 villes:

| (i, j) | 0 | 1 | 2 | 3 |
|--------|---|---|---|---|
| **0**  | 0 | 1 | 2 | 3 |
| **1**  | 1 | 0 | 4 | 5 |
| **2**  | 2 | 4 | 0 | 6 |
| **3**  | 3 | 5 | 6 | 0 |

Dans cet exemple, la ville 0 est à une distance de 1 de la ville 1, 2 de la ville 2 et 3 de la ville 3. De plus, vous 
pouvez remarquer que la matrice est symétrique par rapport à la diagonale. Cela signifie que la distance entre la ville
`i` et la ville `j` est la même que la distance entre la ville `j` et la ville `i`. Finalement, vous pouvez remarquer
que le chemin le plus court pour visiter toutes les villes une seule fois et revenir à la ville de départ est de
visiter les villes dans l'ordre 0, 3, 2, 1, 0. Ce cycle hamiltonien a une distance totale de 14.


Vous devrez donc trouver le chemin le plus court pour
visiter toutes les villes une seule fois et revenir à la ville de départ. Pour ce faire, vous devrez utiliser un
algorithme de recherche. Vous pouvez utiliser l'algorithme de recherche de votre choix, mais nous vous suggérons
d'utiliser l'un des algorithmes suivants qui, selon nous, sont les plus simples à implémenter:

- [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)


## À faire

1. Vous devez faire un fork du dépôt GitHub du défi utilisant GitHub Classroom. Vous pouvez accéder au dépôt en cliquant
    [ici](https://classroom.github.com/a/7PXPqCu1).
2. **Implémenter votre propre algorithme dans la classe `TSP` du fichier [tsp.py](src/tsp.py) et implémenter sa méthode 
`get_solution() -> Union[Tuple, List[int], np.ndarray]`. Votre algorithme peut comporter autant de méthodes et d'attributs 
que vous souhaitez, mais la méthode `get_solution()` doit s'y trouver.** De plus, la signature du constructeur de la classe `TSP` ne devrait pas être modifiée. Toutefois, le contenu du
constructeur peut être modifié à votre guise.
3. Pour tester votre implementation, vous pouvez rouler le script `run_tests.py`.
   
Finalement, l'utilisation de librairies de résolution du problème de TSP comme networkx est interdite. Vous devez
implémenter votre propre algorithme de résolution de TSP à l'aide des librairies de base de python (numpy, scipy,
etc.). Vous pouvez utiliser des librairies pour générer des graphes aléatoires, mais vous ne pouvez pas utiliser de
librairies pour résoudre le problème de TSP.

## Critères d'évaluation
- Coût total du cycle hamiltonien: 50%
- Explication de la solution : 30%
- Qualité du code : 10%
- Utilisation d'environnement virtuel (venv): 5%
- Utilisation de Git : 5%

Le coût du cycle hamiltonien sera calculé à l'aide de l'objet `PerformanceTestCase` fournit dans le fichier 
[tester.py](tools/tester.py). Si l'interface n'est pas respecté (le type de sortie de 
la méthode `get_solution`, le nom de l'objet) ou si le code contient un/des erreur(s), la performance de votre code 
sera malheureusement égal à zéro. Dans ce cas, assurez-vous de bien respecter l'interface et de rouler les tests afin
de vous assurez de ne pas avoir de problème lors de la correction. Le score utilisé pour l'évaluation sera :
```
score = (target_cost / cycle_cost) * 100 [%]
```
où `target_cost` est le coût du cycle hamiltonien obtenu avec un algorithme choisi par les correcteurs et `cycle_cost`
est le coût du cycle hamiltonien obtenu avec votre algorithme. Le score sera donc égal à 100% si votre algorithme
trouve le cycle hamiltonien optimal et sera égal à 0% si votre algorithme trouve un cycle hamiltonien dont le coût est
infiniment grand. De plus, si votre algorithme trouve un chemin qui n'est pas un cycle hamiltonien, votre score sera
égal à 0%.

L'explication de la solution devra être contenue dans le fichier `README.md` de votre projet qui explique la solution 
que vous avez utilisé pour résoudre le problème. Cette explication sert essentiellement à nous permettre de savoir si
vous comprenez vraiment ce que vous avez fait ou si vous avez juste volé du code sur internet. Veuillez tout de même 
rester concis dans vos explications.

La qualité du code sera évalué à l'aide de l'outil [pycodestyle](https://pycodestyle.pycqa.org/en/latest/intro.html). 
Si votre code ne respecte pas les normes de [PEP8](https://peps.python.org/pep-0008/), vous perdrez des points. 

Afin de voir votre résultat sur les différents critères/échelons, vous pouvez lancer le script `main.py` avec
la commande:
```shell
python main.py
```
qui va rouler les tests et vous afficher vos résultats.


<span style="color:red;font-size:40pt">**ATTENTION** IL EST TRÈS IMPORTANTE DE RESPECTER LES SECTIONS SUIVANTES POUR QUE
VOTRE SOLUTION SOIT ÉVALUÉE</span> 

## Remise du projet

Pour remettre le projet, il suffit de s'assurer que le code soit dans la branche `main` du répertoire github créé à 
partir de github classroom. Le fichier `tsp.py` devra être modifié avec votre algorithme. 
Le fichier `README.md` contenant les explications de votre 
solution devra être présent dans le répertoire afin que nous puissions évaluer votre compréhension de la solution que vous 
avez utilisé. N'hésitez pas à ajouter des
images, des graphiques ou tout autre élément qui pourrait nous aider à comprendre votre solution.
Finalement, n'oubliez pas de mettre un fichier `requirements.txt` dans votre dossier afin que nous puissions installer 
les dépendances de votre code. Afin de générer ce fichier facilement, vous pouvez utiliser la librairie 
[pipreqs](https://pypi.org/project/pipreqs/) ou si vous utilisez *Pycharm* allez dans "*tools→Sync Python Requirements...*".

### Évaluation 
Votre code sera évalué automatiquement à l'aide de divers graph. À noter que les réseaux dont vous avez accès valider 
votre solution ne sont pas les mêmes que ceux utilisés pour l'évaluation finale. Donc, assurez-vous que votre solution 
soit générale. Vous pouvez ainsi avoir un score de 100% lors de vos essais, mais avoir un score inférieur lors de 
l'évaluation finale.


## Ressources
- [Discord server](https://discord.gg/F8kcefP3my) où vous pouvez poser vos questions et/ou
    collaborer avec vos coéquipiers.
- [GitHub](https://github.com/Progfest-2024/TSP-template) du défi.

## Auteurs
- [Jérémie Gince](https://github.com/JeremieGince)
- [Rémi Lamontagne Caron](https://github.com/rem657)


## Remerciements
Un gros merci à [Antoine Carrier](https://github.com/AntoineCarrier) pour avoir fournit l'idée du défi.