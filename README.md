setmaster
=========

THIS IS NOT A FINISHED WORK! And I am not actively developing this. Anyone can fork it. If you have any questions regarding this you can send me an email on pedromcaraujo@gmail.com. 

I use my fork of https://github.com/bransorem/Magic-Scraper in https://github.com/pedroma/Magic-Scraper to do an initial import of the card into mongo and then just use some python scripts to finish of the import.

Document structure of cards::

Normal card
```json
{
    "setname" : "M11",
    "front" : {
        "image" : "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=205957&type=card",
        "multiverse_id" : 205957,
        "artist" : "Aleksi Briclot",
        "pt" : "4",
        "othersets" : {
            "0" : "Magic 2010 (Mythic Rare)",
            "1" : "Magic 2011 (Mythic Rare)",
            "2" : "Lorwyn (Rare)"
        },
        "colors" : [
            "White"
        ],
        "number" : "1",
        "rarity" : "Mythic Rare",
        "converted" : 4,
        "flavor" : "None",
        "set" : "Magic 2011",
        "text" : {
            "0" : "+1: You gain 2 life.",
            "1" : "-1: Put a +1/+1 counter on each creature you control. Those creatures gain vigilance until end of turn.",
            "2" : "-6: Put a white Avatar creature token onto the battlefield. It has \"This creature's power and toughness are each equal to your life total.\""
        },
        "type" : "Planeswalker  — Ajani",
        "mana" : {
            "0" : "2",
            "1" : "White",
            "2" : "White"
        },
        "name" : "Ajani Goldmane"
    },
    "id" : 205957
}
```

Double card (split):
```json
{
    "setname" : "Apocalypse",
    "front" : {
        "partB" : {
            "image" : "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=27165&type=card",
            "multiverse_id" : 27165,
            "artist" : "David Martin",
            "pt" : "None",
            "othersets" : {
                "0" : "Apocalypse (Uncommon)",
                "1" : "Apocalypse (Uncommon)",
                "2" : "Magic: The Gathering-Commander (Uncommon)",
                "3" : "Duel Decks: Izzet vs. Golgari (Uncommon)"
            },
            "colors" : [
                "Blue"
            ],
            "number" : "128",
            "rarity" : "Uncommon",
            "converted" : 2,
            "flavor" : "None",
            "set" : "Apocalypse",
            "text" : "None",
            "type" : "Instant",
            "mana" : {
                "0" : "1",
                "1" : "Blue"
            },
            "name" : "Ice"
        },
        "partA" : {
            "image" : "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=27165&type=card",
            "multiverse_id" : 27165,
            "artist" : "David Martin",
            "pt" : "None",
            "othersets" : {
                "0" : "Apocalypse (Uncommon)",
                "1" : "Apocalypse (Uncommon)",
                "2" : "Magic: The Gathering-Commander (Uncommon)",
                "3" : "Duel Decks: Izzet vs. Golgari (Uncommon)"
            },
            "colors" : [
                "Red"
            ],
            "number" : "128",
            "rarity" : "Uncommon",
            "converted" : 2,
            "flavor" : "None",
            "set" : "Apocalypse",
            "text" : {
                "0" : "Fire deals 2 damage divided as you choose among one or two target creatures and/or players.",
                "1" : ""
            },
            "type" : "Instant",
            "mana" : {
                "0" : "1",
                "1" : "Red"
            },
            "name" : "Fire"
        }
    },
    "id" : 27165,
    "_id" : ObjectId("517131993a92cdfc5f0052e9"),
    "__v" : 0
}

```
Double card (flip)
```json
{
    "front" : {
        "image" : "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=74489&type=card",
        "multiverse_id" : 74489,
        "artist" : "Tsutomu Kawade",
        "pt" : "2 / 2",
        "othersets" : "None",
        "colors" : [
            "Blue"
        ],
        "number" : "31",
        "rarity" : "Uncommon",
        "converted" : 3,
        "flavor" : "None",
        "set" : "Betrayers of Kamigawa",
        "text" : {
            "0" : "Whenever you cast a Spirit or Arcane spell, you may put a ki counter on Callow Jushi.",
            "1" : "At the beginning of the end step, if there are two or more ki counters on Callow Jushi, you may flip it.",
            "2" : "----",
            "3" : "Jaraku the Interloper",
            "4" : "Legendary Creature — Spirit",
            "5" : "3/4",
            "6" : "Remove a ki counter from Jaraku the Interloper: Counter target spell unless its controller pays {{2}}."
        },
        "type" : "Creature  — Human Wizard",
        "mana" : {
            "0" : "1",
            "1" : "Blue",
            "2" : "Blue"
        },
        "name" : "Callow Jushi"
    },
    "id" : 74489,
    "_id" : ObjectId("5179786225d14f572b00000f"),
    "__v" : 0
}
```


