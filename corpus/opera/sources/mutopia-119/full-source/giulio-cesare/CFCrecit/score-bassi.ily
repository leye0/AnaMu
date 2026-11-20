\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \scoreInit
      \keepWithTag #'up  \global
      \sesto \includeNotes "sesto"
    >> \includeLyrics "sesto-lyrics"
    \instrStaff \markup "" <<
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
