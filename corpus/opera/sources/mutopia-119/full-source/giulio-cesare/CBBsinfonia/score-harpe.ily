\score {
  \new GrandStaff <<
    \instrStaff \markup "" <<
      \keepWithTag #'partUp \global
      \clef treble \includeNotes "harpe1"
    >>
    \instrStaff \markup "" <<
      \keepWithTag #'partDown \global
      \clef bass \includeNotes "harpe2"
    >>
  >>
  \header {
    opus = "Sinfonia."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
