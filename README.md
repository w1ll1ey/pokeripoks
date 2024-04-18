# Autovertailusovellus:

## Käyttöohjeet:

1. Kloonaa repositorio tietokoneellesi
2. Lisää sen juurikansioon .env-tiedosto ja määritä sen sisältö näin:
```DATABASE_URL=<add-your-local-database>
SECRET_KEY=<add-your-secret-key>```
3. Aktivoi virtuaaliympäristö:
```$ python3 -m venv venv```
```$ source venv/bin/activate```
4. Asenna sovelluksen riippuvuudet:
```$ pip install -r ./requirements.txt```
5. Määritä tietokannan skeema:
```$ psql < schema.sql```
6. Käynnistä sovellus:
```$ flask run```

## Nykyinen tila:

- käyttäjä voi luoda tunnukset ja kirjautua niillä sisään
- käyttäjä voi luoda auton yhteiseen tietokantaan ja antaa sille tietoja
- käyttäjä voi luoda vertailuja henkilökohtaisilla parametreillä ja lisätä niihin autoja
- sovellus hyödyntää tietokannan tietoja ja sen lisäksi että esittelee ne vertailussa laskee niistä myös uusia tietoja, kuten käyttökustannusten osa-alueita (polttoaine, verot jne.) ja kokonaisuuksia

## TODO:

- mahdollisuus syöttää ja hyödyntää enemmän dataa autoista
- mahdollisuus syöttää enemmän tietoja vertailun yksilöintiä varten
- parempi visuaalinen toteutus ja muotoilu etenkin vertailun kohdalta
- mahdollinen: käyttäjät voi syöttää kokemuksia omistamistaan autoista ja siten esim. keskimääräisiä huoltokustannuksia voisi saada selville
- käytettävyyden parantaminen (merkittävästi)
- luonnoskoodien poisto