Double card (double):
```json
{
    "setname" : "Innistrad",
    "back" : {
        "image" : "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=226755&type=card",
        "multiverse_id" : 226755,
        "artist" : "Nils Hamm",
        "pt" : "3 / 2",
        "othersets" : "None",
        "colors" : [
            "Blue"
        ],
        "number" : "51b",
        "rarity" : "Common",
        "converted" : "None",
        "flavor" : {
            "0" : "\"Unfortunately, all my test animals have died or escaped, so I shall be the final subject. I feel no fear. This is a momentous night.\"",
            "1" : "—Laboratory notes, final entry"
        },
        "set" : "Innistrad",
        "text" : {
            "0" : "Flying"
        },
        "type" : "Creature  — Human Insect",
        "mana" : "None",
        "name" : "Insectile Aberration"
    },
    "front" : {
        "image" : "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=226755&type=card",
        "multiverse_id" : 226755,
        "artist" : "Nils Hamm",
        "pt" : "1 / 1",
        "othersets" : "None",
        "colors" : [
            "Blue"
        ],
        "number" : "51a",
        "rarity" : "Common",
        "converted" : 1,
        "flavor" : "None",
        "set" : "Innistrad",
        "text" : {
            "0" : "At the beginning of your upkeep, look at the top card of your library. You may reveal that card. If an instant or sorcery card is revealed this way, transform Delver of Secrets."
        },
        "type" : "Creature  — Human Wizard",
        "mana" : {
            "0" : "Blue"
        },
        "name" : "Delver of Secrets"
    },
    "id" : 226755,
    "_id" : ObjectId("5171312c3a92cdfc5f004eac"),
    "__v" : 0
}
```

Card types are: flip (74489), split (27165), double (226755), normal
What it should be:
```json
{
    "set": "Innistrad",
    "multiverse_id": 226755,
    "image": "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=226755&type=card",
    "artist": "Nils Hamm",
    "rarity": "Common",
    "othersets": "None",
    "type": "double",
    "card": {
        "pt" : "1 / 1",
        "colors" : [
            "Blue"
        ],
        "number" : "51a",
        "converted" : 1,
        "flavor" : "None",
        "text" : {
            "0" : "At the beginning of your upkeep, look at the top card of your library. You may reveal that card. If an instant or sorcery card is revealed this way, transform Delver of Secrets."
        },
        "type" : "Creature  — Human Wizard",
        "mana" : {
            "0" : "Blue"
        },
        "name" : "Delver of Secrets"
    },
    "extra": {
        "pt" : "3 / 2",
        "colors" : [
            "Blue"
        ],
        "number" : "51b",
        "converted" : "None",
        "flavor" : {
            "0" : "\"Unfortunately, all my test animals have died or escaped, so I shall be the final subject. I feel no fear. This is a momentous night.\"",
            "1" : "—Laboratory notes, final entry"
        },
        "text" : {
            "0" : "Flying"
        },
        "type" : "Creature  — Human Insect",
        "mana" : "None",
        "name" : "Insectile Aberration"
    }

}
```
