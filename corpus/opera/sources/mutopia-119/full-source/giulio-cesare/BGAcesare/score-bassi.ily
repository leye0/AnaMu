\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'partUp \global
      \cesare \includeNotes #"cesare" 
    >> \includeLyrics #"cesare-lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'partDown \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena VII."
    opus = "Recit. Cesare: Alma del gran Pompeo"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
