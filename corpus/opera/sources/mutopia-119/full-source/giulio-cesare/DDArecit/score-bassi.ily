\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'partUp \global
      \cesare \includeNotes #"cesare"
    >> \includeLyrics #"cesare-lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      \clef bass \includeNotes #"bassi"
      \includeFigures #"figures"
    >>
  >>
  \header {
    piece = "Scena IV."
    opus = "Recit. Cesare: Dall' ondoso periglio salvo mi"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
