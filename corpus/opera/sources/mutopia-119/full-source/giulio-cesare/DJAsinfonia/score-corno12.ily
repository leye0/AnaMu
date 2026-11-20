\score {
  \instrStaff \markup \instruments { 
    "Corno I. II." \smaller \italic "ex G." }
  <<
    \keepWithTag #'(corno partBoth) \global
    \clef treble
    \new Voice <<
      { \oneVoice s1*4 s2 \voiceOne s2 s4
        \oneVoice s16 \voiceOne s8. s4
        \oneVoice s16 \voiceOne s8. s1*4 s4
        \oneVoice s2. s1*2 s2 s16 \voiceOne s8. s4
        \oneVoice s16 \voiceOne s8. s2. s1*4 s2.
        \oneVoice s4 s2. s8 \voiceOne s8^\markup \tempo Adagio. s2. 
        \oneVoice s8 \voiceOne s8 s2.
        \oneVoice s4 s1*2
      }
      \includeNotes "corno1" 
    >>
    \new Voice { \voiceTwo \includeNotes "corno2" }
  >>
  \header {
    piece = "Scena Ultima."
    opus = "Sinfonia"
    breakbefore = #(break-before?) 
  }
  \layout { }
}
