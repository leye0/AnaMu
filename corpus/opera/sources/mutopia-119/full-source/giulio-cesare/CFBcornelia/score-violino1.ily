\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino1"
  >>
  \header {
    opus = "Aria. Cornelia: Cessa omai di sospirare"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
