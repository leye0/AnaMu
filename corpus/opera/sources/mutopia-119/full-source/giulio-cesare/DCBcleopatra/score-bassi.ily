\score {
  \instrStaff \markup "" <<
    \keepWithTag #'partBoth \global
    \clef bass
    {
      \includeNotes #"bassi-1"
      <<
        \includeNotes #"bassi-2"
        \break
        \includeFigures #"figures-2"
      >>
    }
  >>
  \header {
    opus = "Aria. Cleopatra: Piangerò la sorte mia"
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
