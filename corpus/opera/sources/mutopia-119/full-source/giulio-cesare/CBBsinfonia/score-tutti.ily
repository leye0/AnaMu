%% Sinfonia
\score {
  \instrStaff \markup "" <<
    \keepWithTag #'() \global
    \clef treble
    \includeNotes "tutti"
  >>
  \header {
    opus = "Sinfonia."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
