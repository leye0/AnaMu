\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    { \includeNotes "violini" \bar "||" }
  >>
  \header {
    piece = "Scena IX."
    opus = "Arioso. Tolomeo: Belle dee di questo core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
