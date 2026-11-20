\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    \includeNotes "flauti"
  >>
  \header {
    opus = "Aria. Cornelia: Cessa omai di sospirare"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
