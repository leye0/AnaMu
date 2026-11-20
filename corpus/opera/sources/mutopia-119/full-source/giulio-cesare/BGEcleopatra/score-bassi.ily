\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cleopatra: Tutto può donna Vezzosa, s'amorosa"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
