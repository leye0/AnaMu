\score {
  \instrStaff \markup \instruments {
    "Corno III. IV." \smaller \italic "ex D." } 
  <<
    \keepWithTag #'(partBoth corno) \global
    \clef treble
    \new Voice <<
      { \oneVoice s1*10 \voiceOne s2.
        \oneVoice s16 \voiceOne s8. s4
        \oneVoice s16 \voiceOne s8. s2 s1 s2.
        \oneVoice s16 \voiceOne s8. s2.
        \oneVoice s4 s1*3 s2 s8 \voiceOne s4. s2.
        \oneVoice s4 s1*2 s2 s4. \voiceOne s8^\markup \tempo Adagio. s2.
        \oneVoice s8 \voiceOne s8 s2.
        \oneVoice s4
      }
      \includeNotes "corno3" 
    >>
    \new Voice { \voiceTwo \includeNotes "corno4" }
  >>
  \header {
    piece = "Scena Ultima."
    opus = "Sinfonia"
    breakbefore = #(break-before?) 
  }
  \layout { }
}
