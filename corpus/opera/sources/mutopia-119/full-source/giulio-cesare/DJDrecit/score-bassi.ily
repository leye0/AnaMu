\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'() \global
      \cesare \includeNotes "cesare"
    >> \includeLyrics "cesare-lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      \clef bass \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
