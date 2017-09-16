# Format for data transmission

Adam -> Alex: Progressions

```javascript
{
    "progression": [
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
    "notes": [
        {
            "pitch": 60, // some integer
            "startTime": 6.5, // some float
            // TODO
        }
    ]
} // This ends the input
```
