\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(partBoth other) \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    piece = "Atto Primo, Scena I."
    opus = "Coro. Viva il nostre Alcide"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
