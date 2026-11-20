\score {
  \instrStaff \markup "" <<
    \keepWithTag #'(partBoth not-flauti) \global
    \clef treble
    { R1*34 \includeNotes "flauti" }
  >>
  \header {
    opus = "Aria. Sesto: Svegliatevi nel core"
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}