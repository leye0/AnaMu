\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(other partBoth) \global
    \clef treble
    \includeNotes "tutti2"
  >>
  \header {
    opus = "Coro. Ritorni omai nel nostro core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
