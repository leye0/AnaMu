\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \scoreInit
      \keepWithTag #'recit \global
      {
        s1*5 \break
        s1 s1*3 \break 
        s1*4 s1 s4 \break
        s1*4 \break
        s1*4 s4 s1 \break
        s1*5
      }
      \includeNotes "recit"
    >>
    \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'() \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena IV."
    opus = "Recitativo"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
