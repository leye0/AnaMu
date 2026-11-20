\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(not-flauti partBoth) \global
    \clef bass
    \includeNotes "bassi"
  >>
  \header {
    opus = "Aria. Sesto: Svegliatevi nel core"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
