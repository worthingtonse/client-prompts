
Backgroud Styling

Starts with the background byt SB (section break).

First byte is the includes bigfield. 

Bit Index | Name | Meaning
---|---|---
0  | Has BG Color | Is there a background color section?  false means transparent
1  | Has a background image |  Is there an image section
2  | Does it have a two color gradient?  |  Does it use a gradiant with two colors?
3  | Does it have a three color gradient?  |  Does it use a gradiant with four colors?
4  | Does it have a four color gradient?  |  Does it use a gradiant with four colors?  
5  | Is it animated?  | Does the background contain animation? 
6  | Does the background have events?  |  Does the background react to events and switch styles? 
7  | Can the user set the style? | Can the user's browser set the style

The order of the bytes that follow depend on the bitfield above. 


Name | bytes | meaning 
---|---|---
BG Color | 2 | up to 65K colors
BG Image | 16 | The first byte says how long the image id is. The image ID consists of the storage cluser ID and the image ID (2 bytes then 14 ID bytes)

etc
