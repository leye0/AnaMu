\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
