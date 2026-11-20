\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(other partBoth) \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Coro. Ritorni omai nel nostro core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
