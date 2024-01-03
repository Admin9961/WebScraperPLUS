L'autore di questo programma, Christopher Zonta, non si assume alcuna responsabilità di lamentele legate a rilevamenti di falsi positivi
dichiarati da VirusTotal, dei suoi prodotti & partner affiliati. Il codice di questi 3 .EXE corrisponde esattamente ai 3 file .py allocati nella
repository "WebscraperPLUS", che sono forniti in plain text con tanto di commenti. Mi dissocio da ogni accusa di "diffusione di malware" dichiarata
da alcuni prodotti antivirus che flaggano erroneamente gli artefatti generati da Pyinstaller come malware, che in definitiva sono rilevamenti
causati dalle signature della versione di Pyinstaller in uso sul mio dispositivo locale (Windows 10 Home build 1904).

In caso si sospetti della presenza di malware in questi .EXE esistono tre opzioni:
- Testare gli .EXE in una sandbox, come VMware, o Virtual Box;
- Non testarli proprio e lasciarli perdere;
- Eseguire la variante in .py, scaricando l'interpreter di Python 3.12 con i relativi importi indicati in 'requirements.txt', eseguendo il comando terminal 'pip install -r requirements.txt'

Questi .EXE sono open source e chiunque può effettuare liberamente il loro 'reverse engineering', modificarli, migliorarli o peggiorarli a proprio piacimento,
in quanto la repository "WebscraperPLUS" è pubblica e forkabile.

I requisiti d'esecuzione, sono possedere un computer (o macchina virtuale) dotati di Windows 10 (si raccomanda la build 1904 come minimo, pubblicata da
Microsoft nel 2020, ma anche le versioni più recenti, incluso Windows 11, potrebbero essere supportate), e dotato di processore AMD64.
Il programma è incompatibile con i processori i386, ed è inoltre incompatibile con tutte le versioni di Windows precedenti al 10.
L'esecuzione su Wine (Unix) non è stata testata, e il programma è completamente (e ovviamente) incompatibile con Macintosh, e tutti i sistemi nativi Unix.
