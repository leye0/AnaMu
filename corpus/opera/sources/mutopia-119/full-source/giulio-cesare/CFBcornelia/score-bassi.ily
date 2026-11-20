\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Cornelia: Cessa omai di sospirare"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
