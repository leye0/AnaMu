%% Recitativo.
\score {
  \new OrchestraStaffGroup <<
    \recitStaff <<
      \keepWithTag #'recit \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'() \global
      \clef bass
      \includeNotes "bassi"
    >>
  >>
  \header {
    piece = "Scena IX."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
