# Nahrada komunit a draftu - proposal

Record prochazi retezcem stavu. Retezec by mel byt konfigurovatelny
v ramci konfigurace komunity, ne v kodu.

Prvni stav je vzdycky "new", dalsi stavy nejsou presne definovany

Jeden zaznam bude rozclenen na verze. Kazda verze ma svoje vlastni PID,
ktere vypada: ``{base-pid}.v{version}.{version}`` nebo ``{base-pid}.{state}``

V kazdem kroku existuje koncept "posledniho" zaznamu. Je to zaznam 
v nejpokrocilejsim retezci stavu, ktery ma zaroven nejvyssi verzi
(ne timestamp).

Tento posledni zaznam ma v pid tabulce alias ``base-pid``

Příklad:

Retezec stavu bude [open, published]

Vedec vytvori zaznam s internim UUID <1>, ten dostane PID:
  * abcde-fghij  <primary>
  * abcde-fghij.open

Pozdeji zazada o publikaci. Vznika Request s typem "requestStateChangePublished"
a po jeho schvaleni (v prubehu se musi nastavit verze zaznamu, pocatecni
je 1.0, ale je mozno ji zmenit) ma zaznam PIDcka:
  * abcde-fghij  <primary>
  * abcde-fghij.published
  * abcde-fghij.v1.0

Vedec bude chtit do zaznamu udelat zmeny. Vznikne Request s typem 
"requestStateChangeChangeNew", a vznika kopie zaznamu s internim UUID <2> s pid:
  * abcde-fghij.open  <primary>

Pri zazadani o publikaci (opet requestStateChangePublished) a schvaleni 
dojde k nasledujicimu:

UUID <1>:
  * abcde-fghij.v1.0  <primary>

UUID <2>:
  * abcde-fghij  <primary>
  * abcde-fghij.published
  * abcde-fghij.v1.1


Konfigurace stavu (per community):

  * Nazev stavu
  * predchozi stav(y)
  * nasledujici stav
  * seznam roli, ktere mohou videt record ve stavu
  * seznam roli, ktere mohou editovat record ve stavu
  * seznam jsonpath, jejichz editace je povolena
  * seznam roli, ktere mohou provest tranzici do dalsiho stavu, 
    pokud je stav validni
  * seznam roli, ktere mohou provest tranzici do dalsiho stavu, 
    pokud stav neni validni

Stav je validni, pokud marshmallow schema a jsonschema omezene 
na pathy union(jsonpath stavu, jsonpath predchozich stavu) je validni,
tj. chyby na jinych paths ignorujeme.


## Pripad delsiho retezce

``[new, open, approved, published]``

## Pripad "obraceny strom"

Do komunity je mozno jak harvestovat, tak i vkladat zaznamy (a nebo jeden model
ma 2 komunity, jedna vklada primo a druha harvestuje).

Harvest retezec:
``[harvested, published]``

Deposit retezec:
``[new, open, approved, published]``







