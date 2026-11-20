%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup "Violino II." <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "violino2"
    >>
    \instrStaff \markup \instruments { "Violino II." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-tutti2"
    >>
  >>
  \layout {}
}