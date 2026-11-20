%% Sinfonia
\score {
  \new StaffGroup <<
    \instrStaff \markup "Violino I." <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "tutti"
    >>
    \instrStaff \markup \instruments { "Violino I." (Orchestra) } <<
      \keepWithTag #'() \global
      \clef treble
      \includeNotes "orch-tutti1"
    >>
  >>
  \layout {}
}