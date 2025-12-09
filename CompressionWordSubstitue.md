# Algorithm Name: The 7308 Word-Substitution Compression

## 1\. Core Concept

This compression standard utilizes a fixed dictionary of the **7,308 most common words** (3 letters or longer) to reduce message size.

It works by splitting the dictionary into **29 "Banks"**. When a word from the dictionary is found in the text, it is replaced by a single non-printable ASCII character (a "Marker") representing that Bank. The specific index of the word within that Bank is then stored in a separate header.

## 2\. Data Structures

### The Dictionary (The 7308 Database)

  * **Total Size:** 7,308 words.
  * **Organization:** The words are distributed into **29 Banks**.
  * **Bank Capacity:** Each Bank holds **252 words**.
      * *Math:* $29 \text{ Banks} \times 252 \text{ words} = 7,308 \text{ words}$.

### The Markers (ASCII Control Codes)

Each of the 29 Banks is assigned a unique **ASCII non-printable character** (Indices 0–31).

  * **Excluded Characters:** To preserve text formatting, the standard whitespace control characters are **not** used as markers:
      * `0x09` (Horizontal Tab)
      * `0x0A` (Line Feed)
      * `0x0D` (Carriage Return)
  * **Function:** When a marker appears in the compressed text, it acts as a signal to "fetch the next word from this specific Bank."

## 3\. How It Works

The compressed file is constructed in two parts: the **Header** and the **Body**.

### Step A: Analysis & Replacement (The Body)

The algorithm scans the source text. If a word is found in the 7308-word database:

1.  It identifies which **Bank** the word belongs to (e.g., Bank `0x03`).
2.  It identifies the word's **Index** within that Bank (e.g., `0x25`).
3.  In the text, the original word is replaced by the **Marker** for that Bank (`0x03`).

### Step B: Building the Queues (The Header)

Simultaneously, the algorithm builds a Header containing 29 separate lists (queues)—one for each Bank.

  * When a word is replaced in the text, its **Index** is added to the corresponding list in the Header.
  * During decompression, every time the reader encounters a Marker in the body, it "pops" the next Index from that Bank's queue to retrieve the correct word.

-----

## 4\. Illustrated Example

**Original Text:**

> "The girl he loves is good because she is nice."

**Dictionary Assumptions for this Example:**

  * **"The"**: Located in Bank `0x00`, at Index `0x04`.
  * **"Because"**: Located in Bank `0x03`, at Index `0x09`.
  * **"Nice"**: Located in Bank `0x03`, at Index `0x25`.

### Compression Process:

1.  **"The" found:**
      * Replace word with Marker `0x00`.
      * Add Index `0x04` to Header Queue `0x00`.
2.  **"Because" found:**
      * Replace word with Marker `0x03`.
      * Add Index `0x09` to Header Queue `0x03`.
3.  **"Nice" found:**
      * Replace word with Marker `0x03`.
      * Add Index `0x25` to Header Queue `0x03`.

### Final Output Structure:

**The Header (The Queues)**
The header stores the sequence of word indices for each bank:

```text
Queue 0x00: 0x04            <-- Corresponds to 'The'
Queue 0x01: [Empty]
...
Queue 0x03: 0x09 0x25       <-- Corresponds to 'because', then 'nice'
...
(Remaining queues empty)
```

**The Body (Compressed Text)**
The text now contains unprintable characters (Markers) instead of the keywords:

```text
[0x00] girl he loves is good [0x03] she is [0x03].
```

**Result:**
The decoder reads the body.

1.  It sees `[0x00]`. It looks at Queue `0x00`, grabs the first item (`0x04`), and restores **"The"**.
2.  It sees the first `[0x03]`. It looks at Queue `0x03`, grabs the first item (`0x09`), and restores **"because"**.
3.  It sees the second `[0x03]`. It looks at Queue `0x03`, grabs the next item (`0x25`), and restores **"nice"**.

## 5\. Summary

  * **Efficiency:** In the example above, 14 bytes of raw text ("The", "because", "nice") were replaced by 3 bytes in the body plus 3 bytes in the header.
  * **Synchronization:** Both sender and receiver must possess the identical database of 7,308 words.
  * **Post-Processing:** Because the resulting file is binary, standard compression tools (like ZIP) can be applied afterward to achieve even higher compression ratios.
