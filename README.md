# 📘 Projekt-Anleitung: Flas BAUM 
k + MySQL auf PythonAnywhereTest
Diese Anleitung beschreibt den kompletten Ablauf, um das Projekt auszuführen und im Team (GitHub + PythonAnywhere) zu entwickeln.

**Hinweis:** Nur eine Person pro Team muss diese Anleitung durchführen.

## ✅ Voraussetzungen

### 👥 Team

-   Alle Teammitglieder besitzen einen **GitHub-A ccount**
-   **Eine Person** besitzt einen **PythonAnywhere-Account**
-   Diese Person teilt das PythonAnywhere-Login **mit dem Team** (damit alle deployen können)

------------------------------------------------------------------------

## 🚀 1. GitHub-Projekt einrichten

### 1.1 Vorlage importieren

1.  Repository öffnen:\
    👉 https://github.com/EgliMNG/db-project
2.  Rechts oben **Fork** klicken
3.  Das neue Repo heisst z.B. username/db-project

### 1.2 Teammitglieder einladen
Im geforkten Repo:
1.  Settings
2.  Collaborators
3.  Add people
4.  Teammitglieder + **Lehrperson** einladen

------------------------------------------------------------------------

## 🌐 2. PythonAnywhere vorbereiten
👉 https://www.pythonanywhere.com

### 2.1 Teacher hinzufügen
1. Account → Education → *Enter your teacher's username*

### 2.2 Neue Flask-Webapp erstellen
1.	Menü: Web → Add new web app
2.	Flask auswählen
3.	Python 3.13 auswählen

### 2.3 Webapp-Verzeichnis ersetzen
1.	Zurück auf das Dashboard
2.	Jetzt Terminal öffnen\
→ Open Bash Console (links auf den Button $ Bash) klicken.

``` bash
# Das von GitHub geforkte Repo klonen
git clone https://github.com/<dein_github_username>/<dein_repo>.git

# Alte Struktur löschen
rm -rf mysite

# Neuen Code als Webapp-Verzeichnis verwenden
mv <dein_repo> mysite 
```

------------------------------------------------------------------------

### 2.4 Autodeployment (post-merge Hook)
Damit Änderungen von GitHub automatisch deployed werden:

1.  Script anlegen und ausführbar machen
``` bash
cd mysite/.git/hooks
touch post-merge
chmod +x post-merge
```

2.  Konsole schliessen
3.  Im Menü auf *Files*
4.  In den Ordner *mysite/.git/hooks* navigieren (Ordnerstruktur links)
5.  File *post-merge* (rechts) öffnen, folgenden Inhalt einfügen und speichern (Save). **Wichtig:** Der username muss hier in Kleinbuchstabe geschrieben werden! 
```bash
#!/bin/bash
touch /var/www/<lowercase(username_pythonanywhere)>_pythonanywhere_com_wsgi.py
```

------------------------------------------------------------------------

## 🗄️ 3. MySQL-Datenbank einrichten

### 3.1 Datenbank erstellen
1.  Im Menü rechts oben auf *Databases* klicken
2.  Unter MySQL ein DB-Passwort wählen und das Passwort notieren (wird im nächsten Schritt benötigt)
3.  Mit "Initialize MySQL" bestätigen
4.  Mit einem Klick auf die neu erstellte DB "&lt;username&gt;$default" die MySQL-Konsole öffnen. (Wenn Console Limit erreicht, auf dem Dashboard oder im Menü Consoles z.B. Bash Console schliessen)
5.  In MySQL-Konsole SQL Script ausführen:

``` sql
SOURCE mysite/db/TODOS.sql;
```
Dadurch wird die gesamte Struktur der Datenbank erstellt.

------------------------------------------------------------------------

### 3.2 `.env` erstellen
1.  Im Menü auf *Files*
2.  Im Textfeld *.env* eintippen und auf "New file" klicken (unbedingt auf der obersten Stufe und **nicht** im "mysite"-Ordner)

3.  Inhalt:
```
DB_HOST=<username_pythonanywhere>.mysql.pythonanywhere-services.com
DB_USER=<username_pythonanywhere>
DB_PASSWORD=<dein_db_passwort>
DB_DATABASE=<username_pythonanywhere>$default
W_SECRET=<irgend_ein_secret>
```
Für `W_SECRET` darfst du irgend eine Buchstaben- und Zahlenkombination wählen und notieren, da du diese im nächsten Schhritt wieder brauchst

------------------------------------------------------------------------

## 🔄 4. GitHub-WebHook für automatisches Deployment

Im GitHub-Repo:
1.  Settings → Webhooks → Add webhook
2.  URL:\
    https://&lt;username_pythonanywhere&gt;.pythonanywhere.com/update_server
3.  Content type: `application/json`
4.  Secret: Die geheime Kombination, die du im ".env" unter `W_SECRET` gesetzt hast
5.  **Add webhook**

------------------------------------------------------------------------

## ✅ 5. Website testen
1. Rufe die URL http://<username_pythonanywhere>.pythonanywhere.com auf.
2. Siehst du ein Login? Klicke auf registrieren und registriere einen User
3. Falls du noch die Message "Welcome to Flask!" siehst, gehe zurück zum Menü "Web" und klicke auf 🔄 Reload

------------------------------------------------------------------------

## 🔗 6. Nützliche Links
- DB-Testing: https://www.db-fiddle.com/
- MySQL: https://www.w3schools.com/mysql/default.asp
- Python: https://www.w3schools.com/python/default.asp
- HTML / CSS:
    - Sammlung von UI-Elementen: https://www.w3schools.com/howto/howto_css_icon_bar.asp
    - HTML: https://www.w3schools.com/html/default.asp
    - CSS: https://www.w3schools.com/css/default.asp
    - Bootstrap-UI-Elemente: https://getbootstrap.com/docs/5.3/examples/
- Flask: https://www.geeksforgeeks.org/python/flask-tutorial/
- Git: https://www.w3schools.com/git/default.asp
