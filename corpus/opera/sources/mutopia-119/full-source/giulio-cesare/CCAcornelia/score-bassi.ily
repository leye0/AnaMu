\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    \includeNotes "bassi"
    \includeFigures "figures"
  >>
  \header {
    piece = "Scena III."
    opus = "Arioso. Cornelia: Deh, piangete, o mesti lumi"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
