# Assembleur pour le jeu d'instructions R12

Exécutez simplement `./cr12.py prog.r12` pour compiler le fichier `prog.r12` contenant des instructions R12.

Par défaut, les instructions codées en binaire seront affichées à la console. Pour les sauvegarder dans un fichier,
redirigez simplement la console vers le fichier:

  > ./cr12.py prog.r12 > prog.bin

Le compilateur supporte les formats d'instruction suivants:
1. `op rd, rs1, rs2`
2. `op rd, rs1`
3. `op rd, rs1, imm4`
4. `op rs, imm6`

où `rd`, `rs1` et `rs2` sont l'un ou l'autre des quatre registres d'**architecture** R0, R1, R2 ou R3,
et où `imm4` et `imm6` sont des valeurs entières (constantes) de quatre (4) ou six (6) bits.
Notez que chaque instruction doit se trouver sur une ligne distincte, et que les lignes blanches
sont permises. 

Pour le quatrième format (`jal`, `bz`, et `bnz`), une étiquette de branchement peut être utilisée. 
Pour définir une étiquette de branchement, il suffit de la définir de la façon suivante avant:
```nom_d_etiquette:```
Les lettres majuscules sont permises.
Lors de la compilation du quatrième format, si `imm6` est une étiquette, le compilateur calculera 
la difference entre les addresses de l'instruction courrante et l'instruction qui suit directement 
l'étiquette. Cette difference sera utilisé comme valeur `imm`.

Les commentaires peuvent être ajoutés n'importe où avec le symbole `#`.

Ce logiciel vous est offert gracieusement, mais sans aucune garantie de bon fonctionnement.
