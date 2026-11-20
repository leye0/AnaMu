%% Sinfonia
\score {
  \instrStaff \markup "" <<
    \keepWithTag #'() \global
    \clef alto
    \includeNotes "viola"
  >>
  \header {
    opus = "Sinfonia."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
