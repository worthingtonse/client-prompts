# QMail Protocol
The QMail protocol is designed to replace the existing email system. 

## RAIDA Mail Folder Structure
The all-folders folder holds all the user and public files. 

Each user is identified by a five byte identifier. Each user has a folder in the private folders that is based on their identifier. The user-folder folder has 256 sub folders
named after the first hexidecimal characters in the users ID. Then, there are four levels of subfolders so that the leaf folders are five folders deep. 

Each user has some standard folders. The user can create any folders that they want but there will always be a Mail folder. 
Within the mail folder there are two types of files, file stipes (.bin) and pointers (.lnk) to file stripes that are located in the public-files. 

```
00
--Mail
----c10d92f83091496d893f8e20f30372ea.0.bin // First Version of the file. 
----c10d92f83091496d893f8e20f30372ea.1.bin // File 0 after it haws been changed. 
----c10d92f83091496d893f8e20f30372ea.2.bin
----.c10d92f83091496d893f8e20f30372ea.3.bin // File after it has been deleted (has a . infont of it. Users can still see deleted files and undelete them)
----e08b3a6835c34716bad5bfe5a6d556cc.lnk // Link to a public file. 

```

## File Nameing convention. 
The file name is composed of two parts:
1. The 1 byte hexidencimal charactger identifier (Random and the same on all 
1. The 8 hexidencimal charactger identifier (Random and the same on all 
1. The 16 hexidecimal character Metadata name.
2. The 16 hexidecimal character shuffling order identifiers. These are used to encrypt the message. 

### The common name is added with the other bytes from other 

This part is returned by the "List Mail Names" service. All the names are added together to create 128 bytes. These bytes can converted into UTF-8. 

Files have a GUID for a name.

```tree
all-folders
--public-folders
----00
------00
--user-folders
----00
----01
----02
----03
----00

```
## Requirments

1. Must to require a domain owener to give email.
2. Does not require a the sender or receiver to have a centralized email server
3. Has a decentralized directory to that people can publish, manage and unpublish their contact information.
4. Stop Spam by making it too expensive
5. Allow users to be paid when the accept emails.
6. Not allow emails to be sent unless they have been paid for.
7. Allow anyone to create a server and earn money by hosting email services.
8. Make email impossible to hack or lose.
9. Make emails quantum safe in transmission and storage.
10. Stop people from monitoring if their emails have been opened. 
11. Reduce storage space by having common server storage areas where data objects can be accessed by multiple people.
12. Make it faster to send and receive emails.
13. Be able to accept annonymous emails but also be able to turn them away.
14. Be able to have end to end encryption that is quantum safe and uses 256 bit AES CTR encryption.
15. Remove HTML, CSS and Javascript from emails and replace it with a much lighter formatting system. 
16. Remove attachments but instead use optional downloads.
17. Being able to send an email and prove your identity if you wish.
18. Allow people to vouch for the authenticity of the sender and receiver.

## Service

Phase | Name | Description
---|---|---
1 | [Update Directory](#update-director) | Allows people to advertise themselves in the directory

1 |[Read Directory](#read-directory) | User can search for the email they want to send to

1 |[Fetch Email](#fetch-email)

1 |[Send To One](#send-to-one) | From to To

2 |[Send To Many](#send-to-many) | One person can send email to many people. 

2 |[Send Associated File](#send-associated-file)

2 |[Fetch Attachement](#fetch-attachement)

3 |[Set Autoresponse](#set-autoresponse)

3 |[Vouch For or Against Sender](#vouch-for-or-against-sender)

3 |[Confirm Receipt](#confirm-receipt)

4 |[Post Master Key](#receiver-post-master-key) | Allows peer to perr encryption but may not be so secure

4 |[Get Receiver's Key](#get-receiver-key) | Allows peer to perr encryption but may not be so secure




## Update Director
This service allows a receiver to tell people how to contact them, how much it costs to send email to them and weather a sender is free or blocked. 

ERD of the Directory

**Table User**

Datatype | Name | Description
---|---|---
int | ID | Primary Key. DN SN SN SN SN (Five bytes of the user's key that show the denomination and four byte serial number)
int | Alias | The name that the person want's to be called by 
string | description  | self discription 
timestamp  | date created   | Set by system
string | Key exchange servers  |  array of raida servers used to exchange keys (ip and port)
string | Email storage servers | array of raida servers used to exchange emails (ip and port  
int | annoyed in past month  | How many people send annoymnet reports 
int | hated in past month | How many people sent hate reports for this email.  
int | User's receiving fee  | How many coins the user needs in order to accept an email
       
## Email Addresses: 

| Dec | Hex | Role | Adjective | Plural Noun |
|-----|-----|------|-----------|-------------|
| 0 | 00 | Keeper | Ancient | Stars |
| 1 | 01 | Guardian | Swift | Crystals |
| 2 | 02 | Sage | Mystic | Shadows |
| 3 | 03 | Scholar | Crimson | Winds |
| 4 | 04 | Warden | Silver | Waters |
| 5 | 05 | Master | Golden | Flames |
| 6 | 06 | Lord | Emerald | Stones |
| 7 | 07 | Lady | Azure | Dreams |
| 8 | 08 | Knight | Violet | Echoes |
| 9 | 09 | Ranger | Ivory | Thorns |
| 10 | 0A | Hunter | Obsidian | Moons |
| 11 | 0B | Seeker | Coral | Tides |
| 12 | 0C | Wanderer | Amber | Sands |
| 13 | 0D | Herald | Jade | Storms |
| 14 | 0E | Oracle | Ruby | Depths |
| 15 | 0F | Mystic | Sapphire | Heights |
| 16 | 10 | Scribe | Bronze | Paths |
| 17 | 11 | Bard | Copper | Realms |
| 18 | 12 | Smith | Iron | Visions |
| 19 | 13 | Weaver | Steel | Whispers |
| 20 | 14 | Crafter | Silk | Secrets |
| 21 | 15 | Builder | Velvet | Riddles |
| 22 | 16 | Maker | Marble | Puzzles |
| 23 | 17 | Shaper | Glass | Mirrors |
| 24 | 18 | Carver | Crystal | Prisms |
| 25 | 19 | Forger | Diamond | Jewels |
| 26 | 1A | Mender | Pearl | Treasures |
| 27 | 1B | Healer | Opal | Riches |
| 28 | 1C | Teacher | Quartz | Gifts |
| 29 | 1D | Guide | Onyx | Tokens |
| 30 | 1E | Leader | Beryl | Charms |
| 31 | 1F | Captain | Garnet | Amulets |
| 32 | 20 | Admiral | Topaz | Relics |
| 33 | 21 | Commander | Turquoise | Artifacts |
| 34 | 22 | General | Peaceful | Totems |
| 35 | 23 | Marshal | Perfect | Emblems |
| 36 | 24 | Sentinel | Perpetual | Symbols |
| 37 | 25 | Watchman | Powerful | Signs |
| 38 | 26 | Scout | Priceless | Marks |
| 39 | 27 | Spy | Bloodstone | Runes |
| 40 | 28 | Agent | Pleading | Glyphs |
| 41 | 29 | Envoy | Polished | Scripts |
| 42 | 2A | Emissary | Radical | Letters |
| 43 | 2B | Ambassador | Radioactive | Words |
| 44 | 2C | Diplomat | Fluorite | Tales |
| 45 | 2D | Negotiator | Pious | Stories |
| 46 | 2E | Mediator | Refined | Legends |
| 47 | 2F | Arbiter | Primitive | Myths |
| 48 | 30 | Judge | Renowned | Fables |
| 49 | 31 | Magistrate | Random | Epics |
| 50 | 32 | Chancellor | Resilient | Chronicles |
| 51 | 33 | Minister | Priceless | Ballads |
| 52 | 34 | Advisor | Repressed | Verses |
| 53 | 35 | Counselor | Righteous | Stanzas |
| 54 | 36 | Consul | Ringing | Melodies |
| 55 | 37 | Elder | Seething | Harmonies |
| 56 | 38 | Patriarch | Realgar | Rhythms |
| 57 | 39 | Matriarch | Sacred | Cadences |
| 58 | 3A | Chieftain | Regal | Tempos |
| 59 | 3B | Warlord | Scholarly | Beats |
| 60 | 3C | Overlord | Screaming | Pulses |
| 61 | 3D | Sovereign | Bornite | Cycles |
| 62 | 3E | Monarch | Shadowy | Spirals |
| 63 | 3F | Emperor | Shattered | Circles |
| 64 | 40 | Empress | Shimmering | Spheres |
| 65 | 41 | Prince | Silent | Orbs |
| 66 | 42 | Princess | Minium | Globes |
| 67 | 43 | Duke | Massicot | Bubbles |
| 68 | 44 | Duchess | Litharge | Droplets |
| 69 | 45 | Count | Smiling | Pearls |
| 70 | 46 | Countess | Speckled | Beads |
| 71 | 47 | Baron | Soaring | Chains |
| 72 | 48 | Baroness | Sparkling | Links |
| 73 | 49 | Viscount | Soothing | Bonds |
| 74 | 4A | Viscountess | Sleepy | Threads |
| 75 | 4B | Marquis | Simple | Cords |
| 76 | 4C | Marquise | Adamite | Ropes |
| 77 | 4D | Earl | Olivenite | Cables |
| 78 | 4E | Bishop | Libethenite | Webs |
| 79 | 4F | Archbishop | Dioptase | Networks |
| 80 | 50 | Cardinal | Chrysocolla | Lattices |
| 81 | 51 | Pope | Azurite | Grids |
| 82 | 52 | Priest | Malachite | Patterns |
| 83 | 53 | Monk | Cuprite | Designs |
| 84 | 54 | Friar | Atacamite | Motifs |
| 85 | 55 | Abbot | Brochantite | Themes |
| 86 | 56 | Prior | Antlerite | Concepts |
| 87 | 57 | Deacon | Chalcanthite | Ideas |
| 88 | 58 | Acolyte | Melanterite | Thoughts |
| 89 | 59 | Novice | Epsomite | Notions |
| 90 | 5A | Initiate | Kieserite | Theories |
| 91 | 5B | Apprentice | Hexahydrite | Principles |
| 92 | 5C | Student | Unlikely | Axioms |
| 93 | 5D | Pupil | Rozenite | Truths |
| 94 | 5E | Disciple | Bonattite | Facts |
| 95 | 5F | Follower | Unleashed | Realities |
| 96 | 60 | Devotee | Cornwallite | Essences |
| 97 | 61 | Believer | Pseudomalachite | Spirits |
| 98 | 62 | Pilgrim | Reichenbachite | Souls |
| 99 | 63 | Crusader | Linarite | Hearts |
| 100 | 64 | Paladin | Caledonite | Minds |
| 101 | 65 | Champion | Leadhillite | Bodies |
| 102 | 66 | Hero | Susannite | Forms |
| 103 | 67 | Warrior | Macquartite | Shapes |
| 104 | 68 | Fighter | Chenite | Images |
| 105 | 69 | Soldier | Unearthly | Figures |
| 106 | 6A | Veteran | Paralaurionite | Silhouettes |
| 107 | 6B | Mercenary | Undisputed | Outlines |
| 108 | 6C | Gladiator | Unforgivable | Contours |
| 109 | 6D | Duelist | Universal | Profiles |
| 110 | 6E | Swordsman | Unlocked | Sketches |
| 111 | 6F | Archer | Vengeful | Drawings |
| 112 | 70 | Marksman | United | Paintings |
| 113 | 71 | Sniper | Vibrant | Portraits |
| 114 | 72 | Assassin | Visionary | Pictures |
| 115 | 73 | Rogue | Delafossite | Scenes |
| 116 | 74 | Thief | Wandering | Views |
| 117 | 75 | Bandit | Weeping | Vistas |
| 118 | 76 | Outlaw | Tenorite | Landscapes |
| 119 | 77 | Pirate | Winged | Horizons |
| 120 | 78 | Buccaneer | Chalcocite | Skylines |
| 121 | 79 | Corsair | Digenite | Cloudscapes |
| 122 | 7A | Privateer | Covellite | Rainbows |
| 123 | 7B | Navigator | Bornite | Auroras |
| 124 | 7C | Pilot | Chalcopyrite | Comets |
| 125 | 7D | Captain | Cubanite | Meteors |
| 126 | 7E | Helmsman | Whimsical | Asteroids |
| 127 | 7F | Bosun | Bravoite | Galaxies |
| 128 | 80 | Admiral | Wistful | Nebulae |
| 129 | 81 | Commodore | Linnaeite | Constellations |
| 130 | 82 | Fleet | Siegenite | Systems |
| 131 | 83 | Skipper | Violarite | Clusters |
| 132 | 84 | Mariner | Polydymite | Groups |
| 133 | 85 | Sailor | Greigite | Sets |
| 134 | 86 | Seaman | Smythite | Collections |
| 135 | 87 | Crew | Zealous | Assemblies |
| 136 | 88 | Deck | Pyrrhotite | Gatherings |
| 137 | 89 | Mate | Niccolite | Meetings |
| 138 | 8A | Chief | Breithauptite | Councils |
| 139 | 8B | Boss | First | Committees |
| 140 | 8C | Director | Last | Boards |
| 141 | 8D | Manager | Long | Panels |
| 142 | 8E | Supervisor | Skutterudite | Juries |
| 143 | 8F | Foreman | Rammelsbergite | Tribunals |
| 144 | 90 | Overseer | Safflorite | Courts |
| 145 | 91 | Inspector | Lollingite | Chambers |
| 146 | 92 | Monitor | Little | Halls |
| 147 | 93 | Observer | Great | Rooms |
| 148 | 94 | Watcher | New | Spaces |
| 149 | 95 | Lookout | Other | Places |
| 150 | 96 | Sentry | Old | Areas |
| 151 | 97 | Guard | Good | Zones |
| 152 | 98 | Protector | Michenerite | Regions |
| 153 | 99 | Defender | Sudburyite | Territories |
| 154 | 9A | Shield | Kotulskite | Domains |
| 155 | 9B | Bastion | Froodite | Kingdoms |
| 156 | 9C | Fortress | Sopcheite | Empires |
| 157 | 9D | Citadel | Stibiopalladinite | Nations |
| 158 | 9E | Tower | Palladseite | Countries |
| 159 | 9F | Rampart | Braggite | Lands |
| 160 | A0 | Bulwark | Vysotskite | Worlds |
| 161 | A1 | Vanguard | Cooperite | Planets |
| 162 | A2 | Pioneer | Bowieite | Satellites |
| 163 | A3 | Explorer | Laurite | Moons |
| 164 | A4 | Trailblazer | Erlichmanite | Suns |
| 165 | A5 | Pathfinder | Osmiridium | Stars |
| 166 | A6 | Scout | Iridosmine | Lights |
| 167 | A7 | Tracker | Platiniridium | Rays |
| 168 | A8 | Pursuer | Iridoplatinum | Beams |
| 169 | A9 | Chaser | Rutheniridosmium | Flashes |
| 170 | AA | Hunter | Ruthenosmiridium | Sparks |
| 171 | AB | Stalker | Osmium | Glows |
| 172 | AC | Predator | Iridium | Shines |
| 173 | AD | Prowler | Ruthenium | Gleams |
| 174 | AE | Lurker | Rhodium | Glimmers |
| 175 | AF | Creeper | Palladium | Twinkles |
| 176 | B0 | Crawler | Platinum | Sparkles |
| 177 | B1 | Sneak | Gold | Dazzles |
| 178 | B2 | Phantom | Silver | Blazes |
| 179 | B3 | Specter | Copper | Burns |
| 180 | B4 | Ghost | Zinc | Flickers |
| 181 | B5 | Spirit | Lead | Wavers |
| 182 | B6 | Wraith | Tin | Dances |
| 183 | B7 | Shade | Iron | Flows |
| 184 | B8 | Shadow | Nickel | Streams |
| 185 | B9 | Echo | Cobalt | Rivers |
| 186 | BA | Whisper | Chromium | Currents |
| 187 | BB | Murmur | Manganese | Tides |
| 188 | BC | Hum | Vanadium | Waves |
| 189 | BD | Buzz | Titanium | Surges |
| 190 | BE | Drone | Scandium | Rushes |
| 191 | BF | Throb | Yttrium | Gushes |
| 192 | C0 | Pulse | Zirconium | Floods |
| 193 | C1 | Beat | Hafnium | Torrents |
| 194 | C2 | Rhythm | Tantalum | Cascades |
| 195 | C3 | Cadence | Niobium | Waterfalls |
| 196 | C4 | Tempo | Molybdenum | Springs |
| 197 | C5 | Meter | Tungsten | Wells |
| 198 | C6 | Measure | Rhenium | Pools |
| 199 | C7 | Time | Technetium | Lakes |
| 200 | C8 | Clock | Ruthenium | Oceans |
| 201 | C9 | Timer | Lightning | Seas |
| 202 | CA | Watch | Thunder | Bays |
| 203 | CB | Bell | Platinum | Harbors |
| 204 | CC | Chime | Aurum | Ports |
| 205 | CD | Ring | Tingling | Docks |
| 206 | CE | Toll | Fragrant | Shores |
| 207 | CF | Gong | Pulsing | Beaches |
| 208 | D0 | Drum | Excited | Coasts |
| 209 | D1 | Horn | Peaceful | Cliffs |
| 210 | D2 | Trumpet | Hydrargyrum | Peaks |
| 211 | D3 | Flute | Joyful | Summits |
| 212 | D4 | Pipe | Happy | Heights |
| 213 | D5 | Reed | Sharp | Tops |
| 214 | D6 | String | Blissful | Caps |
| 215 | D7 | Bow | Euphoric | Crowns |
| 216 | D8 | Harp | Sparkling | Crests |
| 217 | D9 | Lyre | Glowing | Ridges |
| 218 | DA | Lute | Radiant | Ranges |
| 219 | DB | Zither | Light | Chains |
| 220 | DC | Dulcimer | Dark | Spines |
| 221 | DD | Sitar | Bright | Bones |
| 222 | DE | Tabla | Sweet  | Ribs |
| 223 | DF | Drum | Blissful | Joints |
| 224 | E0 | Cymbal | Fluffy | Limbs |
| 225 | E1 | Gong | Hard | Wings |
| 226 | E2 | Triangle | Plutonium | Feathers |
| 227 | E3 | Chime | Soft | Plumes |
| 228 | E4 | Bell | Fiery  | Scales |
| 229 | E5 | Whistle | Silky  | Shells |
| 230 | E6 | Flute | Electric  | Husks |
| 231 | E7 | Fife | Euphoric  | Pods |
| 232 | E8 | Piccolo | Fragrant  | Seeds |
| 233 | E9 | Oboe | Lavender  | Grains |
| 234 | EA | Clarinet | Rough | Kernels |
| 235 | EB | Bassoon | Smooth | Nuts |
| 236 | EC | Saxophone | Icy | Fruits |
| 237 | ED | Trombone | Steamy | Berries |
| 238 | EE | Trumpet | Freezing | Blossoms |
| 239 | EF | French | Burning | Flowers |
| 240 | F0 | Tuba | Cold | Petals |
| 241 | F1 | Euphonium | Hot | Leaves |
| 242 | F2 | Baritone | Cool | Branches |
| 243 | F3 | Cornet | Warm | Twigs |
| 244 | F4 | Flugelhorn | Minty | Stems |
| 245 | F5 | Bugle | Savory | Roots |
| 246 | F6 | Posthorn | Tangy | Vines |
| 247 | F7 | Alphorn | Spicy | Tendrils |
| 248 | F8 | Shofar | Salty | Shoots |
| 249 | F9 | Conch | Bitter | Buds |
| 250 | FA | Didgeridoo | Sweet | Sprouts |
| 251 | FB | Vuvuzela | Stellar | Blades |
| 252 | FC | Kazoo | Cosmic | Spikes |
| 253 | FD | Harmonica | Ethereal | Points |
| 254 | FE | Accordion | Celestial | Tips |
| 255 | FF | Concertina | Divine | Edges |

