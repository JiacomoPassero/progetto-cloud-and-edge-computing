## Introduzione
Il progetto è un blog realizzato tramite flask che svolge la funzione di Curriculum Vitae raccogliendo informazioni sulle competenze dell’autore e permette la pubblicazione post rappresentati da file md.

Le modifiche al progetto hanno come obiettivo di creare un container che permetta di semplificare l’avvio, la gestione e la portabilità del sito web e lo sviluppo un workflow CI/CD che permetta di testare, validare e pubblicare il progetto sul web tramite un'istanza EC2 di Amazon.

## Docker
Il progetto è stato inserito in un container docker ottenendo maggiore isolamento e portabilità rispetto al solo virtual environment di python.
Il [Dockerfile](https://github.com/JiacomoPassero/progetto-cloud-and-edge-computing/blob/produzione/Dockerfile) del progetto utilizza la versione 3.11 di python usando la relativa immagine dal repository ufficiale docker.
Dopo aver copiato i file sorgente e i post nella work directory vengono installate le librerie necessarie al blog e viene lanciato uno [script](https://github.com/JiacomoPassero/progetto-cloud-and-edge-computing/blob/produzione/first_start.sh) contenente i comandi di avvio dell’applicazione.

## Docker Compose
Applicazione flusk e database sono stati separati su due container la cui orchestrazione è gestita tramite l’apposito file [docker-compose.yml](https://github.com/JiacomoPassero/progetto-cloud-and-edge-computing/blob/produzione/docker-compose.yml).
Il database utilizza un immagine docker postgres definendone il nome e la coppia username/password necessari per connettersi.
Il secondo container ospitante l'applicazione flask usa il dockerfile definito nel progetto come immagine, descritto nella sezione precedente.

I due container sono connessi alla stessa rete privata usando un driver bridge e solamente la porta del sistema utilizzata dall’applicazione flusk viene mappata verso l’esterno.
Per il protocollo HTTP sono ammesse solamente connessioni sulla porta 8080 così da ridurre la superficie d'attacco del sistema.

Tramite l’uso di docker compose diventa possibile inizializzare ed avviare il progetto tramite l’esecuzione di un solo comando (docker compose up --build) ottenendo un processo più semplice rispetto alla versione iniziale.

## CI/CD PIPELINE
Per automatizzare le fasi di testing e deploy sono stati usati i workflows di github ovvero un meccanismo che permette di eseguire del codice (tramite containerizzazione) al verificarsi di determinati eventi nel repository; solitamente push su determinati branch.

Un workflow è definito da un file YAML al cui interno sono specificati vari jobs contenenti comandi di setup e il codice da eseguire.
Il progetto definisce in un unico [workflow](https://github.com/JiacomoPassero/progetto-cloud-and-edge-computing/blob/produzione/.github/workflows/ci-cd-pipeline.yml) un job di deploy che dipende da due job di testing in modo che la pubblicazione di una modifica non avvenga a meno che i controlli sulle funzionalità non siano superati.

Questa sequenza implementa una logica di sicurezza che interrompe l’aggiornamento del progetto se sono presenti potenziali vulnerabilità che verrebbero trasferite sull’istanza EC2 connessa ad internet.

## Test
Per la parte di continuous integration sono stati scritti due test suits che verificano correttezza del progetto e la qualità minima del codice da una prospettiva di sicurezza.

Il file PostValidation.py contiene un insieme di test che valida la struttura dei post affinchè  rispettino il template fornito.
Il file StaticAnalisys.py invece controlla il contenuto di app.py individuando un pattern specifico considerato tossico: l’avvio del progetto in modalità debug in produzione.
Il test fallisce se il progetto è impostato per essere eccessivamente verboso in caso di crash: un comportamento che costituisce una vulnerabilità di sicurezza.

## Deploy
Il deploy avviene su un'istanza amazon EC2 di tipo t2.micro impostata solo per accettare connessioni con un approccio whitelist/allowlist: solo HTTP sulla porta 8080 e connessioni SSH con autenticazione tramite chiave asimmetrica per l'aggiornamento del sito.
Le regole di connessione sono implementate tramite security groups di AWS: uno dedicato alle connessioni HTTPS e un secondo dedicato ad SSH. 

Sono disponibili ulteriori servizi AWS per permettere al progetto una scalabilità automatica completamente gestita ma che sono stati scartati perché eccessivi per le funzionalità presenti ed evitare costi imprevisti.

Le operazioni di deploy avvengono in un job dedicato che si connette all’istanza EC2 tramite canale SSH.
La connessione è implementata tramite una github action appositamente implementata e resa disponibile pubblicamente sulla stessa piattaforma.

Per permettere questo passaggio è necessario aggiungere al progetto alcuni dati sensibili che sono salvati nell’area Secrets di github per gestirli in maniera sicura.

L'istanza EC2 gratuita non permette di avere un hostname fisso dunque l'indirizzo pubblico può cambiare a seguito di interruzioni del suo funzionamento oppure dopo un reboot.
Quando ciò avviene è necessario aggiornare i Secrets dell'applicazione.

Lo stesso vale per quando la durata delle credenziali di connession scade.

Il job in caso di push sul branch “produzione” si connette all’istanza, copia i file aggiornati del repository nel sistema operativo dell’host e avvia il docker-compose del progetto ricreando creando il container aggiornato.

