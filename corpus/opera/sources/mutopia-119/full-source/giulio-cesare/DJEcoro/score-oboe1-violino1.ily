\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(other partBoth) \global
    \clef treble
    \includeNotes "tutti1"
    { s4 s1*43 s2. \break }
  >>
  \header {
    opus = "Coro. Ritorni omai nel nostro core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
