\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    piece = "Scena IX."
    opus = "Arioso. Tolomeo: Belle dee di questo core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
