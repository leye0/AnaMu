%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \recitStaff <<
      \keepWithTag #'(recit hack) \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'() \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena X."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { indent = \smallindent }
}
