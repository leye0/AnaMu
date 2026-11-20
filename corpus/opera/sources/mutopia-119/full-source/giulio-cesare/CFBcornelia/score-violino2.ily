\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "violino2"
  >>
  \header {
    opus = "Aria. Cornelia: Cessa omai di sospirare"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
