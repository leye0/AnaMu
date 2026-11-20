%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \recitStaff <<
      \global
      \includeNotes "recit"
    >>
    \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena II."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { indent = \noindent }
}
