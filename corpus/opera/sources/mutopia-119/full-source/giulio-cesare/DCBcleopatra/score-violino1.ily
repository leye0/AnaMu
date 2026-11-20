\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef treble
    {
      \includeNotes #"violino1-1"
      \includeNotes #"violini-2"
    }
  >>
  \header {
    opus = "Aria. Cleopatra: Piangerò la sorte mia"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
