# Format for data transmission

Adam -> Alex: Progressions

```javascript
{
    "progressions": [
        {
            "weight": 0, // some integer
            "chords": [  // list of chords
                {
                    "type": "I", // some string
                               // this is the chord type (e.g. tonic)
                    "inversion": 1 // the inversion, duh
                }, // This ends the definition of a chord
            ], // This ends the list of chords
        }, // This ends the definition of a progression
    ], // This ends the list of progressions
} // This ends the constant file data
```

Ethan -> Alex: Notes

```javascript
{
    "notes": [
        {
            "pitch": 60, // some integer
            "startTime": 6.5, // some float
            "duration": 0.5, // some float
            "velocity": 55 // some 7-bit integer
        } // This ends the definition of a note
    ] // This ends the list of notes
} // This ends the input
```

Alex: Internal representation of notes in the generator

```javascript
{
    "notes": [
        {
            "pitch": 0, // some integer in [0, 11]
            "startTime": 6.5, // some float
            "duration": 0.5, // some float
            "velocity": 55, // some 7-bit integer
            "octave": 1, // some integer; number of octaves removed
            "uuid": 1 // index in this list
        } // This ends the definition of a note
    ] // This ends the list of notes
} // This ends the format
```
