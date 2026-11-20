\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \scoreInit
      \keepWithTag #'recit  \global
      \includeNotes #"recit"
    >> \includeLyrics #"lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'partDown \global
      \clef bass \includeNotes #"bassi"
      \includeFigures #"figures"
    >>
  >>
  \header {
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
