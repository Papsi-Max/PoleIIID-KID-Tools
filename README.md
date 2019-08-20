# PoleIIID-KID-Tools

Veuillez trouver dans ce document toutes les informations relatives aux scripts Python que j'ai développé durant 
mon cursus scolaire. Le dossier contient quatre scripts rédigés pour un projet en particulier, KID, un film de fin
d'étude réalisé en deux ans et produit par huit étudiants. Dans ce document, je décris le contenu de chacun des 
scripts pour une meilleure compréhension de leur utilité.

### AETools : Animation Export Tools

AETools est un interface orienté export d’animation pour Maya. Il comprend une partie playblast pour permettre à
l’animateur d’avoir un aperçu rapide de son animation et une partie alembic qui lui permet d’exporter l’animation
de ses personnages en quelques clics. Pour des facilités d’utilisation, le script peut être placé dans la barre de
raccourci de Maya.

Lorsque vous lancez le script, une fenêtre s’ouvre laissant apparaître un interface qui contient les options nécessaires 
à l’animateur pour exporter son animation. Vous pouvez retrouver sur cette interface des champs pré renseignés si les 
conditions le permettent. Divisé en deux parties distinctes, le côté droit est réservé à l’export vidéo de l’animation alors
que la branche de gauche comprend les options liés à la partie alembic.

Sous le bouton “Launch Playblast” se trouve une fonction qui a pour objectif de configurer les options de playblast 
avant de pouvoir le lancer. Ces conditions existent pour vous empêcher d’écraser par maladresse un fichier du même
nom. Pour une lecture fluide de la vidéo, le script fait appel à «ffmpeg» qui converti le playblast en .mkv avec le 
codec H264 qui, en plus de fluidifier la lecture, rend le fichier moins volumineux.

Le bouton “Launch ABC Exporter”, cache une autre fonction. Cette fonction vérifie que les cases sélectionnées ont leur
correspondance dans la scène. Si c’est le cas, il sélectionne les maillages en question et les exporte en format .abc avec
toutes les options nécessaires au bon développement du reste du projet. Dans le cas où la case n’a pas de correspondance, 
le script passe tout simplement à la l’étape suivante. L’export des lights ne se fait pas en .abc mais en fichier .ma pour 
des raisons de non compatibilité des lights avec l’alembic.

### AutoAssemblyBuilder :

AutoAssemblyBuilder est un outil pour Maya qui automatise la création de scène d’assemblage.

Le script se lance dans une scène vierge. Il faut choisir la séquence et le plan que vous voulez assembler dans la fenêtre 
qui s’est ouverte. Après la validation du plan, le script cherche dans les dossiers de production à atteindre l’emplacement 
spécifique du plan. Les fichiers .ma et .mb du dossier sont importés dans la scène. Le programme scanne le nom de chaque 
fichier pour trouver son équivalent alembic. En cas de correspondance, le script importe le fichier .abc qui donnera la 
position et l’animation du mesh dans l’espace. Il se termine après avoir importé les fichiers .vdb.

### ArnoldBatchRender :

ArnoldBatchRender est un ensemble de scripts qui fonctionne en standalone permettant de rendre plusieurs scènes Maya à 
la suite. Ils ouvrent les scènes sélectionnées sans interface graphique et utilise Arnold pour exécuter le rendu.

Le script “startBatching_IRL.py” se dirige versle dossier contenant les scènes Maya à rendre, dossier qui doit être renseigné 
au préalable dans le script, puis il liste toutes les scènes. Ensuite, il mémorise le path de la première scène et lance le 
script de rendu, “myPyScriptForRender_IRL.py”. Une fois que le rendu est terminé, le script remplace le path de la scène par 
la suivante, etc jusqu’à atteindre la fin de la liste.

Le script de rendu est organisé en plusieurs étapes. Il commence par vérifier si la scène existe en testant son path. Dans le 
cas où le chemin est inexistant, le script s’arrête et “startBatching_IRL.py” reprend la main. Ensuite, il copie un fichier 
contenant une liste de presets pour la fenêtre de rendu de Maya et le colle dans un dossier destiné à ce type de fichier, 
dossier défini et verrouillé par Maya. Puis le script charge le plugin “Arnold”, si il ne l’était pas déjà, et charge
le fichier de preset. Il restera les paramètres spécifiques aux plans et le destinations des rendus que le script changera 
par lui même.

Une fois la configuration des paramètres achevée, il crée un fichier .bat qui sert à lancer “Render.exe”, un exécutable qui 
effectue les rendus de Maya. La dernière étape consiste à exécuter le fichier .bat. Lorsque le rendu est terminé, le script 
ferme la scène.

Ce script ne sera pas utilisé lors de la production par souci de licence. Arnold ajoutait un watermark sur les rendus en standalone.

### AutoCompo :

AutoCompo est un outil pour Nuke qui automatise la préparation de la scène de travail du compositeur. Il permet à l’utilisateur 
d’ajouter dans sa scène tous les éléments relatifs au plan sur lequel il travaillera en lui installant un template de node qui 
lui allègent son travail de préparation de scène. Pour des facilités d’utilisation, le script peut être placé dans la barre de 
raccourci de Nuke.

Au lancement du script, le compositeur renseigne le numéro de séquence ainsi que le numéro du plan qui sera composé. Lorsque 
que l'utilisateur a validé son choix de plan, le script ajoute ces informations au path pour atteindre le dossier contenant 
les pass à composer. Il ajoute les fichiers dans Nuke en créant, pour chaque fichier, deux nodes qu’il relie, une node Read 
et une node Unpremult. Il paramètre la node Read en lui ajoutant, après un formatage spécifique à Nuke, le path de l’image 
associée. Ensuite, il crée une node Premult que le script relie à toutes les nodes Unpremult précédemment créés. Enfin, il 
ajoute une node Write qu’il configure pour que le compositeur puisse rendre ses plans sans se soucier des paramètres lié au rendu.

Le département Composition ne voulait pas de précomposition dans le script.

Liste d’autres outils moins conséquents réalisés pour la production :
- **ConvAviToJpg**
- **LighterTools (réalisé après demande du département Lighting)**
- **animAnimationTools**
- **removeNamespace**
- **resetPivotTo0**

### Contact :
* Maxime BOULOGNE
* Junior TD
* maxime.boulogne.3D@gmail.com
* +33 669 983 617
