\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \scoreInit
      \keepWithTag #'up \global
      \cesare \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'partDown \global
      \clef bass \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
