\score {
  \new StaffGroup <<
    \instrStaff \markup { Violoncelli } <<
      \keepWithTag #'partUp \global
      \clef bass
      \includeNotes "bassi"
    >>
    \instrStaff \markup \instruments { Bassi (Orchestra) } <<
      \keepWithTag #'partDown \global
      \clef bass
      \includeNotes "orch-bassi"
    >>
  >>
  \header {
    breakbefore = #(break-before?) 
  }
  \layout { }
}
