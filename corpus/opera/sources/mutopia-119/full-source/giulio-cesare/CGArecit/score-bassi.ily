\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'up \global
      \cleopatra \includeNotes "cleopatra"
    >> \includeLyrics "cleopatra-lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena VII."
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
