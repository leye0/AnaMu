\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef tenor
    \includeNotes "gamba"
  >>
  \header {
    opus = "Aria. Cleopatra: V'adoro, pupile"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
