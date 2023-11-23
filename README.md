------ D-LAN 2023 ------
Årets sida är skapt med hjälp av Django och Bootstrap. Eventuella ändringar som behövr göras i grundfunktionaliteten för webbsidan kräver viss kännedom om dessa ramverk, och jag hänvisar till deras respektive dokumentation.

-- Sökvägar att hålla extra koll på: - /static/
Innehåller alla statiska filer såsom bilder, fonts, CSS och JS-filer. - /templates/
Här finns alla template-filer som nyttjas för sidan - base.html innehåller header och footer, alla andra html-filer motsvarar en individuell view på sidan och kan uppdateras individuellt vid behov.

-- Deployment
Om denna sida kommer att återanvändas för framtida D-LAN så följer nedan en grov guide för deployment efter att all relevant information är uppdaterad.

    - Tillgång till sektionens server tillhandahålls av nuvarande Webmaster. Kontakta vederbörande för tillgång.

    - Främst hänvisar jag till Djangos deployment-checklist, som kan hittas via Google. Här finns instruktioner kring rimliga kontroller att göra i Djangos källkod innan sidan lanseras.

    - Projektet bör med fördel ligga lagrat på GitLab, och det enklaste sättet att få upp filerna på sektionens server är genom att klona GitLab-projektet. Var NOGA med att projektets secret key (k.txt i nuvarande version) INTE läggs upp på GitLab, och att eventuell ny nyckel finns med i .gitignore.

    - Samma sak gäller för Stripes nycklar, som självklart inte heller får lagras på Git. Dessa behöver manuellt läggas in när projektet lanseras.
